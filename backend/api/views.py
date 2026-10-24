from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Avg, Count
from django.db.models.functions import TruncMonth
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import date
from decimal import Decimal
from .models import Tutor, Materia, Tutoria, Disponibilidad, Resena, PasswordResetToken, UserProfile, GrupoTutoria, InscripcionGrupo
from .serializers import (
    TutorSerializer, TutorListSerializer, MateriaSerializer,
    TutoriaSerializer, UserSerializer, DisponibilidadSerializer,
    ResenaSerializer, AdminUserSerializer, GrupoTutoriaSerializer, InscripcionGrupoSerializer
)
from .permissions import IsAdminOrReadOnly

class AuthViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]

    @action(detail=False, methods=['post'])
    def login(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({'detail': 'Se requiere usuario y contraseña'}, status=status.HTTP_400_BAD_REQUEST)

        # Soporte para login por email
        if '@' in username:
            try:
                user_obj = User.objects.get(email=username)
                username = user_obj.username
            except User.DoesNotExist:
                return Response({'detail': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)
        
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': UserSerializer(user).data
            })
        return Response({'detail': 'Credenciales inválidas'}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['post'])
    def register(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        
        if not username or not email or not password:
            return Response(
                {'detail': 'Se requieren username, email y contraseña'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if len(password) < 6:
            return Response(
                {'detail': 'La contraseña debe tener al menos 6 caracteres'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if User.objects.filter(username=username).exists():
            return Response(
                {'detail': 'El nombre de usuario ya existe'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if User.objects.filter(email=email).exists():
            return Response(
                {'detail': 'El correo electrónico ya está registrado'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=request.data.get('first_name', ''),
                last_name=request.data.get('last_name', '')
            )
            
            # Crear perfil de tutor si se solicita
            if request.data.get('role') == 'tutor':
                Tutor.objects.create(
                    usuario=user,
                    especialidad=request.data.get('especialidad', 'General')
                )
                
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': UserSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'detail': f'Error al crear usuario: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def profile(self, request):
        return Response(UserSerializer(request.user).data)

    @action(detail=False, methods=['post'])
    def refresh(self, request):
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response({'detail': 'Se requiere refresh token'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            refresh = RefreshToken(refresh_token)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            })
        except Exception:
            return Response({'detail': 'Token inválido'}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=['post'])
    def request_password_reset(self, request):
        """Solicitar restablecimiento de contraseña por correo o teléfono"""
        identifier = request.data.get('identifier')
        
        if not identifier:
            return Response({'detail': 'Se requiere correo o teléfono'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = None
        
        # Buscar por correo
        if '@' in identifier:
            try:
                user = User.objects.get(email=identifier)
            except User.DoesNotExist:
                pass
        
        # Si no encontró por correo, buscar por teléfono
        if not user:
            try:
                profile = UserProfile.objects.get(phone_number=identifier)
                user = profile.user
            except UserProfile.DoesNotExist:
                pass
        
        if not user:
            return Response(
                {'detail': 'Si existe una cuenta asociada, recibirás las instrucciones'},
                status=status.HTTP_200_OK
            )
        
        # Crear token de restablecimiento
        reset_token = PasswordResetToken.objects.create(user=user)
        
        # Enviar correo (o mostrar en consola para desarrollo)
        try:
            subject = 'Restablecimiento de Contraseña - TutoUdec'
            message = f"""
            Hola {user.first_name or user.username},
            
            Has solicitado restablecer tu contraseña en TutoUdec.
            
            TU TOKEN DE RESTABLECIMIENTO ES: {reset_token.token}
            
            Este token expirará en 1 hora.
            
            Si no solicitaste esto, ignora este correo.
            
            Saludos,
            Equipo TutoUdec
            """
            
            print("\n" + "="*80)
            print("  TOKEN DE RESTABLECIMIENTO GENERADO:")
            print("="*80)
            print(f"  Usuario: {user.username} ({user.email})")
            print(f"  Token: {reset_token.token}")
            print("="*80 + "\n")
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Error sending email: {e}")
            print("\n" + "="*80)
            print("  TOKEN DE RESTABLECIMIENTO GENERADO (CORREO FALLÓ):")
            print("="*80)
            print(f"  Usuario: {user.username} ({user.email})")
            print(f"  Token: {reset_token.token}")
            print("="*80 + "\n")
        
        data = {'detail': 'Si existe una cuenta asociada, recibirás las instrucciones'}
        if getattr(settings, 'PASSWORD_RESET_SHOW_TOKEN', False):
            data['reset_token'] = str(reset_token.token)
        return Response(data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def change_password(self, request):
        """Cambiar contraseña del usuario autenticado"""
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        confirm_password = request.data.get('confirm_password')
        
        if not old_password or not new_password or not confirm_password:
            return Response(
                {'detail': 'Se requiere contraseña actual y nueva contraseña'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if new_password != confirm_password:
            return Response(
                {'detail': 'Las nuevas contraseñas no coinciden'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if len(new_password) < 6:
            return Response(
                {'detail': 'La nueva contraseña debe tener al menos 6 caracteres'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = request.user
        if not user.check_password(old_password):
            return Response(
                {'detail': 'La contraseña actual es incorrecta'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.set_password(new_password)
        user.save()
        
        return Response(
            {'detail': 'Contraseña cambiada exitosamente'},
            status=status.HTTP_200_OK
        )
    
    @action(detail=False, methods=['post'])
    def confirm_password_reset(self, request):
        """Confirmar restablecimiento de contraseña con token"""
        token = request.data.get('token')
        new_password = request.data.get('new_password')
        
        if not token or not new_password:
            return Response(
                {'detail': 'Se requiere token y nueva contraseña'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if len(new_password) < 6:
            return Response(
                {'detail': 'La contraseña debe tener al menos 6 caracteres'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            reset_token = PasswordResetToken.objects.get(token=token)
        except PasswordResetToken.DoesNotExist:
            return Response(
                {'detail': 'Token inválido'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not reset_token.is_valid():
            return Response(
                {'detail': 'Token expirado o ya usado'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Cambiar contraseña
        user = reset_token.user
        user.set_password(new_password)
        user.save()
        
        # Marcar token como usado
        reset_token.used = True
        reset_token.save()
        
        return Response(
            {'detail': 'Contraseña restablecida exitosamente'},
            status=status.HTTP_200_OK
        )


class DashboardViewSet(viewsets.ViewSet):
    permission_classes = [IsAdminUser]

    @action(detail=False, methods=['get'])
    def resumen(self, request):
        hoy = timezone.localdate()
        indice_mes_actual = hoy.year * 12 + hoy.month - 1
        meses = []
        for desplazamiento in reversed(range(6)):
            indice_mes = indice_mes_actual - desplazamiento
            anio, mes_cero_based = divmod(indice_mes, 12)
            meses.append(date(anio, mes_cero_based + 1, 1))

        tutorias_por_mes = {
            item['mes'].strftime('%Y-%m'): item['total']
            for item in Tutoria.objects.filter(
                creado_en__date__gte=meses[0]
            ).annotate(
                mes=TruncMonth('creado_en')
            ).values('mes').annotate(
                total=Count('id')
            ).order_by('mes')
        }
        tutorias_por_estado = dict(
            Tutoria.objects.values_list('estado').annotate(total=Count('id'))
        )
        calificacion_promedio = Tutor.objects.aggregate(
            promedio=Avg('calificacion')
        )['promedio']

        return Response({
            'indicadores': {
                'usuarios': User.objects.count(),
                'tutores': Tutor.objects.count(),
                'materias': Materia.objects.count(),
                'tutorias': Tutoria.objects.count(),
                'calificacion_promedio': round(
                    float(calificacion_promedio or 0), 2
                ),
            },
            'tutorias_por_estado': [
                {
                    'estado': estado,
                    'etiqueta': etiqueta,
                    'total': tutorias_por_estado.get(estado, 0),
                }
                for estado, etiqueta in Tutoria.ESTADOS
            ],
            'tutorias_por_mes': [
                {
                    'mes': mes.strftime('%Y-%m'),
                    'total': tutorias_por_mes.get(mes.strftime('%Y-%m'), 0),
                }
                for mes in meses
            ],
            'tutorias_por_materia': list(
                Materia.objects.annotate(
                    total=Count('tutorias')
                ).filter(tutorias__isnull=False).values(
                    'nombre', 'total'
                ).order_by('-total', 'nombre')[:5]
            ),
            'actualizado_en': timezone.now().isoformat(),
        })


class MateriaViewSet(viewsets.ModelViewSet):
    queryset = Materia.objects.all()
    serializer_class = MateriaSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nombre', 'descripcion']
    ordering_fields = ['nombre', 'creado_en']
    ordering = ['nombre']
    
    @action(detail=True, methods=['get'])
    def tutorias(self, request, pk=None):
        """Obtener todas las tutorías de una materia"""
        materia = self.get_object()
        tutorias = materia.tutorias.all()
        serializer = TutoriaSerializer(tutorias, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def tutores(self, request, pk=None):
        """Obtener todos los tutores de una materia"""
        materia = self.get_object()
        tutores = materia.tutores.filter(disponible=True)
        serializer = TutorListSerializer(tutores, many=True)
        return Response(serializer.data)


class TutorViewSet(viewsets.ModelViewSet):
    queryset = Tutor.objects.select_related('usuario').prefetch_related('materias')
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['nivel_experiencia', 'disponible', 'materias']
    search_fields = ['usuario__username', 'usuario__first_name', 'usuario__last_name', 'especialidad']
    ordering_fields = ['calificacion', 'tarifa_por_hora', 'creado_en']
    ordering = ['-calificacion']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return TutorListSerializer
        return TutorSerializer
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def mi_perfil(self, request):
        """Obtener el perfil de tutor del usuario autenticado"""
        try:
            tutor = Tutor.objects.get(usuario=request.user)
            serializer = self.get_serializer(tutor)
            return Response(serializer.data)
        except Tutor.DoesNotExist:
            return Response(
                {'error': 'No tienes un perfil de tutor'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=True, methods=['get'])
    def tutorias(self, request, pk=None):
        """Obtener todas las tutorías de un tutor"""
        tutor = self.get_object()
        tutorias = tutor.tutorias.all()
        estado = request.query_params.get('estado')
        
        if estado:
            tutorias = tutorias.filter(estado=estado)
        
        serializer = TutoriaSerializer(tutorias, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def estadisticas(self, request, pk=None):
        """Obtener estadísticas de un tutor"""
        tutor = self.get_object()
        tutorias_totales = tutor.tutorias.count()
        tutorias_completadas = tutor.tutorias.filter(estado='completada').count()
        tutorias_pendientes = tutor.tutorias.filter(estado='pendiente').count()
        
        return Response({
            'tutorias_totales': tutorias_totales,
            'tutorias_completadas': tutorias_completadas,
            'tutorias_pendientes': tutorias_pendientes,
            'calificacion_promedio': tutor.calificacion,
            'tarifa_por_hora': str(tutor.tarifa_por_hora),
            'materias': tutor.materias.count(),
        })
    
    @action(detail=True, methods=['post'])
    def marcar_disponible(self, request, pk=None):
        """Marcar tutor como disponible"""
        tutor = self.get_object()
        tutor.disponible = True
        tutor.save()
        return Response({'status': 'Tutor marcado como disponible'})
    
    @action(detail=True, methods=['post'])
    def marcar_no_disponible(self, request, pk=None):
        """Marcar tutor como no disponible"""
        tutor = self.get_object()
        tutor.disponible = False
        tutor.save()
        return Response({'status': 'Tutor marcado como no disponible'})


class TutoriaViewSet(viewsets.ModelViewSet):
    queryset = Tutoria.objects.select_related('tutor', 'estudiante', 'materia').all()
    serializer_class = TutoriaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['estado', 'tutor', 'estudiante', 'materia']
    search_fields = ['estudiante__username', 'tutor__usuario__username', 'materia__nombre']
    ordering_fields = ['fecha_inicio', 'creado_en', 'estado']
    ordering = ['-fecha_inicio']
    
    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return qs
        if hasattr(user, 'perfil_tutor'):
            return qs.filter(tutor=user.perfil_tutor)
        return qs.filter(estudiante=user)

    def update(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({'detail': 'Solo un administrador puede editar tutorias.'}, status=status.HTTP_403_FORBIDDEN)
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({'detail': 'Solo un administrador puede editar tutorias.'}, status=status.HTTP_403_FORBIDDEN)
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not request.user.is_staff:
            return Response({'detail': 'Solo un administrador puede eliminar tutorias.'}, status=status.HTTP_403_FORBIDDEN)
        return super().destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        """Al crear una tutoría, calcular la tarifa y asignar estudiante"""
        # El estudiante autenticado puede registrar su propia tutoría.
        # Si quien crea es admin, puede asignar explícitamente otro estudiante.
        if self.request.user.is_staff and serializer.validated_data.get('estudiante'):
            tutoria = serializer.save()
        else:
            tutoria = serializer.save(estudiante=self.request.user)
        if not tutoria.tarifa and tutoria.tutor.tarifa_por_hora:
            duracion_horas = Decimal(tutoria.duracion_minutos) / Decimal(60)
            tutoria.tarifa = tutoria.tutor.tarifa_por_hora * duracion_horas
            tutoria.save()
    
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def mis_tutorias(self, request):
        """Obtener las tutorías del usuario actual"""
        tutorias = Tutoria.objects.filter(estudiante=request.user)
        estado = request.query_params.get('estado')
        
        if estado:
            tutorias = tutorias.filter(estado=estado)
        
        serializer = self.get_serializer(tutorias, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def mis_tutorias_como_tutor(self, request):
        """Obtener las tutorías del tutor actual (si lo es)"""
        try:
            tutor = Tutor.objects.get(usuario=request.user)
            tutorias = Tutoria.objects.filter(tutor=tutor)
            estado = request.query_params.get('estado')
            if estado:
                tutorias = tutorias.filter(estado=estado)
            serializer = self.get_serializer(tutorias, many=True)
            return Response(serializer.data)
        except Tutor.DoesNotExist:
            return Response({'error': 'No eres un tutor'}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['post'])
    def confirmar(self, request, pk=None):
        """Confirmar una tutoría"""
        tutoria = self.get_object()
        if tutoria.estado != 'pendiente':
            return Response(
                {'error': 'Solo se pueden confirmar tutorías pendientes'},
                status=status.HTTP_400_BAD_REQUEST
            )
        tutoria.estado = 'confirmada'
        tutoria.save()
        serializer = self.get_serializer(tutoria)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def iniciar(self, request, pk=None):
        """Iniciar una tutoría"""
        tutoria = self.get_object()
        if tutoria.estado not in ['pendiente', 'confirmada']:
            return Response(
                {'error': 'La tutoría no puede ser iniciada en este estado'},
                status=status.HTTP_400_BAD_REQUEST
            )
        tutoria.estado = 'en_progreso'
        tutoria.save()
        serializer = self.get_serializer(tutoria)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def completar(self, request, pk=None):
        """Completar una tutoría"""
        tutoria = self.get_object()
        if tutoria.estado != 'en_progreso':
            return Response(
                {'error': 'Solo se pueden completar tutorías en progreso'},
                status=status.HTTP_400_BAD_REQUEST
            )
        tutoria.estado = 'completada'
        tutoria.nota = request.data.get('nota', '')
        tutoria.save()
        serializer = self.get_serializer(tutoria)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def cancelar(self, request, pk=None):
        """Cancelar una tutoría"""
        tutoria = self.get_object()
        if tutoria.estado not in ['pendiente', 'confirmada', 'en_progreso']:
            return Response(
                {'error': 'La tutoría no puede ser cancelada en este estado'},
                status=status.HTTP_400_BAD_REQUEST
            )
        tutoria.estado = 'cancelada'
        tutoria.save()
        serializer = self.get_serializer(tutoria)
        return Response(serializer.data)


class DisponibilidadViewSet(viewsets.ModelViewSet):
    queryset = Disponibilidad.objects.all()
    serializer_class = DisponibilidadSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tutor', 'dia_semana', 'activo']


class ResenaViewSet(viewsets.ModelViewSet):
    queryset = Resena.objects.all()
    serializer_class = ResenaSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['tutor', 'estudiante', 'tutoria']
    ordering_fields = ['creado_en', 'calificacion']
    ordering = ['-creado_en']


class UserAdminViewSet(viewsets.ModelViewSet):
    """
    ViewSet para la gestión de usuarios por parte de administradores.
    """
    queryset = User.objects.all().order_by('id')
    serializer_class = AdminUserSerializer
    permission_classes = [IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering_fields = ['id', 'username', 'date_joined']

    @action(detail=True, methods=['post'])
    def make_admin(self, request, pk=None):
        user = self.get_object()
        user.is_staff = True
        user.save()
        return Response({'status': f'Usuario {user.username} ahora es administrador'})

    @action(detail=True, methods=['post'])
    def remove_admin(self, request, pk=None):
        user = self.get_object()
        user.is_staff = False
        user.save()
        return Response({'status': f'Privilegios de administrador removidos para {user.username}'})


class ChatbotViewSet(viewsets.ViewSet):
    """
    Chatbot de soporte para TutoUdec y la Universidad de Cundinamarca.
    """
    permission_classes = [AllowAny]

    KNOWLEDGE_BASE = {
        'bienvenida': [
            'hola', 'buenos dias', 'buenas tardes', 'buenas noches', 'qué tal', 'ola', 
            'hello', 'hi', 'como estas', 'cómo estás'
        ],
        'universidad': [
            'universidad', 'udec', 'cundinamarca', 'campus', 'facultad', 'sede', 
            'ubicacion', 'ubicación', 'donde esta', 'dónde está', 'direccion'
        ],
        'inscripcion': [
            'inscribirme', 'inscripcion', 'inscripción', 'matricula', 'matrícula', 
            'matricularme', 'cómo inscribirme', 'como inscribirme', 'registrarme', 
            'registro', 'crear cuenta', 'nueva cuenta'
        ],
        'tutorias': [
            'tutoria', 'tutorías', 'tutorias', 'tutor', 'tutores', 'clases particulares', 
            'ayuda academica', 'ayuda académica', 'clase', 'sesion', 'sesión', 
            'agendar', 'reservar', 'pedir tutoria', 'cancelar tutoria', 'cambiar horario'
        ],
        'materias': [
            'materia', 'materias', 'asignatura', 'asignaturas', 'curso', 'cursos', 
            'cálculo', 'algebra', 'física', 'química', 'programación', 'estadística', 
            'economía', 'ingles', 'matemáticas', 'biología', 'filosofía', 'historia'
        ],
        'horarios': [
            'horario', 'horarios', 'disponibilidad', 'cuándo', 'qué días', 'cuando', 
            'que dias', 'hora', 'fechas', 'días disponibles', 'disponible'
        ],
        'costos': [
            'precio', 'costo', 'tarifa', 'cuánto cuesta', 'cuanto cuesta', 'dinero', 
            'pago', 'pagos', 'valor', 'cuánto', 'cuanto', 'gratis', 'subsidio', 'descuento'
        ],
        'soporte': [
            'ayuda', 'soporte', 'problema', 'error', 'no funciona', 'ayudar', 
            'ayúdame', 'ayudame', 'necesito ayuda', 'tengo un problema', 'no puedo', 
            'fallo', 'falla', 'bug', 'problemas', 'duda', 'pregunta', 'preguntar'
        ],
        'contacto': [
            'contacto', 'contactar', 'teléfono', 'telefono', 'correo', 'email', 
            'dirección', 'direccion', 'oficina', 'ubicación', 'ubicacion', 'llamar', 'redes sociales'
        ],
        'despedida': [
            'adiós', 'adios', 'chau', 'hasta luego', 'gracias', 'muchas gracias', 
            'ok', 'gracias por todo', 'muchas gracias por la ayuda', 'bye', 'goodbye'
        ],
        'login': [
            'login', 'iniciar sesion', 'iniciar sesión', 'entrar', 'acceder', 
            'no puedo entrar', 'no puedo iniciar sesión', 'contraseña olvidada', 
            'olvide mi contraseña', 'olvidé mi contraseña', 'recuperar contraseña',
            'cambiar contraseña', 'contraseña nueva'
        ],
        'perfil': [
            'perfil', 'mi perfil', 'editar perfil', 'actualizar perfil', 'cambiar datos', 
            'datos personales', 'informacion personal', 'información personal', 'foto de perfil'
        ],
        'tutor': [
            'ser tutor', 'cómo ser tutor', 'como ser tutor', 'requisitos tutor',
            'inscribirse como tutor', 'registrarse como tutor', 'perfil de tutor'
        ],
        'pago': [
            'pagar', 'método de pago', 'metodo de pago', 'efectivo', 'transferencia',
            'nequi', 'daviplata', 'cómo pagar', 'como pagar', 'factura'
        ],
        'calificacion': [
            'calificar', 'calificación', 'calificacion', 'reseña', 'resena',
            'cómo calificar', 'como calificar', 'puntuación', 'puntuacion', 'estrellas'
        ],
        'seguridad': [
            'seguridad', 'privacidad', 'datos personales', 'contraseña segura',
            'cuenta segura', 'protección', 'proteccion'
        ]
    }

    RESPONSES = {
        'bienvenida': [
            '¡Hola! Bienvenido al soporte de TutoUdec. ¿En qué puedo ayudarte hoy?',
            '¡Hola! ¿Cómo estás? Estoy aquí para resolver tus dudas sobre TutoUdec y la UdeC.',
            '¡Bienvenido! Cuéntame, ¿qué necesitas saber?'
        ],
        'universidad': [
            'La Universidad de Cundinamarca (UdeC) es una institución pública de educación superior con sedes en varias ciudades del departamento. TutoUdec es la plataforma oficial de tutorías académicas.',
            'La UdeC ofrece programas de pregrado y posgrado en diversas áreas del conocimiento. Nuestra plataforma conecta estudiantes con tutores calificados.',
            'En la Universidad de Cundinamarca, las tutorías son parte fundamental del apoyo académico. TutoUdec facilita este proceso.',
            'La UdeC tiene sedes en Fusagasugá, Facatativá, Soacha, Ubaté y Chía. El campus principal está en Fusagasugá.'
        ],
        'inscripcion': [
            'Para inscribirte en TutoUdec, simplemente ve a la sección de "Registro", completa tus datos y elige si eres estudiante o tutor. ¡Es rápido y fácil!',
            'La inscripción es gratuita. Solo necesitas tu correo institucional (@udec.edu.co) o personal para crear tu cuenta.',
            '¿Problemas para inscribirte? Asegúrate de completar todos los campos obligatorios y verifica tu conexión a internet.',
            'Si ya tienes cuenta, ve a "Iniciar Sesión" e ingresa tu usuario y contraseña. ¡Es así de simple!'
        ],
        'tutorias': [
            'Las tutorías en TutoUdec son sesiones personalizadas donde un tutor calificado te ayudará con tus dudas académicas. Puedes buscar tutores por materia o nombre.',
            'Para agendar una tutoría: 1) Busca un tutor disponible, 2) Selecciona un horario que te convenga, 3) Confirma tu reserva.',
            'Los tutores son estudiantes avanzados o profesionales con experiencia en sus áreas. Todos son verificados por la universidad.',
            'Puedes crear una nueva tutoría tocando el botón + en la barra inferior de la aplicación.',
            'Si necesitas cancelar una tutoría, ve a la sección de "Tutorias", selecciona la tutoría y toca el botón de cancelar.',
            'Recuerda que debes cancelar con al menos 2 horas de anticipación para evitar penalizaciones.'
        ],
        'materias': [
            'Ofrecemos tutorías en una amplia variedad de materias: Cálculo, Álgebra, Física, Química, Programación, Estadística, Economía, Inglés, Biología, Filosofía, Historia y muchas más.',
            'Puedes ver todas las materias disponibles en la sección "Materias" de la aplicación. Si no encuentras la que necesitas, ¡avísanos!',
            'Cada materia tiene múltiples tutores disponibles para que elijas el que mejor se adapte a tu estilo de aprendizaje.',
            'Las materias más populares son: Cálculo I y II, Física Mecánica, Programación Básica, Álgebra Lineal y Estadística.'
        ],
        'horarios': [
            'Los tutores establecen sus propios horarios de disponibilidad. Puedes ver los horarios disponibles en el perfil de cada tutor.',
            'Las tutorías pueden ser presenciales en el campus o virtuales (online). Elige la modalidad que prefieras.',
            'Recuerda confirmar tu asistencia a las tutorías. Si no puedes asistir, cancela con anticipación.',
            'Los horarios más comunes son de lunes a viernes entre 2:00 PM y 8:00 PM, y sábados por la mañana.'
        ],
        'costos': [
            'Los precios varían según el tutor y la materia. Puedes ver la tarifa por hora en el perfil de cada tutor.',
            'Algunas tutorías pueden ser gratuitas o subsidiadas por la universidad. ¡Revisa los detalles!',
            'El pago se realiza directamente con el tutor o a través de la plataforma, según lo acordado.',
            'Las tarifas típicas están entre $20,000 y $50,000 pesos colombianos por hora. Los tutores expertos pueden cobrar más.',
            'Siempre pregunta por descuentos o paquetes de varias tutorías, muchos tutores ofrecen precios especiales.'
        ],
        'soporte': [
            'Estoy aquí para ayudarte. ¿Qué problema estás experimentando? Cuéntame los detalles para poder ayudarte mejor.',
            'Si tienes un problema técnico, puedes escribir a tutoudec.soporte@gmail.com. Para dudas académicas, ¡usa el chatbot o busca un tutor!',
            'Revisa primero la sección de "Ayuda" en la aplicación. Si no encuentras la respuesta, ¡no dudes en preguntarme!',
            'Para reportar un error, por favor incluye: ¿Qué estabas haciendo? ¿Qué error apareció? ¿Qué dispositivo usas? Gracias por ayudarnos a mejorar!'
        ],
        'contacto': [
            'Puedes contactarnos a través de: Correo: tutoudec.soporte@gmail.com, Teléfono: +57 1 234 5678, o visitarnos en el campus principal.',
            'Nuestro horario de atención es de lunes a viernes de 8:00 AM a 6:00 PM.',
            'La oficina de soporte está ubicada en el edificio A, sala 101 del campus principal de la UdeC en Fusagasugá.',
            'Si prefieres, también puedes contactarnos a través de nuestras redes sociales: @TutoUdec en Instagram y Facebook.',
            'Síguenos en redes sociales para estar al tanto de noticias, consejos y nuevas funcionalidades de TutoUdec!'
        ],
        'despedida': [
            '¡De nada! Un gusto ayudarte. ¡Éxito en tus estudios!',
            '¡Gracias por usar TutoUdec! Si necesitas más ayuda, ¡aquí estaré!',
            '¡Hasta pronto! Que tengas un excelente día y mucho éxito en la UdeC.',
            '¡Nos vemos! Recuerda que estoy aquí para ayudarte con cualquier duda que tengas.'
        ],
        'login': [
            'Para iniciar sesión, ve a la pantalla de "Iniciar Sesión" e ingresa tu nombre de usuario o correo y tu contraseña.',
            'Si olvidaste tu contraseña, toca en "¿Olvidaste tu contraseña?" y sigue las instrucciones para restablecerla.',
            'Asegúrate de que tu conexión a internet esté activa y que estás usando las credenciales correctas.',
            'Si sigue sin funcionar, verifica que no tengas mayúsculas activadas o espacios extra en tu usuario o contraseña.',
            'Para cambiar tu contraseña, ve a tu perfil y selecciona la opción "Seguridad y Contraseña".'
        ],
        'perfil': [
            'Para ver o editar tu perfil, ve a la sección "Perfil" en la barra inferior de la aplicación.',
            'En tu perfil puedes cambiar tu foto, actualizar tus datos personales y ver tu historial de tutorías.',
            'Si eres tutor, también puedes gestionar tu disponibilidad y tus materias desde tu perfil.',
            'Recuerda mantener tu información actualizada para que los demás usuarios puedan conocerte mejor.',
            'Tu foto de perfil ayuda a los demás usuarios a reconocerte, así que elige una imagen clara y profesional.'
        ],
        'tutor': [
            '¡Ser tutor es una excelente oportunidad para compartir tus conocimientos y ganar dinero!',
            'Para ser tutor, debes ser estudiante avanzado o egresado de la UdeC, tener buenas calificaciones y pasar un proceso de selección.',
            'Los requisitos para ser tutor son: promedio mínimo de 3.5, disponibilidad horaria y conocimientos sólidos en al menos una materia.',
            'Si quieres inscribirte como tutor, ve a la sección de registro y selecciona la opción "Soy tutor".',
            'Como tutor, puedes establecer tus propios horarios y tarifas, y ayudar a otros estudiantes a tener éxito académico.'
        ],
        'pago': [
            'Los métodos de pago varían según el tutor. La mayoría acepta efectivo, transferencias bancarias, Nequi o Daviplata.',
            'Siempre acuerda el método de pago con tu tutor antes de la tutoría para evitar malentendidos.',
            'Si pagas por transferencia, guarda el comprobante de pago y compártelo con tu tutor.',
            'Recuerda que el pago se realiza después de la tutoría, a menos que hayas acordado lo contrario con tu tutor.',
            'Si tienes problemas con el pago, contacta a soporte técnico a través de tutoudec.soporte@gmail.com.'
        ],
        'calificacion': [
            'Calificar a tu tutor es muy importante para ayudar a otros estudiantes a tomar decisiones.',
            'Para calificar a un tutor, ve a la sección de "Tutorias", selecciona la tutoría completada y toca el botón de calificar.',
            'Puedes calificar del 1 al 5 estrellas y dejar un comentario sobre tu experiencia con el tutor.',
            'Las calificaciones ayudan a mantener la calidad de los tutores en la plataforma.',
            'Recuerda ser honesto y constructivo en tu reseña, ¡esto ayuda a mejorar la comunidad!'
        ],
        'seguridad': [
            'Tu seguridad y privacidad son nuestra prioridad. Nunca compartas tu contraseña con nadie.',
            'Usa una contraseña segura: combina letras mayúsculas y minúsculas, números y símbolos.',
            'No compartas información personal sensible (como números de tarjeta) en la plataforma.',
            'Si notas actividad sospechosa en tu cuenta, cambia tu contraseña inmediatamente y contacta a soporte.',
            'Recuerda cerrar sesión cuando uses dispositivos públicos o compartidos.'
        ],
        'default': [
            'Lo siento, no entiendo tu pregunta. ¿Podrías reformularla?',
            'Interesante. ¿Podrías ser más específico? Estoy aquí para ayudarte con TutoUdec y la UdeC.',
            'No tengo información sobre eso. ¿Podrías preguntar algo relacionado con las tutorías o la universidad?',
            'Disculpa, no reconozco esa pregunta. Prueba preguntar sobre: tutorías, materias, inscripción, horarios, costos, seguridad o la universidad.'
        ]
    }

    def classify_intent(self, message):
        message_lower = message.lower()
        for intent, keywords in self.KNOWLEDGE_BASE.items():
            for keyword in keywords:
                if keyword in message_lower:
                    return intent
        return 'default'

    def get_response(self, intent):
        import random
        return random.choice(self.RESPONSES[intent])

    @action(detail=False, methods=['post'])
    def chat(self, request):
        """Enviar mensaje al chatbot y recibir respuesta"""
        user_message = request.data.get('message', '')
        
        if not user_message.strip():
            return Response(
                {'detail': 'Por favor envía un mensaje'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        from .ai_chatbot import chat_response_json
        history = request.data.get('history') or []
        if not isinstance(history, list):
            history = []
        chat_json = chat_response_json(
            user_message[:1000], [h for h in history[-8:] if isinstance(h, dict)]
        )
        payload = chat_json['payload']

        return Response({
            'user_message': user_message,
            'bot_response': payload['answer'],
            'intent': payload['intent'],
            'suggestions': payload['suggestions'],
            'response_json': {
                'standard': 'empresarial-5.0',
                'mode': chat_json['mode'],
                'provider': chat_json['provider'],
                **payload,
            }
        })

    @action(detail=False, methods=['get'])
    def quick_questions(self, request):
        """Obtener preguntas frecuentes sugeridas"""
        questions = [
            '¿Cómo me inscribo?',
            '¿Qué materias hay disponibles?',
            '¿Cómo busco un tutor?',
            '¿Cuánto cuestan las tutorías?',
            '¿Qué es la UdeC?'
        ]
        return Response({'quick_questions': questions})


class GrupoTutoriaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para grupos de tutoría con cupos múltiples.
    """
    queryset = GrupoTutoria.objects.select_related('tutor', 'materia').all()
    serializer_class = GrupoTutoriaSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['tutor', 'materia', 'modalidad', 'estado']
    search_fields = ['nombre', 'descripcion', 'materia__nombre', 'tutor__usuario__username']
    ordering_fields = ['fecha_inicio', 'creado_en', 'cupos_disponibles']
    ordering = ['-fecha_inicio']

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminOrReadOnly]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        grupo = serializer.save()
        grupo.cupos_disponibles = grupo.cupos_maximos
        grupo.save()

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def inscribirse(self, request, pk=None):
        """Inscribirse en un grupo de tutoría"""
        grupo = self.get_object()
        
        if grupo.esta_lleno:
            return Response(
                {'error': 'El grupo está lleno'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if grupo.estado != 'programado':
            return Response(
                {'error': 'Solo se puede inscribir en grupos programados'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        inscripcion, created = InscripcionGrupo.objects.get_or_create(
            grupo=grupo,
            estudiante=request.user,
            defaults={'estado': 'inscrito'}
        )
        
        if not created:
            if inscripcion.estado == 'cancelado':
                inscripcion.estado = 'inscrito'
                inscripcion.save()
                grupo.cupos_disponibles -= 1
                grupo.save()
            else:
                return Response(
                    {'error': 'Ya estás inscrito en este grupo'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            grupo.cupos_disponibles -= 1
            grupo.save()
        
        return Response(
            InscripcionGrupoSerializer(inscripcion).data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def mis_grupos(self, request):
        """Obtener grupos donde el usuario está inscrito"""
        inscripciones = InscripcionGrupo.objects.filter(
            estudiante=request.user,
            estado='inscrito'
        ).select_related('grupo')
        grupos = [i.grupo for i in inscripciones]
        serializer = self.get_serializer(grupos, many=True)
        return Response(serializer.data)


class InscripcionGrupoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para inscripciones en grupos de tutoría.
    """
    queryset = InscripcionGrupo.objects.select_related('grupo', 'estudiante').all()
    serializer_class = InscripcionGrupoSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['grupo', 'estudiante', 'estado', 'asistio']
    ordering_fields = ['fecha_inscripcion']
    ordering = ['-fecha_inscripcion']

    def get_queryset(self):
        qs = super().get_queryset()
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return qs
        if hasattr(user, 'perfil_tutor'):
            return qs.filter(grupo__tutor=user.perfil_tutor)
        return qs.filter(estudiante=user)

    @action(detail=True, methods=['post'])
    def cancelar(self, request, pk=None):
        """Cancelar inscripción en un grupo"""
        inscripcion = self.get_object()
        
        if inscripcion.estudiante != request.user and not request.user.is_staff:
            return Response(
                {'detail': 'No tienes permiso para cancelar esta inscripción'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        if inscripcion.estado == 'cancelado':
            return Response(
                {'error': 'La inscripción ya está cancelada'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        inscripcion.estado = 'cancelado'
        inscripcion.save()
        
        grupo = inscripcion.grupo
        grupo.cupos_disponibles += 1
        grupo.save()
        
        return Response(InscripcionGrupoSerializer(inscripcion).data)