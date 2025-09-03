from enum import StrEnum

class Sentiment(StrEnum):
    """Enumeration of possible sentiment values."""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"

class GeminiModel(StrEnum):
    """Available Gemini model names."""
    FLASH = "gemini-2.5-flash"
    PRO = "gemini-2.5-pro"
    FLASH_LITE = "gemini-2.5-flash-lite"
