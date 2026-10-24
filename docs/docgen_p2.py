import json
import yaml
from docgen_base import *


def ej(nombre, max_lineas=60):
    with open(os.path.join(RAIZ, 'docs', f'_ej_{nombre}.json'), encoding='utf-8') as f:
        lineas = f.read().split('\n')
    if len(lineas) > max_lineas:
        lineas = lineas[:max_lineas] + ['  ...']
    return '\n'.join(lineas)


DESC = {
    'POST /api/auth/register/': ('Crea una cuenta nueva (estudiante o tutor) y devuelve los tokens', 'Pública'),
    'POST /api/auth/login/': ('Valida usuario y contraseña y devuelve access y refresh', 'Pública'),
    'POST /api/auth/refresh/': ('Entrega un nuevo token de acceso a partir del refresh', 'Pública'),
    'GET /api/auth/profile/': ('Datos del usuario autenticado', 'JWT'),
    'POST /api/auth/change_password/': ('Cambia la contraseña conociendo la actual', 'JWT'),
    'POST /api/auth/request_password_reset/': ('Genera un token de recuperación para el correo indicado', 'Pública'),
    'POST /api/auth/confirm_password_reset/': ('Fija una contraseña nueva con el token recibido', 'Pública'),
    'POST /api/chatbot/chat/': ('Envía un mensaje al asistente y recibe respuesta y JSON 5.0', 'Pública'),
    'GET /api/chatbot/quick_questions/': ('Preguntas rápidas sugeridas', 'Pública'),
    'GET /api/dashboard/resumen/': ('Métricas globales del sistema', 'Administrador'),
    'GET /api/tutores/': ('Lista paginada de tutores', 'Pública'),
    'POST /api/tutores/': ('Crea un perfil de tutor', 'Administrador'),
    'GET /api/tutores/{id}/': ('Detalle del tutor con materias y reseñas', 'Pública'),
    'GET /api/tutores/{id}/disponibilidad_mensual/': ('Días y horarios libres del mes', 'Pública'),
    'GET /api/tutores/{id}/estadisticas/': ('Conteo de tutorías por estado y calificación', 'JWT'),
    'GET /api/tutores/{id}/tutorias/': ('Tutorías de ese tutor', 'JWT'),
    'POST /api/tutores/{id}/marcar_disponible/': ('Activa al tutor para recibir reservas', 'JWT (dueño)'),
    'POST /api/tutores/{id}/marcar_no_disponible/': ('Pausa las reservas del tutor', 'JWT (dueño)'),
    'GET /api/tutores/mi_perfil/': ('Perfil de tutor del usuario autenticado', 'JWT'),
    'GET /api/materias/': ('Catálogo de materias con valoración y total de tutores', 'Pública'),
    'GET /api/materias/{id}/': ('Detalle de una materia', 'Pública'),
    'GET /api/materias/{id}/tutores/': ('Tutores que dictan la materia', 'Pública'),
    'GET /api/materias/{id}/tutorias/': ('Tutorías registradas de la materia', 'JWT'),
    'GET /api/tutorias/': ('Lista de tutorías (según rol)', 'JWT'),
    'POST /api/tutorias/': ('Agenda una tutoría con validación de reserva', 'JWT'),
    'GET /api/tutorias/mis_tutorias/': ('Tutorías del estudiante autenticado', 'JWT'),
    'GET /api/tutorias/mis_tutorias_como_tutor/': ('Tutorías que atiende el tutor autenticado', 'JWT'),
    'POST /api/tutorias/{id}/confirmar/': ('Pasa la tutoría de pendiente a confirmada', 'JWT (tutor)'),
    'POST /api/tutorias/{id}/iniciar/': ('Pasa la tutoría a en progreso', 'JWT (tutor)'),
    'POST /api/tutorias/{id}/completar/': ('Marca la tutoría como completada', 'JWT (tutor)'),
    'POST /api/tutorias/{id}/cancelar/': ('Cancela la tutoría', 'JWT'),
    'GET /api/disponibilidades/': ('Franjas semanales de disponibilidad', 'JWT'),
    'GET /api/resenas/': ('Reseñas registradas', 'Pública'),
    'POST /api/resenas/': ('Crea una reseña', 'JWT'),
    'GET /api/grupos/': ('Grupos de tutoría', 'JWT'),
    'POST /api/grupos/{id}/inscribirse/': ('Inscribe al usuario autenticado en el grupo', 'JWT'),
    'GET /api/grupos/mis_grupos/': ('Grupos en los que está inscrito el usuario', 'JWT'),
    'POST /api/inscripciones/{id}/cancelar/': ('Cancela la inscripción', 'JWT'),
    'GET /api/usuarios/': ('Listado de usuarios', 'Administrador'),
    'POST /api/usuarios/{id}/make_admin/': ('Otorga permisos de administrador', 'Administrador'),
    'POST /api/usuarios/{id}/remove_admin/': ('Retira permisos de administrador', 'Administrador'),
}


