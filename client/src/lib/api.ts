import axios from "axios";
import { Note, NoteCreate, NoteUpdate } from "@/types/notes";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export const notesApi = {
  // Create a new note
  createNote: async (noteData: NoteCreate): Promise<Note> => {
    const response = await api.post("/notes", noteData);
    return response.data;
  },

  // Get all notes for a user
  getNotes: async (userId: string): Promise<Note[]> => {
    const response = await api.get(`/notes?user_id=${userId}`);
    return response.data;
  },

  // Get a single note by ID
  getNote: async (noteId: string, userId: string): Promise<Note> => {
    const response = await api.get(`/notes/${noteId}?user_id=${userId}`);
    return response.data;
  },

  // Update a note with LLM enrichments
  enrichNote: async (noteId: string, userId: string): Promise<Note> => {
    const response = await api.patch(
      `/notes/${noteId}/enrich?user_id=${userId}`
    );
    return response.data;
  },

  // Update note content
  updateNote: async (
    noteId: string,
    userId: string,
    updates: NoteUpdate
  ): Promise<Note> => {
    const response = await api.patch(
      `/notes/${noteId}?user_id=${userId}`,
      updates
    );
    return response.data;
  },

  // Delete a note
  deleteNote: async (noteId: string, userId: string): Promise<boolean> => {
    const response = await api.delete(`/notes/${noteId}?user_id=${userId}`);
    return response.data;
  },
};

export default api;
