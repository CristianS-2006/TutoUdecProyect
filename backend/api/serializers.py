from rest_framework import serializers
from django.contrib.auth.models import User
from django.db.models import Avg
from .models import Tutor, Materia, Tutoria, Disponibilidad, Resena, GrupoTutoria, InscripcionGrupo


class UserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role']
        read_only_fields = ['id']

    def get_role(self, obj):
        if obj.is_staff or obj.is_superuser:
            return 'admin'
        if hasattr(obj, 'perfil_tutor'):
            return 'tutor'
        return 'estudiante'


class AdminUserSerializer(serializers.ModelSerializer):
    """
    Serializer para gestión de usuarios por administradores (API).
    Permite editar flags y asignar permisos/grupos.
    """

    role = serializers.SerializerMethodField(read_only=True)
    groups = serializers.PrimaryKeyRelatedField(many=True, read_only=False, queryset=User.groups.rel.model.objects.all())
    user_permissions = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=False,
        queryset=User.user_permissions.rel.model.objects.all(),
        required=False,
    )

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
            'role',
        ]
        read_only_fields = ['id', 'role']

    def get_role(self, obj):
        if obj.is_staff or obj.is_superuser:
            return 'admin'
        if hasattr(obj, 'perfil_tutor'):
            return 'tutor'
        return 'estudiante'


class MateriaSerializer(serializers.ModelSerializer):
    total_tutorias = serializers.SerializerMethodField()
    total_tutores = serializers.SerializerMethodField()
    valoracion = serializers.SerializerMethodField()
    
    class Meta:
        model = Materia
        fields = ['id', 'nombre', 'descripcion', 'creado_en', 'total_tutorias', 'total_tutores', 'valoracion']
        read_only_fields = ['id', 'creado_en']

    def to_internal_value(self, data):
        """
        Compatibilidad con clientes que envían claves distintas
        (por ejemplo `name` en lugar de `nombre`).
        """
        mutable_data = dict(data)
        if not mutable_data.get('nombre'):
            if mutable_data.get('name'):
                mutable_data['nombre'] = mutable_data.get('name')
            elif mutable_data.get('titulo'):
                mutable_data['nombre'] = mutable_data.get('titulo')
            elif mutable_data.get('materia'):
                mutable_data['nombre'] = mutable_data.get('materia')
        return super().to_internal_value(mutable_data)
    
    def get_total_tutorias(self, obj):
        return obj.tutorias.count()

    def get_total_tutores(self, obj):
        return obj.tutores.count()

    def get_valoracion(self, obj):
        promedio = obj.tutores.aggregate(p=Avg('calificacion'))['p']
        return round(float(promedio), 1) if promedio else 0.0


class TutorSerializer(serializers.ModelSerializer):
    usuario = UserSerializer(read_only=True)
    usuario_nombre = serializers.SerializerMethodField()
    total_resenas = serializers.SerializerMethodField()
    resenas = serializers.SerializerMethodField()
    usuario_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='usuario',
        write_only=True
    )
    materias = MateriaSerializer(many=True, read_only=True)
    materias_ids = serializers.PrimaryKeyRelatedField(
        queryset=Materia.objects.all(),
        many=True,
        source='materias',
        write_only=True
    )
    total_tutorias = serializers.SerializerMethodField()
    promedio_calificacion = serializers.ReadOnlyField(source='calificacion')
    
    class Meta:
        model = Tutor
        fields = [
            'id', 'usuario', 'usuario_id', 'especialidad', 'nivel_experiencia',
            'bio', 'tarifa_por_hora', 'calificacion', 'foto', 'teléfono',
            'disponible', 'materias', 'materias_ids', 'total_tutorias',
            'promedio_calificacion', 'creado_en', 'actualizado_en',
            'usuario_nombre', 'total_resenas', 'resenas'
        ]
        read_only_fields = ['id', 'creado_en', 'actualizado_en']
    
    def get_total_tutorias(self, obj):
        return obj.tutorias.count()

    def get_usuario_nombre(self, obj):
        return obj.usuario.get_full_name() or obj.usuario.username

    def get_total_resenas(self, obj):
        return obj.resenas.count()

    def get_resenas(self, obj):
        return [
            {
                'estudiante': r.estudiante.get_full_name() or r.estudiante.username,
                'calificacion': r.calificacion,
                'comentario': r.comentario,
                'creado_en': r.creado_en,
            }
            for r in obj.resenas.select_related('estudiante')[:5]
        ]


