import axios from 'axios';

// Configuración base de API para frontend web.
// Se prioriza variable de entorno para facilitar despliegues por ambiente.
const baseURL =
  import.meta.env.VITE_API_URL?.replace(/\/$/, '') || 'http://127.0.0.1:8000/api';

const ACCESS_KEY = 'tutoudec_access';
const REFRESH_KEY = 'tutoudec_refresh';

export const api = axios.create({
  baseURL,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
    Accept: 'application/json',
  },
});

api.interceptors.request.use((config) => {
  // Regla de autenticación: si existe access token, se adjunta en cada request.
  const token = localStorage.getItem(ACCESS_KEY);
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (res) => res,
  async (error) => {
    // Manejo de error relevante: ante 401 se intenta refresh automático
    // una sola vez para evitar bucles infinitos.
    const original = error.config;
    if (error.response?.status === 401 && original && !original._retry) {
      original._retry = true;
      const refresh = localStorage.getItem(REFRESH_KEY);
      if (refresh) {
        try {
          // Se usa axios base para evitar recursión del mismo interceptor.
          const { data } = await axios.post(`${baseURL}/auth/refresh/`, {
            refresh,
          });
          localStorage.setItem(ACCESS_KEY, data.access);
          original.headers.Authorization = `Bearer ${data.access}`;
          return api(original);
        } catch {
          // Si falla refresh, se limpia sesión local y se propaga error.
          localStorage.removeItem(ACCESS_KEY);
          localStorage.removeItem(REFRESH_KEY);
        }
      }
    }
    return Promise.reject(error);
  }
);

export function setTokens(access, refresh) {
  if (access) localStorage.setItem(ACCESS_KEY, access);
  if (refresh) localStorage.setItem(REFRESH_KEY, refresh);
}

export function clearTokens() {
  localStorage.removeItem(ACCESS_KEY);
  localStorage.removeItem(REFRESH_KEY);
}

export const authApi = {
  // Endpoints de identidad: login, alta de usuario, perfil y refresh.
  login: (body) => api.post('/auth/login/', body),
  register: (body) => api.post('/auth/register/', body),
  profile: () => api.get('/auth/profile/'),
  refresh: (refresh) => api.post('/auth/refresh/', { refresh }),
};

export const tutoresApi = {
  // Endpoints de tutores para listados, detalle y métricas.
  list: (params) => api.get('/tutores/', { params }),
  get: (id) => api.get(`/tutores/${id}/`),
  estadisticas: (id) => api.get(`/tutores/${id}/estadisticas/`),
  tutorias: (id, params) =>
    api.get(`/tutores/${id}/tutorias/`, { params }),
};

export const materiasApi = {
  // Endpoints de materias y tutores asociados.
  list: (params) => api.get('/materias/', { params }),
  get: (id) => api.get(`/materias/${id}/`),
  tutores: (id) => api.get(`/materias/${id}/tutores/`),
};

export const tutoriasApi = {
  // Endpoints de ciclo de vida de tutorías (crear, confirmar, cancelar, etc.).
  list: (params) => api.get('/tutorias/', { params }),
  get: (id) => api.get(`/tutorias/${id}/`),
  misTutorias: (params) =>
    api.get('/tutorias/mis_tutorias/', { params }),
  create: (body) => api.post('/tutorias/', body),
  confirmar: (id) => api.post(`/tutorias/${id}/confirmar/`),
  cancelar: (id) => api.post(`/tutorias/${id}/cancelar/`),
};

export const dashboardApi = {
  resumen: () => api.get('/dashboard/resumen/'),
};

export { ACCESS_KEY, REFRESH_KEY };
