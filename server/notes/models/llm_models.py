from pydantic import BaseModel, Field
from datetime import datetime
from .enums import Sentiment

class LLMEnrichment(BaseModel):
    """Model for LLM-generated note enrichments."""
    summary: str = Field(..., description="AI-generated summary of the note content")
    topics: list[str] = Field(..., description="Extracted topics from the note content")
    sentiment: Sentiment = Field(..., description="Analyzed sentiment of the note content")
    key_entities: list[str] = Field(..., description="Key entities (nouns) identified in the note content")
    suggested_tags: list[str] = Field(..., description="AI-suggested tags for the note")
    complexity_score: float = Field(..., description="Calculated complexity score of the note content")
    enrichment_timestamp: datetime = Field(..., description="Timestamp when enrichment was generated")
    llm_model: str = Field(..., description="Name/version of the LLM model used")
