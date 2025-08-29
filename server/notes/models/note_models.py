from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from datetime import datetime, timezone
from uuid import UUID, uuid4

class NoteBase(BaseModel):
    """Base model for note data."""
    content: str = Field(..., description="The content of the note")
    user_id: str = Field(..., description="The user ID of the note's owner")

class NoteCreate(NoteBase):
    """Model for creating a new note."""
    pass

class NoteUpdate(BaseModel):
    """Model for updating a note."""
    content: Optional[str] = Field(None, description="The updated content of the note")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Updated metadata for the note")

class Note(NoteBase):
    """Complete note model with all fields."""
    id: UUID = Field(default_factory=uuid4, description="Unique identifier for the note")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Timestamp of note creation")
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), description="Timestamp of last revision")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="JSON metadata field for anything")
    
    def __init__(self, **data):
        super().__init__(**data)
        # Ensure updated_at is exactly the same as created_at for new notes
        if 'updated_at' not in data:
            # If no updated_at provided, use the same timestamp as created_at
            self.updated_at = self.created_at

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
            UUID: lambda v: str(v)
        }
