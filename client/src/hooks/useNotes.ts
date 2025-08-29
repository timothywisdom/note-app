import { useState, useEffect, useCallback } from "react";
import { Note, NoteCreate, NoteUpdate } from "@/types/notes";
import { notesApi } from "@/lib/api";
import { useUser } from "@/contexts/UserContext";

export const useNotes = () => {
  const { currentUserId } = useUser();
  const [notes, setNotes] = useState<Note[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Fetch all notes for the current user
  const fetchNotes = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);
      const fetchedNotes = await notesApi.getNotes(currentUserId);
      setNotes(fetchedNotes);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to fetch notes");
    } finally {
      setLoading(false);
    }
  }, [currentUserId]);

  // Create a new note
  const createNote = useCallback(async (noteData: NoteCreate) => {
    try {
      setLoading(true);
      setError(null);
      const newNote = await notesApi.createNote(noteData);
      setNotes((prev) => [newNote, ...prev]);
      return newNote;
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to create note");
      throw err;
    } finally {
      setLoading(false);
    }
  }, []);

  // Enrich a note with AI
  const enrichNote = useCallback(
    async (noteId: string) => {
      try {
        setLoading(true);
        setError(null);
        const enrichedNote = await notesApi.enrichNote(noteId, currentUserId);
        setNotes((prev) =>
          prev.map((note) => (note.id === noteId ? enrichedNote : note))
        );
        return enrichedNote;
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to enrich note");
        throw err;
      } finally {
        setLoading(false);
      }
    },
    [currentUserId]
  );

  // Update a note
  const updateNote = useCallback(
    async (noteId: string, updates: NoteUpdate) => {
      try {
        setLoading(true);
        setError(null);
        const updatedNote = await notesApi.updateNote(
          noteId,
          currentUserId,
          updates
        );
        setNotes((prev) =>
          prev.map((note) => (note.id === noteId ? updatedNote : note))
        );
        return updatedNote;
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to update note");
        throw err;
      } finally {
        setLoading(false);
      }
    },
    [currentUserId]
  );

  // Delete a note
  const deleteNote = useCallback(
    async (noteId: string) => {
      try {
        setLoading(true);
        setError(null);
        await notesApi.deleteNote(noteId, currentUserId);
        setNotes((prev) => prev.filter((note) => note.id !== noteId));
      } catch (err) {
        setError(err instanceof Error ? err.message : "Failed to delete note");
        throw err;
      } finally {
        setLoading(false);
      }
    },
    [currentUserId]
  );

  // Load notes on mount and when user changes
  useEffect(() => {
    fetchNotes();
  }, [fetchNotes]);

  return {
    notes,
    loading,
    error,
    createNote,
    enrichNote,
    updateNote,
    deleteNote,
    fetchNotes,
  };
};
