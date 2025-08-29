"use client";

import React, { createContext, useContext, useState, ReactNode } from "react";

interface UserContextType {
  currentUserId: string;
  setCurrentUserId: (userId: string) => void;
}

const UserContext = createContext<UserContextType | undefined>(undefined);

export const useUser = () => {
  const context = useContext(UserContext);
  if (context === undefined) {
    throw new Error("useUser must be used within a UserProvider");
  }
  return context;
};

interface UserProviderProps {
  children: ReactNode;
}

export const UserProvider: React.FC<UserProviderProps> = ({ children }) => {
  const [currentUserId, setCurrentUserId] = useState<string>("user123"); // Default user for demo

  return (
    <UserContext.Provider value={{ currentUserId, setCurrentUserId }}>
      {children}
    </UserContext.Provider>
  );
};
