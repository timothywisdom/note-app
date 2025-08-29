from enum import Enum

class Sentiment(str, Enum):
    """Enumeration of possible sentiment values."""
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