class TutoriaSerializer(serializers.ModelSerializer):
    tutor_nombre = serializers.CharField(source='tutor.usuario.get_full_name', read_only=True)
    estudiante_nombre = serializers.CharField(source='estudiante.get_full_name', read_only=True)
    materia_nombre = serializers.CharField(source='materia.nombre', read_only=True)
    
    class Meta:
        model = Tutoria
        fields = [
            'id', 'tutor', 'tutor_nombre', 'estudiante', 'estudiante_nombre',
            'materia', 'materia_nombre', 'fecha_inicio', 'fecha_fin',
            'duracion_minutos', 'estado', 'descripcion', 'lugar', 'tarifa',
            'nota', 'creado_en', 'actualizado_en'
        ]
        read_only_fields = ['id', 'creado_en', 'actualizado_en']
        extra_kwargs = {'estudiante': {'required': False}}


class TutorListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listar tutores"""
    usuario_nombre = serializers.CharField(source='usuario.get_full_name', read_only=True)
    total_tutorias = serializers.SerializerMethodField()
    materias_nombres = serializers.SerializerMethodField()
    
    class Meta:
        model = Tutor
        fields = [
            'id', 'usuario_nombre', 'especialidad', 'nivel_experiencia', 'bio',
            'tarifa_por_hora', 'calificacion', 'disponible', 'total_tutorias', 'materias_nombres'
        ]
    
    def get_materias_nombres(self, obj):
        return [m.nombre for m in obj.materias.all()]
    
    def get_total_tutorias(self, obj):
        return obj.tutorias.filter(estado='completada').count()


class DisponibilidadSerializer(serializers.ModelSerializer):
    tutor_nombre = serializers.CharField(source='tutor.usuario.username', read_only=True)
    dia_semana_display = serializers.CharField(source='get_dia_semana_display', read_only=True)

    class Meta:
        model = Disponibilidad
        fields = [
            'id', 'tutor', 'tutor_nombre', 'dia_semana', 'dia_semana_display',
            'hora_inicio', 'hora_fin', 'activo'
        ]
        read_only_fields = ['id']


class ResenaSerializer(serializers.ModelSerializer):
    tutor_nombre = serializers.CharField(source='tutor.usuario.username', read_only=True)
    estudiante_nombre = serializers.CharField(source='estudiante.username', read_only=True)

    class Meta:
        model = Resena
        fields = [
            'id', 'tutor', 'tutor_nombre', 'estudiante', 'estudiante_nombre',
            'tutoria', 'grupo', 'calificacion', 'comentario', 'creado_en'
        ]
        read_only_fields = ['id', 'creado_en']


class GrupoTutoriaSerializer(serializers.ModelSerializer):
    tutor_nombre = serializers.CharField(source='tutor.usuario.get_full_name', read_only=True)
    materia_nombre = serializers.CharField(source='materia.nombre', read_only=True)
    esta_lleno = serializers.BooleanField(read_only=True)
    estudiantes_inscritos = serializers.SerializerMethodField()

    class Meta:
        model = GrupoTutoria
        fields = [
            'id', 'tutor', 'tutor_nombre', 'materia', 'materia_nombre',
            'nombre', 'descripcion', 'cupos_maximos', 'cupos_disponibles',
            'esta_lleno', 'fecha_inicio', 'fecha_fin', 'duracion_minutos',
            'lugar', 'modalidad', 'estado', 'estudiantes_inscritos',
            'creado_en', 'actualizado_en'
        ]
        read_only_fields = ['id', 'creado_en', 'actualizado_en', 'cupos_disponibles']

    def get_estudiantes_inscritos(self, obj):
        inscripciones = obj.inscripciones.filter(estado='inscrito').select_related('estudiante')
        return UserSerializer([i.estudiante for i in inscripciones], many=True).data


class InscripcionGrupoSerializer(serializers.ModelSerializer):
    estudiante_nombre = serializers.CharField(source='estudiante.get_full_name', read_only=True)
    estudiante_username = serializers.CharField(source='estudiante.username', read_only=True)
    grupo_nombre = serializers.CharField(source='grupo.nombre', read_only=True)
    materia_nombre = serializers.CharField(source='grupo.materia.nombre', read_only=True)

    class Meta:
        model = InscripcionGrupo
        fields = [
            'id', 'grupo', 'grupo_nombre', 'materia_nombre',
            'estudiante', 'estudiante_nombre', 'estudiante_username',
            'fecha_inscripcion', 'estado', 'asistio'
        ]
        read_only_fields = ['id', 'fecha_inscripcion', 'estudiante']