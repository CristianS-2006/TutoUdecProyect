from docgen_base import *


def parte1():
    H('1. Introducción')
    P('TutoUdec nació de una situación bastante común en cualquier universidad: los estudiantes que van atrasados en una materia saben que existen compañeros que la dominan, pero no tienen una forma ordenada de encontrarlos, de saber cuándo están libres ni de acordar una hora sin cruzar veinte mensajes por WhatsApp. Del otro lado, los estudiantes que sí dominan una materia y estarían dispuestos a ayudar no tienen un lugar donde mostrarse ni donde fijar sus horarios y su tarifa.')
    P('Este documento recoge todo lo que se construyó para resolver ese problema en la Universidad de Cundinamarca: una plataforma de tutorías con una API en Django, una aplicación web en Vue 3, una aplicación móvil en React Native (Expo), una base de datos PostgreSQL en la nube, un asistente conversacional que conoce la universidad y un análisis exploratorio de los datos. También documenta cómo se probó, cómo se desplegó en Azure, qué problemas aparecieron en el camino y cómo se resolvieron.')
    P('El texto está pensado para dos tipos de lector. El primero es quien evalúa el trabajo y necesita ver que cada requisito se cumplió, con evidencia. El segundo es quien tendrá que mantener o ampliar el sistema y necesita entender las decisiones de diseño sin leer todo el código. Por eso el documento mezcla explicaciones, diagramas, capturas de la ejecución, tablas de referencia y, al final, anexos con el código fuente más relevante.')

    H('1.1 Planteamiento del problema', 2, False)
    P('Antes de la plataforma, la búsqueda de un tutor dependía del boca a boca. Los problemas concretos que se identificaron fueron estos:')
    B(['No existe un directorio único de tutores con su especialidad, su nivel de experiencia y su tarifa.',
       'Los horarios se acuerdan por mensajes privados, lo que provoca choques: dos estudiantes pueden quedar con el mismo tutor a la misma hora sin saberlo.',
       'No hay historial. Si una tutoría se cancela o se completa, no queda registro de nada, y tampoco se pueden dejar reseñas que ayuden a otros estudiantes a escoger.',
       'Quien llega nuevo a la universidad no sabe a quién preguntarle sobre trámites, calendario, sedes o programas, y termina buscando la misma información en cuatro sitios distintos.'])

    H('1.2 Objetivo general', 2, False)
    P('Desarrollar y desplegar una plataforma multiplataforma (API, web y móvil) que permita a los estudiantes de la Universidad de Cundinamarca encontrar tutores, consultar su disponibilidad mensual, agendar tutorías sin choques de horario y resolver dudas generales mediante un asistente conversacional.')

    H('1.3 Objetivos específicos', 2, False)
    N(['Diseñar un modelo de datos relacional que represente usuarios, tutores, materias, tutorías, disponibilidad, reseñas y grupos de tutoría.',
       'Exponer una API REST autenticada con JWT, con paginación, filtros y documentación interactiva.',
       'Construir una aplicación web y una aplicación móvil que consuman esa misma API y ofrezcan registro, inicio de sesión, recuperación de contraseña, catálogo de tutores y materias, agenda y chatbot.',
       'Implementar un cálculo de disponibilidad mensual y una validación de reservas que impida horarios pasados, fuera de la disponibilidad del tutor o superpuestos con otra tutoría.',
       'Incorporar un asistente conversacional con conocimiento de la Universidad de Cundinamarca, que responda de forma clara y que admita cuando no sabe.',
       'Realizar un análisis exploratorio de los datos con gráficas y un tablero para el administrador.',
       'Desplegar el backend, la web y la base de datos en Azure y generar un APK instalable de la aplicación móvil.',
       'Validar el sistema con pruebas automatizadas y con pruebas de extremo a extremo contra el entorno desplegado.'])

    H('1.4 Alcance y limitaciones', 2, False)
    P('El alcance cubre los ocho módulos funcionales descritos en el capítulo 3: autenticación, recuperación de contraseña, tutores, materias, tutorías con agenda mensual, reseñas, grupos de tutoría y chatbot, más el tablero de análisis para administradores. Quedan por fuera, de forma deliberada, los pagos en línea, las videollamadas integradas y las notificaciones push, porque el tiempo disponible se dedicó a que lo esencial funcionara bien en lugar de agregar piezas a medias.')
    P('Hay tres limitaciones que conviene decir desde ya, porque más adelante se retoman. La primera: el servidor de demostración atiende por HTTP y no por HTTPS, ya que no cuenta con un dominio propio para emitir un certificado. La segunda: el envío de correos de recuperación depende de credenciales SMTP; para la demostración el sistema puede devolver el token en la respuesta, algo que en producción debe apagarse. La tercera: el APK se compiló y se verificó revisando el paquete generado, pero no se ejecutó sobre un teléfono físico durante la elaboración de este documento, por lo que las capturas de ejecución que se muestran son de la aplicación web desplegada.')

    H('1.5 Metodología de trabajo', 2, False)
    P('El proyecto se trabajó de forma iterativa. Cada iteración tomó un conjunto pequeño de requisitos, los implementó de extremo a extremo (modelo, API, interfaz), los probó y los desplegó antes de pasar a lo siguiente. Esa forma de trabajo explica por qué la historia del proyecto se lee como una secuencia de entregas y no como una cascada de fases.')
    T(['Iteración', 'Contenido principal', 'Resultado verificable'],
      [['1', 'Modelos, API base, autenticación JWT, web y móvil iniciales', 'Registro, inicio de sesión y catálogo funcionando'],
       ['2', 'Chatbot con conocimiento de la UdeC y modo JSON empresarial 5.0', 'Respuestas con fuentes y respuesta honesta cuando no sabe'],
       ['3', 'Despliegue en Azure (VM, nginx, gunicorn, PostgreSQL) y corrección del error 500', 'API y web accesibles por IP pública'],
       ['4', 'Análisis exploratorio (EDA) y tablero de administración', 'Seis gráficas y dashboard con métricas reales'],
       ['5', 'Corrección del APK: HTTP en texto claro y recuperación de contraseña real', 'Registro de estudiante y tutor desde el APK'],
       ['6', 'Agenda mensual, validación de reservas, materias con valoración, traducción total al español', 'Tutorías agendadas y persistidas en la nube'],
       ['7', 'Documentación final, diagramas y capturas de ejecución', 'Este documento']],
      [1.8, 8.5, 5.5], 'Iteraciones del proyecto')

    H('1.6 Estructura del documento', 2, False)
    P('El capítulo 2 describe el contexto y los actores. El 3 lista los requisitos. El 4 presenta la arquitectura y la tecnología. Los capítulos 5 a 8 contienen los diagramas de casos de uso, de clases, entidad-relación y de flujo. El 9 documenta la base de datos, el 10 la API y el 11 la seguridad. Los capítulos 12 a 15 explican el chatbot, la agenda mensual, la aplicación web y la aplicación móvil. El 16 reúne las capturas de la ejecución. Los capítulos 17 y 18 tratan el análisis de datos y las pruebas. El 19 es el manual de instalación y operación, el 20 el manual de usuario, el 21 la bitácora de problemas y el 22 la verificación de requisitos. Cierran el documento las conclusiones, el trabajo futuro, el glosario, la bibliografía y los anexos con código fuente.')

    # ---------------------------------------------------------------
    H('2. Contexto y actores')
    H('2.1 La Universidad de Cundinamarca', 2, False)
    P('La Universidad de Cundinamarca (UdeC) es una institución pública de educación superior del departamento de Cundinamarca, con sede principal en Fusagasugá y extensiones y seccionales en varios municipios, entre ellos Girardot, Zipaquirá, Ubaté, Soacha, Facatativá y Chía. Tiene programas en áreas como ingeniería, ciencias administrativas, ciencias agropecuarias, ciencias de la salud, ciencias del deporte, ciencias sociales y educación. Es en este contexto, con estudiantes repartidos en varias sedes, donde una plataforma que permita agendar tutorías sin coincidir físicamente en un solo lugar resulta especialmente útil: de ahí que la modalidad virtual y la presencial convivan en el diseño.')
    P('El asistente conversacional incluye información de la universidad (sedes, programas, calendario y trámites generales) que se recopiló de los textos que el equipo tenía a mano. Es información de referencia y no sustituye los canales oficiales; cuando una pregunta sale de ese conocimiento, el asistente lo dice.')

    H('2.2 Actores del sistema', 2, False)
    T(['Actor', 'Descripción', 'Qué hace en la plataforma'],
      [['Visitante', 'Persona sin sesión iniciada', 'Ve el catálogo de tutores y materias, conversa con el chatbot, se registra o inicia sesión'],
       ['Estudiante', 'Usuario registrado con rol estudiante', 'Consulta la agenda mensual de un tutor, agenda y cancela tutorías, deja reseñas, se inscribe en grupos'],
       ['Tutor', 'Usuario registrado con perfil de tutor', 'Mantiene su perfil y su disponibilidad, confirma, inicia y completa las tutorías que le reservan'],
       ['Administrador', 'Usuario con permisos de staff o superusuario', 'Gestiona usuarios, materias y tutores desde el panel de Django y consulta el dashboard de métricas'],
       ['Sistema externo', 'Servicio de correo SMTP', 'Entrega los mensajes de recuperación de contraseña']],
      [3, 5.5, 7.3], 'Actores del sistema')

    H('2.3 Historias de usuario principales', 2, False)
    T(['Código', 'Historia', 'Criterio de aceptación'],
      [['HU-01', 'Como visitante quiero registrarme para poder agendar tutorías.', 'Con los campos válidos se crea el usuario y se recibe un token; con datos inválidos el mensaje de error está en español.'],
       ['HU-02', 'Como usuario quiero recuperar mi contraseña si la olvidé.', 'Se solicita el restablecimiento con el correo, se recibe un token y con él se fija una nueva contraseña; el token deja de servir después de usarse.'],
       ['HU-03', 'Como estudiante quiero ver los tutores de una materia con su valoración.', 'La lista muestra nombre, especialidad, tarifa, calificación y disponibilidad, paginada de 10 en 10.'],
       ['HU-04', 'Como estudiante quiero ver la disponibilidad de todo el mes de un tutor.', 'El calendario marca los días con cupo y, al elegir un día, lista los horarios libres según la duración.'],
       ['HU-05', 'Como estudiante quiero agendar una tutoría en un horario libre.', 'La tutoría queda en estado pendiente y aparece en «Mis tutorías»; un horario ocupado se rechaza.'],
       ['HU-06', 'Como tutor quiero confirmar, iniciar y completar mis tutorías.', 'Cada cambio de estado queda guardado y visible para el estudiante.'],
       ['HU-07', 'Como estudiante quiero preguntarle al chatbot por la universidad.', 'Responde de forma coherente y, si no tiene la información, lo reconoce sin inventar.'],
       ['HU-08', 'Como administrador quiero ver métricas del sistema.', 'El dashboard muestra usuarios, tutores, materias y tutorías con datos reales de la base.']],
      [1.6, 7, 7.2], 'Historias de usuario')

    # ---------------------------------------------------------------
    H('3. Requisitos del sistema')
    H('3.1 Requisitos funcionales', 2, False)
    T(['ID', 'Requisito', 'Módulo', 'Estado'],
      [['RF-01', 'Registrar usuarios con nombre, correo, usuario y contraseña, validando los datos', 'Autenticación', 'Cumplido'],
       ['RF-02', 'Iniciar sesión y mantenerla con tokens JWT (acceso y refresco)', 'Autenticación', 'Cumplido'],
       ['RF-03', 'Recuperar la contraseña mediante un token de un solo uso con vencimiento', 'Autenticación', 'Cumplido'],
       ['RF-04', 'Cambiar la contraseña estando autenticado', 'Autenticación', 'Cumplido'],
       ['RF-05', 'Listar tutores con paginación, búsqueda y filtros', 'Tutores', 'Cumplido'],
       ['RF-06', 'Mostrar el detalle del tutor con materias, reseñas recientes y total de reseñas', 'Tutores', 'Cumplido'],
       ['RF-07', 'Listar materias con descripción, valoración promedio y número de tutores', 'Materias', 'Cumplido'],
       ['RF-08', 'Consultar la disponibilidad mensual de un tutor para una duración dada', 'Agenda', 'Cumplido'],
       ['RF-09', 'Agendar una tutoría validando fecha futura, ventana de disponibilidad y choques', 'Tutorías', 'Cumplido'],
       ['RF-10', 'Cambiar el estado de una tutoría (confirmar, iniciar, completar, cancelar)', 'Tutorías', 'Cumplido'],
       ['RF-11', 'Registrar reseñas con calificación y comentario', 'Reseñas', 'Cumplido'],
       ['RF-12', 'Crear grupos de tutoría con cupos e inscribir estudiantes', 'Grupos', 'Cumplido'],
       ['RF-13', 'Responder preguntas sobre la UdeC y sobre la plataforma en lenguaje natural', 'Chatbot', 'Cumplido'],
       ['RF-14', 'Devolver la respuesta del chatbot también en formato JSON estructurado (empresarial 5.0)', 'Chatbot', 'Cumplido'],
       ['RF-15', 'Mostrar un dashboard con métricas para el administrador', 'Analítica', 'Cumplido'],
       ['RF-16', 'Ofrecer una aplicación móvil que consuma la misma API', 'Móvil', 'Cumplido']],
      [1.6, 8.6, 3, 2.6], 'Requisitos funcionales')

    H('3.2 Requisitos no funcionales', 2, False)
    T(['ID', 'Requisito', 'Cómo se atiende'],
      [['RNF-01', 'Toda la interfaz y los mensajes de error deben estar en español', 'Textos de la web y del móvil en español; LANGUAGE_CODE es-co; mensajes de validación redactados en español'],
       ['RNF-02', 'La base de datos debe estar en la nube', 'PostgreSQL en Azure, accesible solo desde el servidor de aplicación'],
       ['RNF-03', 'Las contraseñas no se guardan en claro', 'Hash PBKDF2 de Django y validadores de contraseña'],
       ['RNF-04', 'Las rutas sensibles exigen autenticación', 'JWT en el encabezado Authorization; permisos por rol en el backend'],
       ['RNF-05', 'La respuesta de la API debe ser ágil con listas grandes', 'Paginación de 10 elementos con tope de 100 y select_related en las consultas'],
       ['RNF-06', 'La API debe estar documentada', 'Esquema OpenAPI y Swagger UI en /docs/'],
       ['RNF-07', 'El sistema debe poder reinstalarse siguiendo una guía', 'Capítulo 19 y README del repositorio'],
       ['RNF-08', 'La zona horaria debe ser la de Colombia', 'TIME_ZONE America/Bogota']],
      [1.8, 5.6, 8.4], 'Requisitos no funcionales')

    # ---------------------------------------------------------------
    H('4. Arquitectura y tecnología')
    H('4.1 Visión general', 2, False)
    P('La plataforma sigue una arquitectura cliente-servidor en tres capas. Dos clientes, uno web y uno móvil, hablan con una única API REST. La API contiene toda la lógica de negocio (validación de reservas, cálculo de agenda, chatbot) y es la única que toca la base de datos. Esa decisión, que parece obvia, tiene una consecuencia práctica importante: cualquier regla que se corrija en el backend se corrige a la vez para la web y para el móvil.')
    FIG('docs/diagramas/01_arquitectura.png', 'Arquitectura general de TutoUdec: clientes, API y base de datos.', 15.5)
    P('El servidor de aplicación corre en una máquina virtual de Azure. El tráfico entra por nginx en el puerto 80; nginx entrega directamente los archivos estáticos de la aplicación web y de Django, y reenvía a gunicorn (en el puerto local 8000) las rutas /api/, /admin/ y /docs/. Gunicorn ejecuta la aplicación Django, que se conecta a PostgreSQL.')

    H('4.2 Pila tecnológica', 2, False)
    T(['Capa', 'Tecnología', 'Versión', 'Para qué se usa'],
      [['Backend', 'Python / Django', '6.0.3', 'Modelos, ORM, administración y lógica de negocio'],
       ['Backend', 'Django REST Framework', '3.14.0', 'Serializadores, vistas y rutas de la API'],
       ['Backend', 'SimpleJWT', '5.3.1', 'Tokens de acceso y refresco'],
       ['Backend', 'drf-spectacular', '0.27.2', 'Esquema OpenAPI y Swagger UI'],
       ['Backend', 'gunicorn', '23.0.0', 'Servidor de aplicación WSGI'],
       ['Datos', 'PostgreSQL', '14+', 'Base de datos relacional en la nube'],
       ['Web', 'Vue', '^3.5.29', 'Interfaz reactiva'],
       ['Web', 'Pinia', '^3.0.4', 'Estado global (sesión)'],
       ['Web', 'Vue Router', '^5.0.3', 'Navegación'],
       ['Web', 'Axios', '^1.13.6', 'Cliente HTTP'],
       ['Web', 'Vite', '^7.3.1', 'Empaquetado y servidor de desarrollo'],
       ['Móvil', 'Expo', '~54.0.37', 'Entorno de desarrollo y compilación'],
       ['Móvil', 'React Native / React', '0.81.5 / 19.1.0', 'Interfaz nativa'],
       ['Móvil', 'React Navigation', 'v7', 'Navegación entre pantallas'],
       ['Análisis', 'pandas, matplotlib', 'actuales', 'Análisis exploratorio y gráficas'],
       ['Infra', 'nginx, systemd', 'del sistema', 'Proxy inverso y supervisión del servicio'],
       ['Infra', 'Azure VM', 'Ubuntu', 'Alojamiento del backend y de la web'],
       ['CI/CD', 'GitHub Actions, EAS Build', '—', 'Flujos de despliegue y compilación del APK']],
      [2.2, 4.3, 3.2, 6.1], 'Tecnologías empleadas')
    P('Las versiones de Vue, Pinia, Vue Router, Axios, Vite, Expo y React Native son las declaradas en los archivos package.json del repositorio. Las del backend están fijadas en backend/requirements.txt.', cursiva=True)

    H('4.3 Estructura del repositorio', 2, False)
    CODE('''TutoUdecProyect/
├── backend/            API Django (settings, urls, api/ con modelos, vistas, agenda, chatbot)
│   └── api/            models.py, serializers.py, views.py, agenda.py, chatbot_engine.py ...
├── web/                Aplicación Vue 3 (src/views, src/router, src/stores)
├── mobile/             Aplicación Expo / React Native (src/screens, src/services)
├── analytics/          Análisis exploratorio (script, gráficas y informe)
├── deploy/             Configuración de nginx y servicio gunicorn
├── docs/               Diagramas, capturas y generadores de este documento
├── .github/workflows/  Flujos de GitHub Actions
└── README.md''', 9)

    H('4.4 Entorno de despliegue', 2, False)
    FIG('docs/diagramas/08_despliegue.png', 'Diagrama de despliegue en Azure.', 15.5)
    T(['Elemento', 'Valor'],
      [['Grupo de recursos', 'Backend_group'],
       ['Máquina virtual', 'Backend (Ubuntu), IP pública 4.206.201.129'],
       ['Servidor web', 'nginx, puerto 80, raíz /var/www/tutoudec'],
       ['Servidor de aplicación', 'gunicorn en 127.0.0.1:8000 gestionado por systemd'],
       ['Estáticos de Django', '/home/cristian/TutoUdecProyect/staticfiles servidos por nginx en /static/'],
       ['Base de datos', 'PostgreSQL en Azure (credenciales en backend/.env, fuera del repositorio)'],
       ['Dirección de la web', 'http://4.206.201.129'],
       ['Dirección de la API', 'http://4.206.201.129/api/'],
       ['Documentación interactiva', 'http://4.206.201.129/docs/']],
      [5, 10.8], 'Datos del entorno desplegado')
