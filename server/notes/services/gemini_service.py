import json
from typing import Dict, Any, Optional
from pydantic import ValidationError
from datetime import datetime, timezone
import google.generativeai as genai
from ..models import Note, LLMEnrichment, Sentiment
from ..interfaces import LLMServiceProtocol

# Maximum number of attempts for structured response generation
MAX_ATTEMPTS = 3

class GeminiService(LLMServiceProtocol):
    """Real LLM service using Google's Gemini API for generating note enrichments."""
    
    def __init__(self, gemini_model: genai.GenerativeModel):
        """Initialize the LLM service with a configured Gemini model."""       
        self.model = gemini_model
        
    async def generate_enrichments(self, note: Note) -> LLMEnrichment:
        """
        Generate enrichments for a note using Gemini API with function calling.
        Includes retry logic with error feedback for structured response validation.
        
        Args:
            note: The note to generate enrichments for
            
        Returns:
            LLMEnrichment: The generated enrichments
            
        Raises:
            Exception: If enrichment generation fails after MAX_ATTEMPTS
        """
        # Create the prompt for analysis
        prompt = self._create_analysis_prompt(note)
        
        # Get the JSON schema for structured output
        json_schema = self._get_json_schema()
        
        last_error = None
        
        for _attempt in range(MAX_ATTEMPTS):
            try:
                # Generate response with structured output
                json_str = await self._call_gemini_api_structured(prompt, json_schema, last_error)
                
                # Parse and validate the response
                enrichments = self._parse_structured_response(json_str)
                
                return enrichments
                
            except ValidationError as e:
                last_error = str(e)
                # Continue to next attempt with error feedback
                continue
                
            except Exception as e:
                # Non-validation errors should be raised immediately
                raise Exception(f"Failed to generate enrichments: {e}")
        
        # If we reach here, all attempts failed with ValidationError
        raise Exception(f"Failed to generate valid enrichments after {MAX_ATTEMPTS} attempts. Last error: {last_error}")
    
    def _create_analysis_prompt(self, note: Note) -> str:
        """Create a simple prompt for note analysis."""
        return f"""
You are an AI assistant that analyzes notes and generates enrichments. 

Please analyze the following note content and provide insights for:
- A concise summary (2-3 sentences)
- Key topics and themes
- Sentiment analysis (positive, negative, or neutral)
- Important entities (people, places, concepts)
- Relevant tags for categorization
- Complexity assessment (0.0 to 1.0 scale)

Note content:
{note.content}

Please provide your analysis in the requested structured format. 
Note: Do not include enrichment_timestamp or llm_model fields - these will be set automatically.
"""
    
    def _get_json_schema(self) -> Dict[str, Any]:
        """Generate JSON schema from the LLMEnrichment Pydantic model."""
        return LLMEnrichment.model_json_schema()
    
    async def _call_gemini_api_structured(self, prompt: str, json_schema: Dict[str, Any], previous_error: Optional[str] = None) -> str:
        """Call the Gemini API with structured output using the JSON schema."""
        try:
            # Configure generation to use structured output
            generation_config = genai.types.GenerationConfig(
                temperature=0.1,  # Lower temperature for more consistent structured output
                top_p=0.8,
                top_k=40,
                max_output_tokens=2048,
            )
            
            # Create the structured prompt with error feedback if available
            error_feedback = ""
            if previous_error:
                error_feedback = f"""

IMPORTANT: The previous attempt to generate a JSON response failed with this validation error:
{previous_error}

Please carefully review the schema requirements and ensure your response exactly matches the expected format. Pay special attention to:
- Required fields that must be present
- Correct data types for each field
- Proper enum values where specified
- Correct field names and structure

"""
            
            structured_prompt = f"""
{prompt}{error_feedback}

Please respond with a JSON object that matches this exact schema:

{json.dumps(json_schema, indent=2)}

Return only the JSON object, no additional text or formatting.
"""
            
            # Call the Gemini API
            response = await self.model.generate_content_async(
                structured_prompt,
                generation_config=generation_config
            )
            
            if response.text:
                # Extract JSON from the response
                json_str = self._extract_json_from_response(response.text)
                return json_str
            else:
                raise Exception("Empty response from Gemini API")
                
        except Exception as e:
            raise Exception(f"Gemini API call failed: {e}")
    
    def _parse_structured_response(self, json_str: str) -> LLMEnrichment:
        """Parse the structured response and validate it against the LLMEnrichment model."""
        # Validate against Pydantic model
        enrichments = LLMEnrichment.model_validate_json(json_str)
        enrichments.enrichment_timestamp = datetime.now(timezone.utc).isoformat()
        enrichments.llm_model = self.model.model_name
        
        return enrichments
            
    
    def _extract_json_from_response(self, response: str) -> str:
        """Extract JSON content from the LLM response, handling markdown formatting."""
        import json
        
        # Remove markdown code blocks if present
        if "```json" in response:
            start = response.find("```json") + 7
            end = response.find("```", start)
            if end != -1:
                json_content = response[start:end].strip()
            else:
                json_content = response[start:].strip()
        elif "```" in response:
            # Remove markdown code blocks without language specification
            start = response.find("```") + 3
            end = response.find("```", start)
            if end != -1:
                json_content = response[start:end].strip()
            else:
                json_content = response[start:].strip()
        else:
            # Return the response as-is if no markdown formatting
            json_content = response.strip()

        # Parse and re-serialize JSON to remove formatting whitespace
        parsed_json = json.loads(json_content)
        return json.dumps(parsed_json, separators=(',', ':'))
