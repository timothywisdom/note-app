"use client";

import { useState } from "react";
import { ChevronDown, User } from "lucide-react";

interface UserSelectorProps {
  currentUserId: string;
  onUserIdChange: (userId: string) => void;
}

const PRESET_USERS = [
  "user123",
  "Tim",
  "Ankush",
  "Tibo",
  "developer",
  "tester",
  "demo_user",
];

export default function UserSelector({
  currentUserId,
  onUserIdChange,
}: UserSelectorProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [customUserId, setCustomUserId] = useState("");

  const handleUserSelect = (userId: string) => {
    onUserIdChange(userId);
    setIsOpen(false);
  };

  const handleCustomUserSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (customUserId.trim()) {
      onUserIdChange(customUserId.trim());
      setCustomUserId("");
      setIsOpen(false);
    }
  };

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
      >
        <User className="h-4 w-4 mr-2" />
        {currentUserId}
        <ChevronDown className="h-4 w-4 ml-2" />
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-56 bg-white rounded-md shadow-lg border border-gray-200 z-50">
          <div className="py-1">
            <div className="px-4 py-2 text-xs font-semibold text-gray-500 uppercase tracking-wide border-b border-gray-100">
              Preset Users
            </div>

            {PRESET_USERS.map((userId) => (
              <button
                key={userId}
                onClick={() => handleUserSelect(userId)}
                className={`block w-full text-left px-4 py-2 text-sm hover:bg-gray-100 ${
                  currentUserId === userId
                    ? "bg-blue-50 text-blue-700"
                    : "text-gray-700"
                }`}
              >
                {userId}
              </button>
            ))}

            <div className="px-4 py-2 text-xs font-semibold text-gray-500 uppercase tracking-wide border-t border-gray-100 mt-2">
              Custom User ID
            </div>

            <form onSubmit={handleCustomUserSubmit} className="px-4 py-2">
              <input
                type="text"
                value={customUserId}
                onChange={(e) => setCustomUserId(e.target.value)}
                placeholder="Enter custom user ID"
                className="w-full px-3 py-2 text-sm border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              />
              <button
                type="submit"
                disabled={!customUserId.trim()}
                className="mt-2 w-full px-3 py-1 text-xs bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                Set Custom User
              </button>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
