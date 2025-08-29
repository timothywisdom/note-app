"use client";

import { useState } from "react";
import { Sparkles, Trash2, Edit3, Calendar, User } from "lucide-react";
import { Note } from "@/types/notes";
import TimestampDisplay from "./TimestampDisplay";

interface NoteCardProps {
  note: Note;
  onEnrich: () => Promise<void>;
  onDelete: () => void;
  onUpdate: (noteId: string, content: string) => void;
}

export default function NoteCard({
  note,
  onEnrich,
  onDelete,
  onUpdate,
}: NoteCardProps) {
  const [isEditing, setIsEditing] = useState(false);
  const [editContent, setEditContent] = useState(note.content);
  const [isEnriching, setIsEnriching] = useState(false);

  const handleSave = () => {
    if (editContent.trim() && editContent !== note.content) {
      onUpdate(note.id, editContent);
      // Don't update originalContent here - wait for the note prop to update
    }
    setIsEditing(false);
  };

  const handleCancel = () => {
    setEditContent(note.content); // Reset to original content
    setIsEditing(false);
  };

  const handleEnrich = async () => {
    setIsEnriching(true);
    try {
      await onEnrich();
    } finally {
      setIsEnriching(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md border border-gray-200 hover:shadow-lg transition-shadow">
      <div className="p-6">
        {/* Header */}
        <div className="flex justify-between items-start mb-4">
          <div className="flex-1 min-w-0">
            <div className="flex items-center text-sm text-gray-500 space-x-4">
              <div className="flex items-center flex-shrink-0">
                <User className="h-4 w-4 mr-1" />
                {note.user_id}
              </div>
              <div className="flex items-center flex-1 min-w-0">
                <Calendar className="h-4 w-4 mr-1 flex-shrink-0" />
                <TimestampDisplay timestamp={note.updated_at} />
              </div>
            </div>
          </div>
          <div className="flex space-x-2 flex-shrink-0 ml-4">
            <button
              onClick={() => setIsEditing(!isEditing)}
              className="p-2 text-gray-400 hover:text-gray-600 rounded-md hover:bg-gray-100"
              title="Edit"
            >
              <Edit3 className="h-4 w-4" />
            </button>
            <button
              onClick={onDelete}
              className="p-2 text-red-400 hover:text-red-600 rounded-md hover:bg-red-50"
              title="Delete"
            >
              <Trash2 className="h-4 w-4" />
            </button>
          </div>
        </div>

        {/* Content */}
        {isEditing ? (
          <div className="mb-4">
            <textarea
              value={editContent}
              onChange={(e) => setEditContent(e.target.value)}
              rows={4}
              className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500"
            />
            <div className="flex justify-end space-x-2 mt-2">
              <button
                onClick={handleCancel}
                className="px-3 py-1 text-sm text-gray-600 hover:text-gray-800"
              >
                Cancel
              </button>
              <button
                onClick={handleSave}
                className="px-3 py-1 text-sm text-blue-600 hover:text-blue-800 font-medium"
              >
                Save
              </button>
            </div>
          </div>
        ) : (
          <div className="mb-4">
            <p
              className="text-gray-700 whitespace-pre-wrap cursor-pointer hover:bg-gray-50 p-2 rounded-md transition-colors"
              onClick={() => setIsEditing(true)}
            >
              {note.content}
            </p>
          </div>
        )}

        {/* AI Enrichment Section */}
        {note.metadata && Object.keys(note.metadata).length > 0 && (
          <div className="border-t border-gray-200 pt-4 mb-4">
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center">
                <Sparkles className="h-4 w-4 text-purple-500 mr-2" />
                <span className="text-sm font-medium text-gray-700">
                  AI Enrichments
                </span>
              </div>
              <TimestampDisplay
                timestamp={
                  note.metadata.enrichment_timestamp || note.updated_at
                }
              />
            </div>

            <div className="space-y-3">
              {note.metadata.summary && (
                <div>
                  <span className="text-xs font-medium text-gray-500 uppercase tracking-wide">
                    Summary
                  </span>
                  <p className="text-sm text-gray-700 mt-1">
                    {note.metadata.summary}
                  </p>
                </div>
              )}

              {note.metadata.topics && note.metadata.topics.length > 0 && (
                <div>
                  <span className="text-xs font-medium text-gray-500 uppercase tracking-wide">
                    Topics
                  </span>
                  <div className="flex flex-wrap gap-2 mt-1">
                    {note.metadata.topics.map((topic, index) => (
                      <span
                        key={index}
                        className="px-2 py-1 text-xs bg-blue-100 text-blue-800 rounded-full"
                      >
                        {topic}
                      </span>
                    ))}
                  </div>
                </div>
              )}

              {note.metadata.suggested_tags &&
                note.metadata.suggested_tags.length > 0 && (
                  <div>
                    <span className="text-xs font-medium text-gray-500 uppercase tracking-wide">
                      Tags
                    </span>
                    <div className="flex flex-wrap gap-2 mt-1">
                      {note.metadata.suggested_tags.map((tag, index) => (
                        <span
                          key={index}
                          className="px-2 py-1 text-xs bg-green-100 text-green-800 rounded-full"
                        >
                          {tag}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

              {note.metadata.sentiment && (
                <div>
                  <span className="text-xs font-medium text-gray-500 uppercase tracking-wide">
                    Sentiment
                  </span>
                  <span
                    className={`ml-2 px-2 py-1 text-xs rounded-full ${
                      note.metadata.sentiment === "positive"
                        ? "bg-green-100 text-green-800"
                        : note.metadata.sentiment === "negative"
                        ? "bg-red-100 text-red-800"
                        : "bg-gray-100 text-gray-800"
                    }`}
                  >
                    {note.metadata.sentiment}
                  </span>
                </div>
              )}

              {note.metadata.key_entities &&
                note.metadata.key_entities.length > 0 && (
                  <div>
                    <span className="text-xs font-medium text-gray-500 uppercase tracking-wide">
                      Key Entities
                    </span>
                    <div className="flex flex-wrap gap-2 mt-1">
                      {note.metadata.key_entities.map((entity, index) => (
                        <span
                          key={index}
                          className="px-2 py-1 text-xs bg-purple-100 text-purple-800 rounded-full"
                        >
                          {entity}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

              {note.metadata.complexity_score && (
                <div>
                  <span className="text-xs font-medium text-gray-500 uppercase tracking-wide">
                    Complexity Score
                  </span>
                  <div className="flex items-center mt-1">
                    <div className="flex-1 bg-gray-200 rounded-full h-2 mr-3">
                      <div
                        className="bg-blue-500 h-2 rounded-full transition-all duration-300"
                        style={{
                          width: `${note.metadata.complexity_score * 100}%`,
                        }}
                      ></div>
                    </div>
                    <span className="text-sm text-gray-700 font-medium">
                      {Math.round(note.metadata.complexity_score * 100)}%
                    </span>
                  </div>
                </div>
              )}
            </div>
          </div>
        )}

        {/* Actions */}
        <div className="flex justify-between items-center pt-4 border-t border-gray-200">
          <button
            onClick={handleEnrich}
            disabled={isEnriching}
            className={`flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors ${
              isEnriching
                ? "text-gray-400 bg-gray-100 cursor-not-allowed"
                : "text-purple-600 bg-purple-50 hover:bg-purple-100"
            }`}
          >
            <Sparkles
              className={`h-4 w-4 mr-2 ${isEnriching ? "animate-pulse" : ""}`}
            />
            {isEnriching ? "Enriching..." : "Enrich with AI"}
          </button>
        </div>
      </div>
    </div>
  );
}
