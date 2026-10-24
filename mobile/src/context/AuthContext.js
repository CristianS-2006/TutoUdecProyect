/**
 * Contexto de sesión móvil: login/registro contra la API, tokens en AsyncStorage,
 * rol de app (tutor/estudiante) para elegir pantalla de inicio.
 */
import React, { createContext, useState, useContext, useEffect } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import api from '../services/api';
import { getApiBaseUrl } from '../config';

const AuthContext = createContext({});

const ROLE_KEY = '@TutoUdec:role';

/** Normaliza errores DRF/red a mensaje legible en Alert. */
function formatApiError(error, fallback) {
  if (error.response?.data) {
    const d = error.response.data;
    if (typeof d === 'string') return d;
    if (d.detail) return Array.isArray(d.detail) ? d.detail.join(' ') : String(d.detail);
    return Object.entries(d)
      .map(([k, v]) => {
        const msg = Array.isArray(v) ? v.join(', ') : String(v);
        return `${k}: ${msg}`;
      })
      .join('\n');
  }
  if (error.code === 'ECONNABORTED') {
    return 'Tiempo de espera agotado. ¿El backend está en marcha y la IP es correcta?';
  }
  if (error.message === 'Network Error') {
    return `Sin conexión al servidor. API: ${getApiBaseUrl()}`;
  }
  return error.message || fallback;
}

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [token, setToken] = useState(null);
  const [appRole, setAppRole] = useState('estudiante');

  useEffect(() => {
    loadStoredData();
  }, []);

  const loadStoredData = async () => {
    try {
      const storedToken = await AsyncStorage.getItem('@TutoUdec:token');
      const storedUser = await AsyncStorage.getItem('@TutoUdec:user');
      const storedRole = await AsyncStorage.getItem(ROLE_KEY);

      if (storedRole === 'tutor' || storedRole === 'estudiante') {
        setAppRole(storedRole);
      }

      if (storedToken && storedUser) {
        setToken(storedToken);
        setUser(JSON.parse(storedUser));
        api.defaults.headers.common.Authorization = `Bearer ${storedToken}`;
      }
    } catch (error) {
      console.error('Error loading stored data:', error);
    } finally {
      setLoading(false);
    }
  };

  /** @param {string} identifier - usuario o correo (el backend acepta ambos) */
  const signIn = async (identifier, password) => {
    try {
      const response = await api.post('/auth/login/', {
        username: identifier.trim(),
        password,
      });

      const { access, refresh, user: userData } = response.data;
      const role = userData.role || 'estudiante';

      await AsyncStorage.setItem('@TutoUdec:token', access);
      await AsyncStorage.setItem('@TutoUdec:refreshToken', refresh);
      await AsyncStorage.setItem('@TutoUdec:user', JSON.stringify(userData));
      await AsyncStorage.setItem(ROLE_KEY, role);

      setToken(access);
      setUser(userData);
      setAppRole(role);
      api.defaults.headers.common.Authorization = `Bearer ${access}`;

      return { success: true };
    } catch (error) {
      return {
        success: false,
        error: formatApiError(error, 'Error al iniciar sesión'),
      };
    }
  };

  const signUp = async (userData, options = {}) => {
    try {
      const role = options.appRole === 'tutor' ? 'tutor' : 'estudiante';
      const response = await api.post('/auth/register/', {
        ...userData,
        role,
      });
      const { access, refresh, user: newUser } = response.data;

      await AsyncStorage.setItem('@TutoUdec:token', access);
      await AsyncStorage.setItem('@TutoUdec:refreshToken', refresh);
      await AsyncStorage.setItem('@TutoUdec:user', JSON.stringify(newUser));

      await AsyncStorage.setItem(ROLE_KEY, role);
      setAppRole(role);

      setToken(access);
      setUser(newUser);
      api.defaults.headers.common.Authorization = `Bearer ${access}`;

      return { success: true };
    } catch (error) {
      return {
        success: false,
        error: formatApiError(error, 'Error al registrarse'),
      };
    }
  };

  const signOut = async () => {
    await AsyncStorage.multiRemove([
      '@TutoUdec:token',
      '@TutoUdec:refreshToken',
      '@TutoUdec:user',
      ROLE_KEY,
    ]);
    setToken(null);
    setUser(null);
    setAppRole('estudiante');
    delete api.defaults.headers.common.Authorization;
  };

  return (
    <AuthContext.Provider
      value={{
        signed: !!user,
        user,
        token,
        appRole,
        loading,
        signIn,
        signUp,
        signOut,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
