from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Dict, Any
from uuid import UUID
from .dependencies import get_notes_service
from .services.notes_service import NotesService
from .models import Note, NoteCreate, NoteUpdate, UnauthorizedAccessError

router = APIRouter(
    prefix="/notes",
    tags=["notes"],
    responses={404: {"description": "Note not found"}},
)




@router.post("/", response_model=Note, status_code=201)
async def create_note(
    note_data: NoteCreate,
    notes_service: NotesService = Depends(get_notes_service)
) -> Note:
    """Create and store a new note."""
    note = await notes_service.create_note(note_data)
    return note

@router.get("/", response_model=List[Note])
async def get_notes(
    user_id: str = Query(..., description="User ID to fetch notes for"),
    notes_service: NotesService = Depends(get_notes_service)
) -> List[Note]:
    """Retrieve all notes belonging to a specific user."""
    if user_id == "":
        notes = []
        return notes
    notes = await notes_service.get_notes_by_user(user_id)
    return notes

@router.get("/{note_id}", response_model=Note)
async def get_note(
    note_id: UUID,
    user_id: str = Query(..., description="User ID to verify ownership"),
    notes_service: NotesService = Depends(get_notes_service)
) -> Note | None:
    """Retrieve a single note by ID."""
    try:
        note = await notes_service.get_note_by_id(note_id, user_id)
        if not note:
            raise HTTPException(status_code=404, detail="Note not found")
        return note
    except UnauthorizedAccessError:
        raise HTTPException(status_code=403, detail="Access denied: Note does not belong to this user")
    except HTTPException as e:
        raise e


@router.patch("/{note_id}/enrich", response_model=Note)
async def enrich_note_with_llm(
    note_id: UUID,
    user_id: str = Query(..., description="User ID to verify ownership"),
    notes_service: NotesService = Depends(get_notes_service)
) -> Note:
    """Update a note with LLM-generated enrichments stored in metadata."""
    try:
        note = await notes_service.update_note_with_llm_enrichments(note_id, user_id)
        if not note:
            raise HTTPException(status_code=404, detail="Note not found")
        return note
    except UnauthorizedAccessError:
        raise HTTPException(status_code=403, detail="Access denied: Note does not belong to this user")
    except HTTPException as e:
        raise e

@router.patch("/{note_id}", response_model=Note)
async def update_note(
    note_id: UUID,
    note_update: NoteUpdate,
    user_id: str = Query(..., description="User ID to verify ownership"),
    notes_service: NotesService = Depends(get_notes_service)
) -> Note:
    """Update a note's content and/or metadata."""
    try:
        note = await notes_service.update_note_content(note_id, user_id, note_update)
        if not note:
            raise HTTPException(status_code=404, detail="Note not found")
        return note
    except UnauthorizedAccessError:
        raise HTTPException(status_code=403, detail="Access denied: Note does not belong to this user")
    except HTTPException as e:
        raise e 
        
@router.delete("/{note_id}", status_code=204)
async def delete_note(
    note_id: UUID,
    user_id: str = Query(..., description="User ID to verify ownership"),
    notes_service: NotesService = Depends(get_notes_service)
) -> None:
    """Delete a note."""
    try:
        success = await notes_service.delete_note(note_id, user_id)
        if not success:
            raise HTTPException(status_code=404, detail="Note not found")
        return None
    except UnauthorizedAccessError:
        raise HTTPException(status_code=403, detail="Access denied: Note does not belong to this user")
    except HTTPException as e:
        raise e 
        
@router.get("/stats/info")
async def get_service_stats(
    notes_service: NotesService = Depends(get_notes_service)
) -> Dict[str, Any]:
    """Get statistics about the notes service."""
    return notes_service.get_stats()