def parte2():
    # ---------------------------------------------------------------
    H('5. Diagrama de casos de uso')
    P('El diagrama de casos de uso resume lo que cada actor puede hacer con el sistema. El estudiante concentra la mayor parte de las funciones porque es el usuario principal; el tutor aporta las acciones que cambian el estado de una tutoría y el administrador se ocupa del mantenimiento y de las métricas.')
    FIG_ALTO('docs/diagramas/02_casos_de_uso.png', 'Diagrama de casos de uso de TutoUdec.', 15.5)
    H('5.1 Especificación de los casos de uso principales', 2, False)
    casos = [
        ('CU-01 Registrarse e iniciar sesión', 'Visitante', 'Ninguna', ['El usuario abre «Registro» y completa nombre, usuario, correo, contraseña y rol.', 'El sistema valida los datos y la política de contraseñas.', 'Se crea el usuario (y el perfil de tutor si el rol lo pide) y se entregan los tokens.', 'El usuario queda con la sesión iniciada.'], 'Si el usuario o el correo ya existen, o la contraseña es débil, se muestra el mensaje de error en español y no se crea nada.'),
        ('CU-02 Recuperar contraseña', 'Usuario registrado', 'Tener un correo registrado', ['El usuario pide el restablecimiento con su correo.', 'El sistema crea un token de un solo uso con vencimiento.', 'El usuario ingresa el token y la nueva contraseña.', 'El sistema cambia la contraseña y marca el token como usado.'], 'Un token vencido o ya usado se rechaza con un mensaje claro.'),
        ('CU-03 Consultar agenda mensual', 'Estudiante', 'Ninguna', ['El estudiante abre el perfil de un tutor.', 'La aplicación pide la disponibilidad del mes y de la duración elegida.', 'El estudiante navega entre meses y ve los días con cupo.', 'Al tocar un día se listan los horarios libres.'], 'Si el tutor no tiene franjas configuradas, se aplica el horario por defecto de lunes a viernes de 8:00 a 18:00.'),
        ('CU-04 Agendar tutoría', 'Estudiante', 'Sesión iniciada', ['El estudiante elige día, hora, materia, duración y lugar.', 'La aplicación envía la solicitud.', 'El servidor valida fecha futura, ventana de disponibilidad, tutor disponible y ausencia de choques.', 'La tutoría se guarda como pendiente con fecha de fin y tarifa calculadas.'], 'Si alguna validación falla, el servidor responde 400 con el motivo y la agenda se refresca.'),
        ('CU-05 Gestionar tutoría (tutor)', 'Tutor', 'Tener tutorías asignadas', ['El tutor abre su panel y ve las tutorías que le reservaron.', 'Confirma una pendiente.', 'Al llegar la hora la inicia y, al terminar, la completa.'], 'Un estudiante o un tutor pueden cancelar mientras la tutoría no esté completada.'),
        ('CU-06 Conversar con el asistente', 'Visitante o usuario', 'Ninguna', ['El usuario escribe su pregunta.', 'El motor normaliza el texto y puntúa los temas conocidos.', 'Se responde con el mejor tema, sugerencias y el JSON estructurado.'], 'Si ninguna intención supera el umbral, el asistente dice que no tiene esa información y sugiere temas que sí domina.'),
        ('CU-07 Calificar tutor', 'Estudiante', 'Haber tenido una tutoría', ['El estudiante elige el tutor y la tutoría.', 'Ingresa calificación y comentario.', 'La reseña queda guardada y alimenta el promedio del tutor y de la materia.'], 'Una calificación fuera del rango de 0 a 5 se rechaza.'),
        ('CU-08 Ver dashboard', 'Administrador', 'Permisos de staff', ['El administrador abre /dashboard.', 'La aplicación consulta /api/dashboard/resumen/.', 'Se muestran usuarios, tutores, materias, tutorías y gráficas.'], 'Un usuario sin permisos recibe un 403 y no ve datos.')]
    for nombre, actor, pre, pasos, alt in casos:
        H(nombre, 3)
        T(['Campo', 'Descripción'], [['Actor', actor], ['Precondición', pre], ['Flujo principal', '\n'.join(f'{i+1}. {x}' for i, x in enumerate(pasos))], ['Flujo alterno', alt]], [3.2, 12.6])

    # ---------------------------------------------------------------
    H('6. Diagrama de clases')
    P('El diagrama de clases muestra las entidades del dominio tal como están definidas en backend/api/models.py y las dos clases de servicio que concentran lógica sin tener tabla propia: el módulo de agenda y el motor del chatbot. Las flechas indican la dirección de la clave foránea y su multiplicidad.')
    FIG('docs/diagramas/04_diagrama_de_clases.png', 'Diagrama de clases del dominio y de los servicios.', 16)
    H('6.1 Descripción de las clases', 2, False)
    T(['Clase', 'Responsabilidad', 'Detalles relevantes'],
      [['User', 'Cuenta del sistema (modelo de Django)', 'Guarda usuario, correo, nombre y el hash de la contraseña'],
       ['UserProfile', 'Datos adicionales del usuario', 'Teléfono y banderas de verificación; se crea por señal al registrar un usuario'],
       ['PasswordResetToken', 'Token de recuperación', 'Tiene vencimiento y bandera de uso; is_valid() combina ambos'],
       ['Tutor', 'Perfil académico de un usuario', 'Especialidad, nivel, tarifa por hora, calificación, disponibilidad y materias'],
       ['Materia', 'Asignatura del catálogo', 'Nombre único y descripción'],
       ['Disponibilidad', 'Franja semanal de un tutor', 'Día de la semana de 0 a 6 y rango horario'],
       ['Tutoria', 'Sesión agendada', 'Calcula fecha_fin a partir de la duración al guardar; estados pendiente, confirmada, en progreso, completada y cancelada'],
       ['Resena', 'Opinión de un estudiante', 'Calificación y comentario ligados a tutor y tutoría'],
       ['GrupoTutoria', 'Sesión colectiva', 'Cupos máximos y disponibles, modalidad presencial, virtual o híbrida'],
       ['InscripcionGrupo', 'Inscripción de un estudiante a un grupo', 'Combinación grupo-estudiante única; registra asistencia'],
       ['agenda (módulo)', 'Cálculo de ventanas, horarios libres y validación de reservas', 'Funciones puras que reciben el tutor y la fecha; las usan la API y las pruebas'],
       ['ChatbotEngine', 'Motor del asistente', 'Normaliza texto, puntúa temas y arma la respuesta con su JSON']],
      [3.4, 5.2, 7.2], 'Clases del sistema')

    # ---------------------------------------------------------------
    H('7. Diagrama entidad-relación')
    P('El modelo relacional resultante tiene once tablas. La relación entre tutores y materias es de muchos a muchos y se resuelve con la tabla intermedia api_tutor_materias. Las tutorías son el punto de encuentro del modelo: apuntan a un tutor, a una materia y a un estudiante (la tabla de usuarios de Django).')
    FIG('docs/diagramas/03_modelo_entidad_relacion.png', 'Diagrama entidad-relación de la base de datos.', 16)
    H('7.1 Reglas de integridad', 2, False)
    B([('Unicidad: ', 'el nombre de la materia, el token de recuperación y la pareja grupo-estudiante en las inscripciones no se pueden repetir.'),
       ('Relación uno a uno: ', 'cada usuario tiene a lo sumo un perfil de usuario y un perfil de tutor.'),
       ('Borrado en cascada: ', 'al eliminar un usuario se eliminan su perfil, sus tokens y su perfil de tutor, con las tutorías asociadas. En la práctica el borrado de usuarios lo hace solo el administrador.'),
       ('Valores acotados: ', 'el día de la semana va de 0 (lunes) a 6 (domingo); el estado de las tutorías, el nivel del tutor y la modalidad del grupo son listas cerradas.')])

    # ---------------------------------------------------------------
    H('8. Diagramas de flujo')
    P('Se documentan tres flujos: el de agendar una tutoría, el del chatbot y el de recuperación de contraseña. Son los tres procesos con más decisiones y los que más errores produjeron durante el desarrollo.')
    H('8.1 Flujo para agendar una tutoría', 2, False)
    FIG_ALTO('docs/diagramas/05_flujo_agendar_tutoria.png', 'Diagrama de flujo para agendar una tutoría.', 17)
    P('El punto clave es la decisión del centro: el servidor valida tres condiciones antes de guardar. Que la validación viva en el servidor y no en la aplicación es deliberado. La agenda que ve el estudiante puede estar desactualizada si otra persona reservó mientras tanto; la última palabra siempre la tiene el backend.')
    H('8.2 Flujo del chatbot', 2, False)
    FIG_ALTO('docs/diagramas/06_flujo_chatbot.png', 'Diagrama de flujo del asistente conversacional.', 17)
    H('8.3 Flujo de recuperación de contraseña', 2, False)
    FIG_ALTO('docs/diagramas/07_flujo_recuperar_contrasena.png', 'Diagrama de flujo de la recuperación de contraseña.', 17)

    # ---------------------------------------------------------------
    H('9. Base de datos')
    P('La base de datos es PostgreSQL. Las tablas las crean las migraciones de Django a partir de backend/api/models.py. A continuación se presenta el diccionario de datos de cada tabla.')
    tablas = [
        ('auth_user', 'Usuarios de Django', [['id', 'entero (PK)', 'Identificador'], ['username', 'texto, único', 'Nombre de usuario'], ['email', 'texto', 'Correo electrónico'], ['first_name / last_name', 'texto', 'Nombre y apellido'], ['password', 'texto', 'Hash PBKDF2 de la contraseña'], ['is_staff / is_superuser', 'booleano', 'Permisos de administración'], ['is_active', 'booleano', 'Cuenta activa'], ['date_joined', 'fecha-hora', 'Fecha de registro']]),
        ('api_userprofile', 'Perfil ampliado', [['id', 'entero (PK)', 'Identificador'], ['user_id', 'FK uno a uno', 'Usuario dueño'], ['phone_number', 'texto', 'Teléfono'], ['email_verified', 'booleano', 'Correo verificado'], ['phone_verified', 'booleano', 'Teléfono verificado']]),
        ('api_passwordresettoken', 'Tokens de recuperación', [['id', 'entero (PK)', 'Identificador'], ['user_id', 'FK', 'Usuario que solicitó el cambio'], ['token', 'texto, único', 'Valor aleatorio entregado al usuario'], ['created_at', 'fecha-hora', 'Momento de creación'], ['expires_at', 'fecha-hora', 'Momento de vencimiento'], ['used', 'booleano', 'Si ya se consumió']]),
        ('api_materia', 'Catálogo de materias', [['id', 'entero (PK)', 'Identificador'], ['nombre', 'texto, único', 'Nombre de la asignatura'], ['descripcion', 'texto', 'Descripción corta'], ['creado_en', 'fecha-hora', 'Fecha de creación']]),
        ('api_tutor', 'Perfiles de tutor', [['id', 'entero (PK)', 'Identificador'], ['usuario_id', 'FK uno a uno', 'Usuario asociado'], ['especialidad', 'texto', 'Área principal'], ['nivel_experiencia', 'texto', 'principiante, intermedio, avanzado o experto'], ['bio', 'texto', 'Presentación del tutor'], ['tarifa_por_hora', 'decimal', 'Valor de la hora en pesos'], ['calificacion', 'decimal', 'Promedio de reseñas'], ['disponible', 'booleano', 'Si recibe reservas'], ['creado_en', 'fecha-hora', 'Fecha de creación']]),
        ('api_tutor_materias', 'Relación tutor-materia', [['id', 'entero (PK)', 'Identificador'], ['tutor_id', 'FK', 'Tutor'], ['materia_id', 'FK', 'Materia']]),
        ('api_disponibilidad', 'Franjas semanales', [['id', 'entero (PK)', 'Identificador'], ['tutor_id', 'FK', 'Tutor'], ['dia_semana', 'entero 0-6', '0 lunes … 6 domingo'], ['hora_inicio', 'hora', 'Inicio de la franja'], ['hora_fin', 'hora', 'Fin de la franja'], ['activo', 'booleano', 'Si la franja se usa']]),
        ('api_tutoria', 'Tutorías agendadas', [['id', 'entero (PK)', 'Identificador'], ['tutor_id', 'FK', 'Tutor asignado'], ['materia_id', 'FK', 'Materia tratada'], ['estudiante_id', 'FK', 'Estudiante que reserva'], ['fecha_inicio', 'fecha-hora', 'Inicio de la sesión'], ['fecha_fin', 'fecha-hora', 'Calculada: inicio + duración'], ['duracion_minutos', 'entero', 'Entre 15 y 240'], ['estado', 'texto', 'pendiente, confirmada, en_progreso, completada o cancelada'], ['lugar', 'texto', 'Sitio o enlace de la sesión'], ['tarifa', 'decimal', 'Valor calculado según la tarifa y la duración'], ['nota', 'texto', 'Observaciones']]),
        ('api_resena', 'Reseñas', [['id', 'entero (PK)', 'Identificador'], ['tutor_id', 'FK', 'Tutor reseñado'], ['estudiante_id', 'FK', 'Autor'], ['tutoria_id', 'FK (opcional)', 'Tutoría relacionada'], ['grupo_id', 'FK (opcional)', 'Grupo relacionado'], ['calificacion', 'decimal', 'Valor entre 0 y 5'], ['comentario', 'texto', 'Opinión']]),
        ('api_grupotutoria', 'Grupos de tutoría', [['id', 'entero (PK)', 'Identificador'], ['tutor_id', 'FK', 'Tutor a cargo'], ['materia_id', 'FK', 'Materia'], ['nombre', 'texto', 'Nombre del grupo'], ['cupos_maximos', 'entero', 'Capacidad'], ['cupos_disponibles', 'entero', 'Cupos restantes'], ['fecha_inicio', 'fecha-hora', 'Inicio'], ['modalidad', 'texto', 'presencial, virtual o híbrida'], ['estado', 'texto', 'programado, en curso, completado o cancelado']]),
        ('api_inscripciongrupo', 'Inscripciones a grupos', [['id', 'entero (PK)', 'Identificador'], ['grupo_id', 'FK', 'Grupo'], ['estudiante_id', 'FK', 'Estudiante'], ['estado', 'texto', 'Estado de la inscripción'], ['asistio', 'booleano', 'Asistencia registrada']])]
    for nombre, desc, filas in tablas:
        H(f'9.{tablas.index((nombre, desc, filas)) + 1} {nombre}', 2, False)
        P(desc + '.')
        T(['Campo', 'Tipo', 'Descripción'], filas, [4.5, 3.6, 7.7])

    H('9.12 Datos de partida', 2, False)
    P('Para que la plataforma no se vea vacía, un comando de carga inicial crea 25 materias (desde Matemáticas y Física hasta Derecho Constitucional, Bases de Datos y Arquitectura de Computadores), 20 tutores con nombres, especialidades y tarifas que van de 25.000 a 50.000 pesos por hora, 84 franjas de disponibilidad y 8 grupos de tutoría. Son datos de demostración; no corresponden a personas reales.')
    H('9.13 Consulta en tiempo real', 2, False)
    P('El script backend/db_live.py permite mirar la base de datos mientras el sistema funciona: lee los conteos de cada tabla y los últimos registros y los repite cada pocos segundos. Se usó durante las pruebas para comprobar que una tutoría agendada desde la aplicación aparecía de inmediato en la tabla api_tutoria.')
    CODE('cd backend\n..\\.venv\\Scripts\\python db_live.py          # consulta continua\n..\\.venv\\Scripts\\python db_live.py --once   # una sola lectura')

    # ---------------------------------------------------------------
    H('10. Referencia de la API')
    P('La API cuelga de /api/. Las listas devuelven la estructura paginada estándar de Django REST Framework (count, next, previous y results). Los parámetros ?page y ?page_size controlan la paginación; page_size admite hasta 100. La documentación interactiva se genera automáticamente y está disponible en /docs/.')
    FIG('docs/capturas/09_swagger.png', 'Swagger UI en /docs/ listando los endpoints de autenticación y chatbot.', 15.5)
    H('10.1 Endpoints', 2, False)
    with open(os.path.join(RAIZ, 'docs', '_schema.yml'), encoding='utf-8') as f:
        esq = yaml.safe_load(f)
    filas = []
    for ruta, ops in esq['paths'].items():
        if ruta == '/api/schema/':
            continue
        for m, o in ops.items():
            if m not in ('get', 'post', 'put', 'patch', 'delete'):
                continue
            k = f'{m.upper()} {ruta}'
            if k in DESC:
                filas.append([m.upper(), ruta, DESC[k][0], DESC[k][1]])
    T(['Método', 'Ruta', 'Descripción', 'Acceso'], filas, [1.5, 5.6, 6.2, 2.5], 'Endpoints principales', 8)
    P('Además de los endpoints listados, los recursos tutores, materias, tutorías, disponibilidades, reseñas, grupos, inscripciones y usuarios exponen el CRUD completo (GET, POST, PUT, PATCH y DELETE sobre /{id}/), sujeto a los permisos de cada uno. El esquema completo con todos los parámetros está en /api/schema/.')

    H('10.2 Ejemplos de uso', 2, False)
    H('Inicio de sesión', 3)
    P('Solicitud:')
    CODE('POST /api/auth/login/\nContent-Type: application/json\n\n{ "username": "demo_estudiante", "password": "••••••••" }')
    P('Respuesta (los tokens se recortan por legibilidad):')
    CODE('HTTP 200\n{\n  "access": "eyJhbGciOiJIUzI1NiIs...",\n  "refresh": "eyJhbGciOiJIUzI1NiIs...",\n  "user": { "id": 31, "username": "demo_estudiante", "email": "...", "first_name": "Laura", "last_name": "Gómez", "role": "estudiante" }\n}')
    H('Lista de tutores', 3)
    CODE('GET /api/tutores/?page_size=2\n\n' + ej('tutores', 45), 7)
    H('Disponibilidad mensual', 3)
    P('El parámetro mes tiene el formato AAAA-MM y duracion va en minutos (entre 15 y 240). La respuesta incluye solo los días con al menos un horario libre.')
    CODE('GET /api/tutores/1/disponibilidad_mensual/?mes=2026-11&duracion=60\n\n' + ej('agenda', 30))
    H('Agendar una tutoría', 3)
    CODE('POST /api/tutorias/\nAuthorization: Bearer <access>\n\n{\n  "tutor": 2,\n  "materia": 12,\n  "fecha_inicio": "2026-10-25T10:00:00-05:00",\n  "duracion_minutos": 60,\n  "lugar": "Biblioteca, sede Fusagasugá"\n}\n\nHTTP 201  → la tutoría queda en estado "pendiente"\nHTTP 400  → { "fecha_inicio": ["Ese horario está fuera de la disponibilidad del tutor. Elige otro de la agenda."] }')
    H('Conversación con el asistente', 3)
    CODE('POST /api/chatbot/chat/\n{ "message": "¿Dónde queda la sede principal de la Universidad de Cundinamarca?" }\n\n')
    CODE(ej('chat', 30))

    # ---------------------------------------------------------------
    H('11. Seguridad')
    H('11.1 Autenticación', 2, False)
    P('La API usa JSON Web Tokens mediante SimpleJWT. Al iniciar sesión el cliente recibe un token de acceso con vigencia de 24 horas y un token de refresco con vigencia de 7 días. El cliente envía el de acceso en el encabezado Authorization con el prefijo Bearer. Cuando el de acceso vence, la web y la aplicación móvil lo renuevan con el refresco sin pedir de nuevo la contraseña.')
    H('11.2 Contraseñas', 2, False)
    P('Las contraseñas se guardan con el hash PBKDF2 que Django aplica por defecto. Además se activaron los validadores estándar: longitud mínima, que no se parezca a los datos del usuario, que no sea una contraseña común y que no sea solo numérica. Los mensajes de esos validadores se traducen al español.')
    H('11.3 Recuperación de contraseña', 2, False)
    P('El proceso original de la aplicación móvil mostraba la pantalla de recuperación pero no enviaba nada al servidor; durante las pruebas se detectó y se reemplazó por un flujo real. El servidor crea un token aleatorio con vencimiento, lo asocia al usuario y lo invalida tras el primer uso. En el entorno de demostración la API puede devolver ese token en la respuesta (variable PASSWORD_RESET_SHOW_TOKEN) para poder probar sin servidor de correo; en un entorno de producción esa variable debe estar apagada y el token viajar solo por correo.')
    H('11.4 Permisos por rol', 2, False)
    T(['Recurso', 'Visitante', 'Estudiante', 'Tutor', 'Administrador'],
      [['Catálogo de tutores y materias', 'Lectura', 'Lectura', 'Lectura', 'Lectura y escritura'],
       ['Agenda mensual', 'Lectura', 'Lectura', 'Lectura', 'Lectura'],
       ['Tutorías propias', '—', 'Crear, ver y cancelar', 'Ver, confirmar, iniciar, completar', 'Todo'],
       ['Reseñas', 'Lectura', 'Crear', 'Lectura', 'Todo'],
       ['Usuarios', '—', '—', '—', 'Todo'],
       ['Dashboard', '—', '—', '—', 'Lectura']],
      [4.2, 2.4, 3.2, 3.4, 2.6], 'Matriz de permisos')
    H('11.5 Otras medidas y riesgos pendientes', 2, False)
    B(['CORS restringido a los orígenes necesarios y secretos en variables de entorno (backend/.env, que no se versiona).',
       'Validación de entrada en serializadores; el ORM de Django evita la inyección SQL por construcción.',
       'Pendiente: servir todo por HTTPS. Hoy el tráfico viaja en texto claro, por lo que las credenciales podrían ser interceptadas en una red no confiable. Para la demostración se aceptó el riesgo; para producción es obligatorio contar con un dominio y un certificado.',
       'Pendiente: limitar la cantidad de intentos de inicio de sesión y de solicitudes de recuperación por dirección IP.'])
