from typing import List, Optional, Dict, Any
from datetime import datetime, timezone
from uuid import UUID
from ..models import Note, NoteCreate, NoteUpdate, UnauthorizedAccessError
from ..interfaces import LLMServiceProtocol

class NotesService:
    """Singleton Service class for managing notes operations."""
    
    _instance = None
    _notes: Dict[UUID, Note] = {}
    
    def __new__(cls, llm_service: LLMServiceProtocol):
        """Create a new singleton instance of the NotesService class."""
        if cls._instance is None:
            cls._instance = super(NotesService, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
    
    def __init__(self, llm_service: LLMServiceProtocol):
        """Initialize the notes service with an LLM service."""
        if not hasattr(self, '_initialized') or not self._initialized:
            self.llm_service = llm_service
            self._initialized = True
    
    async def create_note(self, note_data: NoteCreate) -> Note:
        """Create and store a new note."""
        note = Note(
            content=note_data.content,
            user_id=note_data.user_id
        )
        
        self._notes[note.id] = note
        return note
    
    async def get_notes_by_user(self, user_id: str) -> List[Note]:
        """Retrieve all notes belonging to a specific user."""
        user_notes = [
            note for note in self._notes.values() 
            if note.user_id == user_id
        ]
        # Sort by creation date, newest first
        return sorted(user_notes, key=lambda x: x.created_at, reverse=True)
    
    async def get_note_by_id(self, note_id: UUID, user_id: str) -> Optional[Note]:
        """Retrieve a single note by ID, ensuring it belongs to the user."""
        note = self._notes.get(note_id)
        if not note:
            return None
        if note.user_id != user_id:
            raise UnauthorizedAccessError(f"Note {note_id} does not belong to user {user_id}")
        return note
    
    async def update_note_with_llm_enrichments(self, note_id: UUID, user_id: str) -> Optional[Note]:
        """Update a note with LLM-generated enrichments."""
        note = await self.get_note_by_id(note_id, user_id)
        if not note:
            return None
        
        # Generate enrichments using LLM service
        enrichments = await self.llm_service.generate_enrichments(note)
        
        # Update the note's metadata with enrichments
        # Convert Pydantic model to dict for storage
        note.metadata.update(enrichments.model_dump())
        
        # Update the stored note
        self._notes[note_id] = note
        
        return note
    
    async def update_note_content(self, note_id: UUID, user_id: str, note_update: NoteUpdate) -> Optional[Note]:
        """Update a note's content and/or metadata."""
        note = await self.get_note_by_id(note_id, user_id)
        if not note:
            return None
        
        content_changed = False
        
        # Update content if provided
        if note_update.content is not None and note_update.content != note.content:
            note.content = note_update.content
            content_changed = True
        
        # Update metadata if provided
        if note_update.metadata is not None:
            note.metadata.update(note_update.metadata)
        
        # Only update timestamp if content actually changed
        if content_changed:
            note.updated_at = datetime.now(timezone.utc)
        
        # Update the stored note
        self._notes[note_id] = note
        
        return note
    
    async def delete_note(self, note_id: UUID, user_id: str) -> bool:
        """Delete a note, ensuring it belongs to the user."""
        note = await self.get_note_by_id(note_id, user_id)
        if note:
            del self._notes[note_id]
            return True
        return False
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics about the notes service."""
        total_notes = len(self._notes)
        unique_users = len(set(note.user_id for note in self._notes.values()))
        
        return {
            "total_notes": total_notes,
            "unique_users": unique_users,
            "storage_type": "in_memory"
        }
