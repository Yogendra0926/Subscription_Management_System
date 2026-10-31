"use client";
import { createContext, useContext, useMemo, useState } from "react";

const AuthContext = createContext(null);
export function AuthProvider({ children }) {
  const [role, setRole] = useState(null);
  const value = useMemo(() => ({ role, signIn: setRole, signOut: () => setRole(null) }), [role]);
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
export const useAuth = () => useContext(AuthContext);
