import json
import asyncio
from typing import Dict, Any
from pydantic import ValidationError
import google.generativeai as genai
from ..models import Note, LLMEnrichment, Sentiment
from ..interfaces import LLMServiceProtocol

class GeminiService(LLMServiceProtocol):
    """Real LLM service using Google's Gemini API for generating note enrichments."""
    
    def __init__(self, gemini_model: genai.GenerativeModel):
        """Initialize the LLM service with a configured Gemini model."""
        if not gemini_model:
            raise ValueError("Gemini model is required")
        
        self.model = gemini_model
        
    async def generate_enrichments(self, note: Note) -> LLMEnrichment:
        """
        Generate enrichments for a note using Gemini API with function calling.
        
        Args:
            note: The note to generate enrichments for
            
        Returns:
            LLMEnrichment: The generated enrichments
            
        Raises:
            Exception: If enrichment generation fails
        """
        try:
            # Create the prompt for analysis
            prompt = self._create_analysis_prompt(note)
            
            # Get the JSON schema for structured output
            json_schema = self._get_json_schema()
            
            # Generate response with structured output
            response = await self._call_gemini_api_structured(prompt, json_schema)
            
            # Parse and validate the response
            enrichments = self._parse_structured_response(response)
            
            return enrichments
            
        except Exception as e:
            raise Exception(f"Failed to generate enrichments: {e}")
    
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
    
    async def _call_gemini_api_structured(self, prompt: str, json_schema: Dict[str, Any]) -> Dict[str, Any]:
        """Call the Gemini API with structured output using the JSON schema."""
        try:
            # Configure generation to use structured output
            generation_config = genai.types.GenerationConfig(
                temperature=0.1,  # Lower temperature for more consistent structured output
                top_p=0.8,
                top_k=40,
                max_output_tokens=2048,
            )
            
            # Create the structured prompt
            structured_prompt = f"""
{prompt}

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
                return json.loads(json_str)
            else:
                raise Exception("Empty response from Gemini API")
                
        except Exception as e:
            raise Exception(f"Gemini API call failed: {e}")
    
    def _parse_structured_response(self, response_data: Dict[str, Any]) -> LLMEnrichment:
        """Parse the structured response and validate it against the LLMEnrichment model."""
        try:
            # Always set the timestamp to when this enrichment was created
            from datetime import datetime, timezone
            response_data["enrichment_timestamp"] = datetime.now(timezone.utc).isoformat()
            
            # Always set the model name
            response_data["llm_model"] = self.model.model_name
            
            # Validate against Pydantic model
            enrichments = LLMEnrichment(**response_data)
            
            return enrichments
            
        except Exception as e:
            raise ValidationError(f"Failed to parse structured response: {e}", model=LLMEnrichment)
    
    def _extract_json_from_response(self, response: str) -> str:
        """Extract JSON content from the LLM response, handling markdown formatting."""
        # Remove markdown code blocks if present
        if "```json" in response:
            start = response.find("```json") + 7
            end = response.find("```", start)
            if end != -1:
                return response[start:end].strip()
        
        # Remove markdown code blocks without language specification
        if "```" in response:
            start = response.find("```") + 3
            end = response.find("```", start)
            if end != -1:
                return response[start:end].strip()
        
        # Return the response as-is if no markdown formatting
        return response.strip()
