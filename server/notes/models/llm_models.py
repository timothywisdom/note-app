from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from .enums import Sentiment

class LLMEnrichment(BaseModel):
    """Model for LLM-generated note enrichments."""
    summary: str = Field(..., description="AI-generated summary of the note content")
    topics: list[str] = Field(..., description="Extracted topics from the note content")
    sentiment: Sentiment = Field(..., description="Analyzed sentiment of the note content")
    key_entities: list[str] = Field(..., description="Key entities (nouns) identified in the note content")
    suggested_tags: list[str] = Field(..., description="AI-suggested tags for the note")
    complexity_score: float = Field(..., description="Calculated complexity score between 0 and 1 of the note content")
    enrichment_timestamp: Optional[datetime] = Field(None, description="Timestamp when enrichment was generated")
    llm_model: Optional[str] = Field(None, description="Name/version of the LLM model used")
