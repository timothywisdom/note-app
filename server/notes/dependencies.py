import os
from fastapi import Depends
import google.generativeai as genai
from .services.llm_stub_service import LLMStubService
from .services.gemini_service import GeminiService
from .services.notes_service import NotesService
from .interfaces import LLMServiceProtocol
from .models.enums import GeminiModel

def get_gemini_api_key() -> str:
    """Dependency function that provides a Gemini API key."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError(
            "GEMINI_API_KEY environment variable is required. "
            "Please set it in your .env file or environment variables."
        )
    return api_key

def get_gemini_model(api_key: str = Depends(get_gemini_api_key)) -> genai.GenerativeModel:
    """Dependency function that provides a configured Gemini model."""
    genai.configure(api_key=api_key)
    model_name = GeminiModel.FLASH
    return genai.GenerativeModel(model_name)

def get_gemini_service(gemini_model: genai.GenerativeModel = Depends(get_gemini_model)) -> GeminiService:
    """Dependency function that provides a GeminiService instance."""
    return GeminiService(gemini_model=gemini_model)

def get_llm_stub_service() -> LLMStubService:
    """Dependency function that provides an LLMStubService instance."""
    return LLMStubService()

def get_notes_service(llm_service: LLMServiceProtocol = Depends(get_gemini_service)) -> NotesService:
    """Dependency function that provides a NotesService instance."""
    return NotesService(llm_service)
