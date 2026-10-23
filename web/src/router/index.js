/**
 * Rutas web y guardas de navegación (invitado vs autenticado).
 */
import { createRouter, createWebHistory } from 'vue-router';
import BaseLayout from '../components/layout/BaseLayout.vue';
import HomeView from '../views/HomeView.vue';
import Sesion from '../components/Pages/Sesion.vue';
import Formulario from '../components/Pages/Formulario.vue';
import TutoresView from '../views/TutoresView.vue';
import MateriasView from '../views/MateriasView.vue';
import ChatbotView from '../views/ChatbotView.vue';
import TutoriasView from '../views/TutoriasView.vue';
import DashboardView from '../views/DashboardView.vue';
import { useAuthStore } from '@/stores/auth';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: BaseLayout,
      children: [
        {
          path: '',
          name: 'home',
          component: HomeView,
        },
        {
          path: 'sesion',
          name: 'sesion',
          component: Sesion,
          meta: { guestOnly: true },
        },
        {
          path: 'formulario',
          name: 'formulario',
          component: Formulario,
          meta: { guestOnly: true },
        },
        {
          path: 'tutores',
          name: 'tutores',
          component: TutoresView,
        },
        {
          path: 'materias',
          name: 'materias',
          component: MateriasView,
        },
        {
          path: 'chatbot',
          name: 'chatbot',
          component: ChatbotView,
        },
        {
          path: 'tutorias',
          name: 'tutorias',
          component: TutoriasView,
          meta: { requiresAuth: true },
        },
        {
          path: 'dashboard',
          name: 'dashboard',
          component: DashboardView,
          meta: { requiresAdmin: true },
        },
      ],
    },
  ],
});

router.beforeEach((to) => {
  const auth = useAuthStore();
  // Rutas protegidas: redirige a login con return URL.
  if (to.meta.requiresAuth && !auth.isAuthenticated) {
    return { name: 'sesion', query: { redirect: to.fullPath } };
  }
  if (to.meta.requiresAdmin && !auth.isAuthenticated) {
    return { name: 'sesion', query: { redirect: to.fullPath } };
  }
  if (to.meta.requiresAdmin && auth.user?.role !== 'admin') {
    return { name: 'home' };
  }
  // Sesión/registro solo para usuarios no autenticados.
  if (to.meta.guestOnly && auth.isAuthenticated) {
    return { name: 'home' };
  }
  return true;
});

export default router;
