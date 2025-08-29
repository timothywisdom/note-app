from typing import Protocol, runtime_checkable
from ..models import Note, LLMEnrichment

@runtime_checkable
class LLMServiceProtocol(Protocol):
    """Protocol defining the interface for LLM services."""
    
    async def generate_enrichments(self, note: Note) -> LLMEnrichment:
        """
        Generate enrichments for a note using an LLM.
        
        Args:
            note: The note to generate enrichments for
            
        Returns:
            LLMEnrichment: The generated enrichments
            
        Raises:
            Exception: If enrichment generation fails
        """
        ...
