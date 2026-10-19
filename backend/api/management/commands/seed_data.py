from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from backend.api.models import Materia, Tutor, Disponibilidad, GrupoTutoria, Tutoria
import random
from datetime import date, datetime, time, timedelta

class Command(BaseCommand):
    help = 'Crea datos de prueba: materias, tutores y disponibilidades'

    def handle(self, *args, **options):
        self.stdout.write('Iniciando creación de datos de prueba...\n')
        
        # Datos de materias
        materias_data = [
            {'nombre': 'Cálculo I', 'descripcion': 'Cálculo diferencial e integral de funciones de una variable'},
            {'nombre': 'Cálculo II', 'descripcion': 'Cálculo de funciones de varias variables y series'},
            {'nombre': 'Álgebra Lineal', 'descripcion': 'Vectores, matrices, sistemas de ecuaciones lineales'},
            {'nombre': 'Física I', 'descripcion': 'Mecánica clásica y teoría de campos'},
            {'nombre': 'Física II', 'descripcion': 'Electromagnetismo y óptica'},
            {'nombre': 'Química General', 'descripcion': 'Principios fundamentales de la química'},
            {'nombre': 'Programación I', 'descripcion': 'Introducción a la programación con Python'},
            {'nombre': 'Programación II', 'descripcion': 'Estructuras de datos y algoritmos'},
            {'nombre': 'Estadística', 'descripcion': 'Estadística descriptiva e inferencial'},
            {'nombre': 'Economía', 'descripcion': 'Principios de economía micro y macro'},
            {'nombre': 'Contabilidad', 'descripcion': 'Contabilidad financiera y administrativa'},
            {'nombre': 'Derecho Constitucional', 'descripcion': 'Derecho público y constitucional'},
            {'nombre': 'Biología', 'descripcion': 'Biología celular y molecular'},
            {'nombre': 'Inglés I', 'descripcion': 'Nivel básico de inglés'},
            {'nombre': 'Inglés II', 'descripcion': 'Nivel intermedio de inglés'},
            {'nombre': 'Inglés III', 'descripcion': 'Nivel avanzado de inglés'},
            {'nombre': 'Matemáticas Discretas', 'descripcion': 'Teoría de conjuntos y lógica'},
            {'nombre': 'Arquitectura de Computadores', 'descripcion': 'Organización y arquitectura de sistemas'},
            {'nombre': 'Bases de Datos', 'descripcion': 'Diseño y administración de bases de datos'},
            {'nombre': 'Sistemas Operativos', 'descripcion': 'Principios de sistemas operativos'},
            {'nombre': 'Redes de Computadores', 'descripcion': 'Redes y protocolos de comunicación'},
            {'nombre': 'Ingeniería de Software', 'descripcion': 'Metodologías y procesos de desarrollo'},
            {'nombre': 'Inteligencia Artificial', 'descripcion': 'Fundamentos de IA y machine learning'},
            {'nombre': 'Sociología', 'descripcion': 'Principios de sociología'},
            {'nombre': 'Psicología', 'descripcion': 'Psicología general y aplicada'},
        ]
        
        # Crear materias
        materias = []
        for mat_data in materias_data:
            materia, created = Materia.objects.get_or_create(
                nombre=mat_data['nombre'],
                defaults={'descripcion': mat_data['descripcion']}
            )
            materias.append(materia)
            if created:
                self.stdout.write(f'[OK] Creada materia: {materia.nombre}\n')
        
        # Datos de tutores
        tutores_data = [
            {'nombre': 'Carlos', 'apellido': 'Rodríguez', 'username': 'crodriguez', 'email': 'crodriguez@udec.edu.co', 'especialidad': 'Matemáticas', 'nivel': 'experto', 'tarifa': 35000},
            {'nombre': 'Ana', 'apellido': 'García', 'username': 'agarcia', 'email': 'agarcia@udec.edu.co', 'especialidad': 'Física', 'nivel': 'avanzado', 'tarifa': 30000},
            {'nombre': 'Luis', 'apellido': 'Martínez', 'username': 'lmartinez', 'email': 'lmartinez@udec.edu.co', 'especialidad': 'Programación', 'nivel': 'experto', 'tarifa': 40000},
            {'nombre': 'María', 'apellido': 'López', 'username': 'mlopez', 'email': 'mlopez@udec.edu.co', 'especialidad': 'Química', 'nivel': 'intermedio', 'tarifa': 25000},
            {'nombre': 'Juan', 'apellido': 'Hernández', 'username': 'jhernandez', 'email': 'jhernandez@udec.edu.co', 'especialidad': 'Estadística', 'nivel': 'avanzado', 'tarifa': 32000},
            {'nombre': 'Sofía', 'apellido': 'González', 'username': 'sgonzalez', 'email': 'sgonzalez@udec.edu.co', 'especialidad': 'Economía', 'nivel': 'intermedio', 'tarifa': 28000},
            {'nombre': 'Diego', 'apellido': 'Pérez', 'username': 'dperez', 'email': 'dperez@udec.edu.co', 'especialidad': 'Derecho', 'nivel': 'experto', 'tarifa': 45000},
            {'nombre': 'Valentina', 'apellido': 'Sánchez', 'username': 'vsanchez', 'email': 'vsanchez@udec.edu.co', 'especialidad': 'Biología', 'nivel': 'avanzado', 'tarifa': 33000},
            {'nombre': 'Andrés', 'apellido': 'Ramírez', 'username': 'aramirez', 'email': 'aramirez@udec.edu.co', 'especialidad': 'Inglés', 'nivel': 'experto', 'tarifa': 30000},
            {'nombre': 'Isabella', 'apellido': 'Torres', 'username': 'itorres', 'email': 'itorres@udec.edu.co', 'especialidad': 'Contabilidad', 'nivel': 'intermedio', 'tarifa': 27000},
            {'nombre': 'Sebastián', 'apellido': 'Flores', 'username': 'sflores', 'email': 'sflores@udec.edu.co', 'especialidad': 'Arquitectura', 'nivel': 'avanzado', 'tarifa': 38000},
            {'nombre': 'Camila', 'apellido': 'Gutiérrez', 'username': 'cgutierrez', 'email': 'cgutierrez@udec.edu.co', 'especialidad': 'Sistemas Operativos', 'nivel': 'experto', 'tarifa': 42000},
            {'nombre': 'Nicolás', 'apellido': 'Rivas', 'username': 'nrivas', 'email': 'nrivas@udec.edu.co', 'especialidad': 'Redes', 'nivel': 'intermedio', 'tarifa': 31000},
            {'nombre': 'Paula', 'apellido': 'Molina', 'username': 'pmolina', 'email': 'pmolina@udec.edu.co', 'especialidad': 'Ingeniería de Software', 'nivel': 'avanzado', 'tarifa': 36000},
            {'nombre': 'Felipe', 'apellido': 'Ortiz', 'username': 'fortiz', 'email': 'fortiz@udec.edu.co', 'especialidad': 'Inteligencia Artificial', 'nivel': 'experto', 'tarifa': 50000},
            {'nombre': 'Juliana', 'apellido': 'Silva', 'username': 'jsilva', 'email': 'jsilva@udec.edu.co', 'especialidad': 'Sociología', 'nivel': 'intermedio', 'tarifa': 26000},
            {'nombre': 'Martín', 'apellido': 'Castro', 'username': 'mcastro', 'email': 'mcastro@udec.edu.co', 'especialidad': 'Psicología', 'nivel': 'avanzado', 'tarifa': 34000},
            {'nombre': 'Lucía', 'apellido': 'Guerrero', 'username': 'lguerrero', 'email': 'lguerrero@udec.edu.co', 'especialidad': 'Matemáticas Discretas', 'nivel': 'intermedio', 'tarifa': 29000},
            {'nombre': 'Emilio', 'apellido': 'Vargas', 'username': 'evargas', 'email': 'evargas@udec.edu.co', 'especialidad': 'Bases de Datos', 'nivel': 'experto', 'tarifa': 41000},
            {'nombre': 'Renata', 'apellido': 'Jiménez', 'username': 'rjimenez', 'email': 'rjimenez@udec.edu.co', 'especialidad': 'Cálculo', 'nivel': 'avanzado', 'tarifa': 37000},
        ]
        
        # Niveles de experiencia
        niveles = ['principiante', 'intermedio', 'avanzado', 'experto']
        
        # Crear tutores
        tutores_creados = []
        for tutor_data in tutores_data:
            # Crear usuario
            user, created = User.objects.get_or_create(
                username=tutor_data['username'],
                defaults={
                    'first_name': tutor_data['nombre'],
                    'last_name': tutor_data['apellido'],
                    'email': tutor_data['email'],
                }
            )
            if created:
                user.set_unusable_password()
                user.is_active = False
                user.save()
            
            # Crear tutor
            tutor, created = Tutor.objects.get_or_create(
                usuario=user,
                defaults={
                    'especialidad': tutor_data['especialidad'],
                    'nivel_experiencia': tutor_data['nivel'],
                    'tarifa_por_hora': tutor_data['tarifa'],
                    'bio': f'Tutor especializado en {tutor_data["especialidad"]} con experiencia en la Universidad de Cundinamarca.',
                    'disponible': True,
                }
            )
            
            # Asignar materias aleatorias
            num_materias = random.randint(2, 5)
            materias_asignadas = random.sample(materias, num_materias)
            tutor.materias.add(*materias_asignadas)
            
            # Crear disponibilidades
            dias_semana = list(range(7))
            horas_dia = [(8, 10), (10, 12), (14, 16), (16, 18), (18, 20)]
            num_disponibilidades = random.randint(3, 8)
            dias_elegidos = random.sample(dias_semana, min(num_disponibilidades, 7))
            
            for dia in dias_elegidos:
                hora = random.choice(horas_dia)
                Disponibilidad.objects.get_or_create(
                    tutor=tutor,
                    dia_semana=dia,
                    hora_inicio=f'{hora[0]:02d}:00:00',
                    hora_fin=f'{hora[1]:02d}:00:00',
                    defaults={'activo': True}
                )
            
            tutores_creados.append(tutor)
            if created:
                self.stdout.write(f'[OK] Creado tutor: {tutor_data["nombre"]} {tutor_data["apellido"]} - {tutor_data["especialidad"]}\n')
        
        # Crear grupos de tutoría con cupos
        grupos_data = [
            {'nombre': 'Cálculo I - Grupo 1', 'descripcion': 'Refuerzo semanal de límites, derivadas e integrales', 'cupos': 10, 'modalidad': 'presencial', 'materia_idx': 0, 'tutor_idx': 0},
            {'nombre': 'Álgebra Lineal - Grupo A', 'descripcion': 'Vectores, matrices y sistemas de ecuaciones', 'cupos': 12, 'modalidad': 'virtual', 'materia_idx': 2, 'tutor_idx': 0},
            {'nombre': 'Programación Python - Nivel Básico', 'descripcion': 'Introducción a la programación con Python', 'cupos': 15, 'modalidad': 'hibrida', 'materia_idx': 6, 'tutor_idx': 2},
            {'nombre': 'Inglés Conversacional - Grupo 2', 'descripcion': 'Práctica de conversación en inglés', 'cupos': 8, 'modalidad': 'virtual', 'materia_idx': 13, 'tutor_idx': 8},
            {'nombre': 'Física I - Mecánica', 'descripcion': 'Mecánica clásica y movimiento', 'cupos': 10, 'modalidad': 'presencial', 'materia_idx': 3, 'tutor_idx': 1},
            {'nombre': 'Estadística Aplicada', 'descripcion': 'Estadística para ciencias sociales', 'cupos': 12, 'modalidad': 'virtual', 'materia_idx': 8, 'tutor_idx': 4},
            {'nombre': 'Cálculo II - Series', 'descripcion': 'Series y funciones de varias variables', 'cupos': 10, 'modalidad': 'presencial', 'materia_idx': 1, 'tutor_idx': 0},
            {'nombre': 'Química General', 'descripcion': 'Principios fundamentales de química', 'cupos': 12, 'modalidad': 'presencial', 'materia_idx': 5, 'tutor_idx': 3},
        ]
        
        grupos_creados = 0
        for grupo_data in grupos_data:
            materia_asignada = materias[grupo_data['materia_idx']]
            tutor_asignado = tutores_creados[grupo_data['tutor_idx']]
            tutor_asignado.materias.add(materia_asignada)
            
            fecha_inicio = timezone.now() + timedelta(days=random.randint(1, 14), hours=random.randint(8, 18))
            fecha_fin = fecha_inicio + timedelta(hours=2)
            
            grupo, created = GrupoTutoria.objects.get_or_create(
                nombre=grupo_data['nombre'],
                tutor=tutor_asignado,
                defaults={
                    'materia': materia_asignada,
                    'descripcion': grupo_data['descripcion'],
                    'cupos_maximos': grupo_data['cupos'],
                    'cupos_disponibles': grupo_data['cupos'],
                    'fecha_inicio': fecha_inicio,
                    'fecha_fin': fecha_fin,
                    'lugar': f'Sala {random.randint(101, 300)} - Edificio A' if grupo_data['modalidad'] == 'presencial' else 'Link: https://zoom.us/j/123456789',
                    'modalidad': grupo_data['modalidad'],
                    'estado': 'programado'
                }
            )
            
            if created:
                grupos_creados += 1
                self.stdout.write(f'[OK] Creado grupo: {grupo_data["nombre"]} - {grupo_data["cupos"]} cupos\n')

        estudiante_demo, estudiante_creado = User.objects.get_or_create(
            username='demo_estudiante',
            defaults={
                'first_name': 'Estudiante',
                'last_name': 'Demostración',
                'email': 'demo.estudiante@example.invalid',
                'is_active': False,
            },
        )
        if estudiante_creado:
            estudiante_demo.set_unusable_password()
            estudiante_demo.save()

        hoy = timezone.localdate()
        indice_mes_actual = hoy.year * 12 + hoy.month - 1
        estados_demo = ['completada', 'confirmada', 'pendiente', 'cancelada', 'completada', 'completada']
        tutorias_creadas = 0
        for desplazamiento, estado in enumerate(estados_demo):
            indice_mes = indice_mes_actual - desplazamiento
            anio, mes_cero_based = divmod(indice_mes, 12)
            fecha = date(anio, mes_cero_based + 1, 15)
            fecha_inicio = timezone.make_aware(
                datetime.combine(fecha, time(hour=14))
            )
            tutor = tutores_creados[desplazamiento]
            materia = tutor.materias.first()
            if materia is None:
                continue
            tutoria, created = Tutoria.objects.get_or_create(
                estudiante=estudiante_demo,
                tutor=tutor,
                defaults={
                    'materia': materia,
                    'fecha_inicio': fecha_inicio,
                    'duracion_minutos': 60,
                    'estado': estado,
                    'descripcion': 'Registro ficticio para demostración del prototipo.',
                    'lugar': 'Universidad de Cundinamarca',
                },
            )
            if created:
                Tutoria.objects.filter(pk=tutoria.pk).update(
                    creado_en=fecha_inicio
                )
                tutorias_creadas += 1
        
        self.stdout.write('\n[OK] Datos de prueba creados exitosamente!\n')
        self.stdout.write(f'   - {len(materias)} materias\n')
        self.stdout.write(f'   - {len(tutores_creados)} tutores\n')
        self.stdout.write(f'   - {grupos_creados} grupos de tutoría\n')
        self.stdout.write(f'   - {tutorias_creadas} tutorías ficticias\n')
