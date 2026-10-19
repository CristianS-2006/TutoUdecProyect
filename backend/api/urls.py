from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TutorViewSet, MateriaViewSet, TutoriaViewSet,
    DisponibilidadViewSet, ResenaViewSet, UserAdminViewSet,
    AuthViewSet, ChatbotViewSet, GrupoTutoriaViewSet, InscripcionGrupoViewSet,
    DashboardViewSet
)

router = DefaultRouter()
router.register(r'tutores', TutorViewSet)
router.register(r'materias', MateriaViewSet)
router.register(r'tutorias', TutoriaViewSet)
router.register(r'disponibilidades', DisponibilidadViewSet)
router.register(r'resenas', ResenaViewSet)
router.register(r'usuarios', UserAdminViewSet, basename='usuarios')
router.register(r'auth', AuthViewSet, basename='auth')
router.register(r'chatbot', ChatbotViewSet, basename='chatbot')
router.register(r'grupos', GrupoTutoriaViewSet, basename='grupos')
router.register(r'inscripciones', InscripcionGrupoViewSet, basename='inscripciones')
router.register(r'dashboard', DashboardViewSet, basename='dashboard')

urlpatterns = [
    path('', include(router.urls)),
]