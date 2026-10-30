import React, { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import { api, clearToken, getToken, saveToken } from "../api/client.js";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(Boolean(getToken()));
  const [authError, setAuthError] = useState("");

  const refreshUser = useCallback(async () => {
    const profile = await api.me();
    setUser(profile);
    return profile;
  }, []);

  useEffect(() => {
    if (!getToken()) return;
    refreshUser()
      .catch((error) => {
        if (error.status === 401) clearToken();
        setUser(null);
        setAuthError(error.message);
      })
      .finally(() => setLoading(false));
  }, [refreshUser]);

  const login = useCallback(async (email, password) => {
    const result = await api.login(email, password);
    saveToken(result.access_token);
    try {
      await refreshUser();
      setAuthError("");
    } catch (error) {
      clearToken();
      throw error;
    }
  }, [refreshUser]);

  const register = useCallback(async (data) => {
    await api.register(data);
    await login(data.email, data.password);
  }, [login]);

  const logout = useCallback(() => {
    clearToken();
    setUser(null);
    setAuthError("");
  }, []);

  const value = useMemo(
    () => ({ user, loading, authError, login, register, logout, refreshUser, setUser }),
    [user, loading, authError, login, register, logout, refreshUser],
  );
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth phải được sử dụng bên trong AuthProvider.");
  return context;
}
