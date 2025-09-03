from ..models import Note, LLMEnrichment, Sentiment
from ..interfaces import LLMServiceProtocol

class LLMStubService(LLMServiceProtocol):
    """Stub service for simulating LLM interactions to generate note enrichments."""
    
    async def generate_enrichments(self, note: Note) -> LLMEnrichment:
        """
        Generate enrichments for a note using an LLM.
        This is a placeholder implementation that simulates LLM enrichment.
        In a real implementation, you would connect to OpenAI, Anthropic, or another LLM service.
        """
        # Simulate LLM processing delay
        import asyncio
        await asyncio.sleep(0.1)
        
        # Generate mock enrichments based on note content
        content = note.content.lower()
        
        enrichments = LLMEnrichment(
            summary=f"Note contains {len(note.content.split())} words",
            topics=self._extract_topics(content),
            sentiment=self._analyze_sentiment(content),
            key_entities=self._extract_entities(content),
            suggested_tags=self._generate_tags(content),
            complexity_score=self._calculate_complexity(note.content),
            enrichment_timestamp=note.updated_at,
            llm_model="mock-llm-service"
        )
        
        return enrichments
    
    def _extract_topics(self, content: str) -> list:
        """Extract potential topics from note content."""
        topics = []
        if "meeting" in content or "agenda" in content:
            topics.append("meeting")
        if "todo" in content or "task" in content:
            topics.append("task")
        if "idea" in content or "concept" in content:
            topics.append("idea")
        if "project" in content:
            topics.append("project")
        if "research" in content:
            topics.append("research")
        return topics or ["general"]
    
    def _analyze_sentiment(self, content: str) -> str:
        """Analyze the sentiment of the note content."""
        positive_words = ["good", "great", "excellent", "amazing", "wonderful", "love", "happy"]
        negative_words = ["bad", "terrible", "awful", "hate", "sad", "angry", "frustrated"]
        
        positive_count = sum(1 for word in positive_words if word in content)
        negative_count = sum(1 for word in negative_words if word in content)
        
        if positive_count > negative_count:
            return Sentiment.POSITIVE
        elif negative_count > positive_count:
            return Sentiment.NEGATIVE
        else:
            return Sentiment.NEUTRAL
    
    def _extract_entities(self, content: str) -> list:
        """Extract potential entities from note content."""
        entities = []
        words = content.split()
        
        # Simple entity extraction (in real implementation, use NER)
        for word in words:
            if word[0].isupper() and len(word) > 2:
                entities.append(word)
            elif word.startswith("@") or word.startswith("#"):
                entities.append(word)
        
        return list(set(entities))[:5]  # Limit to 5 entities
    
    def _generate_tags(self, content: str) -> list:
        """Generate suggested tags for the note."""
        tags = []
        words = content.split()
        
        # Generate tags based on content patterns
        if any(word in content for word in ["urgent", "important", "priority"]):
            tags.append("priority")
        if any(word in content for word in ["work", "job", "career"]):
            tags.append("work")
        if any(word in content for word in ["personal", "family", "home"]):
            tags.append("personal")
        if any(word in content for word in ["idea", "inspiration", "creative"]):
            tags.append("creative")
        
        return tags
    
    def _calculate_complexity(self, content: str) -> float:
        """Calculate a simple complexity score for the note."""
        words = content.split()
        sentences = content.split('.')
        avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
        avg_sentence_length = len(words) / len(sentences) if sentences else 0
        
        # Simple complexity formula
        complexity = (avg_word_length * 0.3) + (avg_sentence_length * 0.1)
        return round(min(complexity, 10.0), 2)  # Cap at 10.0
