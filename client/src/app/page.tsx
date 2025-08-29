"use client";

import { useState } from "react";
import { Plus } from "lucide-react";
import { useNotes } from "@/hooks/useNotes";
import { useUser } from "@/contexts/UserContext";
import { CreateNoteFormData } from "@/types/notes";
import CreateNoteModal from "@/components/CreateNoteModal";
import NoteCard from "@/components/NoteCard";
import UserSelector from "@/components/UserSelector";

export default function Home() {
  const { currentUserId, setCurrentUserId } = useUser();
  const {
    notes,
    loading,
    error,
    createNote,
    enrichNote,
    deleteNote,
    updateNote,
  } = useNotes();
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);

  const handleCreateNote = async (formData: CreateNoteFormData) => {
    try {
      await createNote({
        content: formData.content,
        user_id: currentUserId,
      });
      setIsCreateModalOpen(false);
    } catch (error) {
      console.error("Failed to create note:", error);
    }
  };

  const handleEnrichNote = async (noteId: string) => {
    try {
      await enrichNote(noteId);
    } catch (error) {
      console.error("Failed to enrich note:", error);
    }
  };

  const handleDeleteNote = async (noteId: string) => {
    if (confirm("Are you sure you want to delete this note?")) {
      try {
        await deleteNote(noteId);
      } catch (error) {
        console.error("Failed to delete note:", error);
      }
    }
  };

  const handleUpdateNote = async (noteId: string, content: string) => {
    try {
      await updateNote(noteId, { content });
    } catch (error) {
      console.error("Failed to update note:", error);
    }
  };

  if (loading && notes.length === 0) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading your notes...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <h1 className="text-2xl font-bold text-gray-900">NoteApp</h1>
              <span className="ml-2 text-sm text-gray-500">
                AI-Powered Notes
              </span>
            </div>
            <div className="flex items-center space-x-4">
              <UserSelector
                currentUserId={currentUserId}
                onUserIdChange={setCurrentUserId}
              />
              <button
                onClick={() => setIsCreateModalOpen(true)}
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                <Plus className="h-4 w-4 mr-2" />
                New Note
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {error && (
          <div className="mb-6 bg-red-50 border border-red-200 rounded-md p-4">
            <div className="flex">
              <div className="text-red-400">
                <svg
                  className="h-5 w-5"
                  viewBox="0 0 20 20"
                  fill="currentColor"
                >
                  <path
                    fillRule="evenodd"
                    d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                    clipRule="evenodd"
                  />
                </svg>
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-red-800">Error</h3>
                <p className="mt-1 text-sm text-red-700">{error}</p>
              </div>
            </div>
          </div>
        )}

        {notes.length === 0 ? (
          <div className="text-center py-12">
            <div className="mx-auto h-12 w-12 text-gray-400">
              <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                />
              </svg>
            </div>
            <h3 className="mt-2 text-sm font-medium text-gray-900">No notes</h3>
            <p className="mt-1 text-sm text-gray-500">
              Get started by creating a new note.
            </p>
            <div className="mt-6">
              <button
                onClick={() => setIsCreateModalOpen(true)}
                className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
              >
                <Plus className="h-4 w-4 mr-2" />
                New Note
              </button>
            </div>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {notes.map((note) => (
              <NoteCard
                key={note.id}
                note={note}
                onEnrich={async () => await handleEnrichNote(note.id)}
                onDelete={() => handleDeleteNote(note.id)}
                onUpdate={handleUpdateNote}
              />
            ))}
          </div>
        )}
      </main>

      {/* Create Note Modal */}
      <CreateNoteModal
        isOpen={isCreateModalOpen}
        onClose={() => setIsCreateModalOpen(false)}
        onSubmit={handleCreateNote}
      />
    </div>
  );
}
