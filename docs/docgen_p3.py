from docgen_p2 import ej
from docgen_base import *


def parte3():
    # ---------------------------------------------------------------
    H('12. Asistente conversacional')
    P('El chatbot es la parte del sistema que más se parece a «una IA», y conviene explicar con honestidad cómo funciona. No es un modelo de lenguaje generativo: es un motor de reglas y conocimiento propio, escrito en Python, que reconoce la intención de una pregunta, la responde con información verificada que está en el repositorio y devuelve, además, un objeto JSON estructurado. Se diseñó así por tres razones: no depende de un servicio externo de pago, sus respuestas son predecibles y revisables, y puede decir «no lo sé» en lugar de inventar.')
    H('12.1 Cómo decide qué responder', 2, False)
    FIG_ALTO('docs/diagramas/06_flujo_chatbot.png', 'Flujo de decisión del asistente (se repite aquí para consulta rápida).', 14)
    N(['El mensaje se normaliza: se pasa a minúsculas, se quitan tildes y signos y se separa en palabras.',
       'Cada tema del motor tiene una lista de palabras clave. Se calcula un puntaje por tema; las palabras demasiado genéricas («hora», «clase», «app», «proyecto») pesan poco para que no disparen respuestas equivocadas.',
       'Si el mejor puntaje supera el umbral, se arma la respuesta del tema y se agregan sugerencias de seguimiento.',
       'Si ningún tema alcanza el umbral, se responde que no se tiene esa información y se ofrecen preguntas que sí se pueden contestar.',
       'El historial de intenciones previas que envía el cliente permite resolver preguntas de seguimiento como «¿y en Girardot?».'])
    H('12.2 Conocimiento incluido', 2, False)
    T(['Grupo', 'Temas'],
      [['Universidad de Cundinamarca', 'Información general, historia, misión y visión, sedes y extensiones, programas por facultad, carreras por sede, posgrados, admisión, calendario, matrícula y costos, gratuidad, bienestar universitario, acreditación, directivos, contacto, transparencia y ambiente, y la aclaración sobre la Universidad Colegio Mayor de Cundinamarca (otra institución)'],
       ['Plataforma TutoUdec', 'Qué es TutoUdec, cómo registrarse, cómo agendar una tutoría, cómo funciona la agenda mensual, cómo recuperar la contraseña, cómo calificar a un tutor, cómo ser tutor, tarifas y modalidades'],
       ['Conversación', 'Saludos, despedidas, agradecimientos y preguntas sobre qué sabe hacer el asistente']],
      [4.6, 11.2], 'Conocimiento del asistente')
    P('La información de la universidad quedó en un archivo aparte (backend/api/udec_knowledge.py) para poder actualizarla sin tocar la lógica. Los datos que cambian con frecuencia, como fechas del calendario o costos, llevan al final una nota que recomienda confirmarlos en el sitio oficial.')
    H('12.3 Respuesta en JSON empresarial 5.0', 2, False)
    P('Además del texto, cada respuesta incluye un objeto response_json con un esquema fijo. La idea de «empresarial 5.0» se tomó de las propuestas de la Industria 5.0, que ponen a la persona en el centro y piden tecnología explicable, sostenible y ética. Se tradujo en campos concretos:')
    T(['Campo', 'Contenido'],
      [['standard', 'Siempre «empresarial-5.0»'],
       ['mode / provider', 'Cómo se generó la respuesta (reglas locales o, si se configura, un proveedor externo)'],
       ['answer', 'Texto de la respuesta'],
       ['intent', 'Intención detectada'],
       ['confidence', 'Valor entre 0 y 1 derivado del puntaje del tema'],
       ['unknown', 'Verdadero cuando el asistente reconoce que no sabe'],
       ['follow_up_question', 'Pregunta de seguimiento sugerida'],
       ['suggestions', 'Lista de preguntas relacionadas'],
       ['business_5_0', 'Cinco notas: centrado en el ser humano, basado en datos, sostenible, automatizado y con IA ética']],
      [4.2, 11.6], 'Campos del JSON')
    CODE(ej('chat2', 40))
    P('El ejemplo anterior corresponde a una pregunta fuera de alcance («¿cuál es la capital de Japón?»). El asistente marca unknown en verdadero, no inventa una respuesta y propone temas que sí domina. Ese comportamiento fue una petición explícita del cliente y está cubierto por la prueba test_unknown_question_admits_ignorance.')
    FIG('docs/capturas/06_chatbot.png', 'Chatbot de la web respondiendo con honestidad a una pregunta fuera de su conocimiento.', 14.5)
    H('12.4 Modo con proveedor externo', 2, False)
    P('El módulo ai_chatbot.py deja preparada la conexión con la API de OpenAI (por defecto el modelo gpt-4o-mini). Solo se activa si AI_ENABLED es verdadero y existe OPENAI_API_KEY; en ese caso el asistente puede apoyarse en el modelo y enriquecer la respuesta. Si no se definen, o si el proveedor falla, el sistema cae al motor de reglas y la respuesta sigue saliendo. Esta redundancia evita que una caída externa deje al chat mudo.')

    # ---------------------------------------------------------------
    H('13. Agenda mensual y reservas')
    P('Este fue el cambio funcional más grande de la última etapa. La versión inicial mostraba la disponibilidad como una lista de franjas por día de la semana, lo que obligaba al estudiante a hacer cálculos mentales («el martes de la próxima semana, ¿cuál fecha es?»). La versión final muestra un calendario del mes completo, con los días que tienen cupo, y deja elegir el horario y registrar la tutoría desde la misma pantalla.')
    H('13.1 Algoritmo de disponibilidad', 2, False)
    N(['Se obtienen las franjas semanales activas del tutor. Si no tiene ninguna, se usa el horario por defecto (lunes a viernes, de 8:00 a 18:00).',
       'Para cada día del mes se toman las franjas que corresponden a su día de la semana.',
       'Cada franja se parte en bloques de la duración pedida (entre 15 y 240 minutos).',
       'Se descartan los bloques que ya pasaron y los que se cruzan con una tutoría activa del tutor (estados pendiente, confirmada o en progreso).',
       'Los días con al menos un bloque libre se devuelven con su lista de horarios en formato HH:MM, en la zona horaria de Colombia.'])
    H('13.2 Validación al reservar', 2, False)
    T(['Regla', 'Mensaje cuando falla'],
      [['El estudiante no puede ser el mismo tutor', 'No puedes agendar una tutoría contigo mismo.'],
       ['El tutor debe estar marcado como disponible', 'El tutor no está disponible por ahora.'],
       ['La fecha debe ser futura', 'La fecha y hora deben ser futuras.'],
       ['El horario debe estar dentro de una franja del tutor', 'Ese horario está fuera de la disponibilidad del tutor. Elige otro de la agenda.'],
       ['No puede haber otra tutoría activa que se cruce', 'El tutor ya tiene una tutoría en ese horario. Elige otro.']],
      [7, 8.8], 'Reglas de validación de reservas')
    P('El administrador puede saltarse estas reglas, algo útil para corregir datos o registrar una tutoría que ocurrió por fuera de la plataforma.')
    H('13.3 Fragmento del código', 2, False)
    CODE(LEER('backend/api/agenda.py')[:2600] + '\n...', 7.5)
    P('El archivo completo está en el anexo A.3. Está escrito con funciones puras para poder probarlo sin servidor: las pruebas de test_disponibilidad_mensual, test_reserva_y_conflicto y test_rechaza_pasado ejercitan justo esas funciones.')

    # ---------------------------------------------------------------
    H('14. Aplicación web')
    P('La aplicación web está hecha con Vue 3 y Vite. Usa Pinia para guardar la sesión, Vue Router para navegar y Axios para llamar a la API. En producción se compila a archivos estáticos que nginx sirve directamente, sin pasar por Django.')
    T(['Ruta', 'Vista', 'Qué muestra', 'Acceso'],
      [['/', 'HomeView', 'Presentación de la plataforma y accesos rápidos', 'Pública'],
       ['/tutores', 'TutoresView', 'Lista paginada de tutores con calificación, tarifa y disponibilidad', 'Pública'],
       ['/materias', 'MateriasView', 'Catálogo de materias con descripción y número de tutorías', 'Pública'],
       ['/chatbot', 'ChatbotView', 'Conversación con el asistente', 'Pública'],
       ['/sesion', 'Inicio de sesión', 'Formulario de acceso', 'Pública'],
       ['/formulario', 'Registro', 'Formulario de alta de usuario', 'Pública'],
       ['/tutorias', 'TutoriasView', 'Tutorías del usuario autenticado', 'JWT'],
       ['/dashboard', 'DashboardView', 'Métricas y gráficas para el administrador', 'Administrador']],
      [2.4, 3.2, 7.4, 2.8], 'Rutas de la aplicación web')
    P('La navegación protegida funciona con una guarda global del router: si la ruta exige sesión y no hay token, redirige al inicio de sesión; si exige permisos de administrador y el usuario no los tiene, lo devuelve al inicio.')
    P('Un detalle visible en las capturas es que el contenido de la web ocupa un ancho fijo a la izquierda en pantallas grandes. Es una limitación de diseño que no afecta a la funcionalidad; en pantallas de móvil la interfaz se adapta bien (figura de la sección 16).')

    # ---------------------------------------------------------------
    H('15. Aplicación móvil')
    P('La aplicación móvil está hecha con React Native sobre Expo. Comparte con la web el mismo backend y las mismas reglas. Se distribuye como un archivo APK generado con EAS Build, el servicio de compilación de Expo.')
    H('15.1 Pantallas', 2, False)
    T(['Pantalla', 'Archivo', 'Función'],
      [['Inicio de sesión', 'auth/LoginScreen.js', 'Acceso con usuario y contraseña; enlace a la recuperación'],
       ['Registro', 'auth/RegisterScreen.js', 'Alta de estudiante o tutor con validación de campos'],
       ['Recuperar contraseña', 'auth/ForgotPasswordScreen.js', 'Solicita el token y fija la contraseña nueva'],
       ['Cambiar contraseña', 'auth/ChangePasswordScreen.js', 'Cambio estando autenticado'],
       ['Inicio', 'main/HomeScreen.js', 'Resumen del estudiante, accesos y próximas tutorías'],
       ['Inicio del tutor', 'main/TutorHomeScreen.js', 'Panel del tutor con sus tutorías por estado'],
       ['Tutores', 'main/TutoresScreen.js', 'Lista con búsqueda y calificación'],
       ['Detalle del tutor', 'main/TutorDetailScreen.js', 'Perfil, materias, reseñas, calendario mensual y reserva'],
       ['Materias', 'main/MateriasScreen.js', 'Tarjetas con descripción, valoración y total de tutores'],
       ['Detalle de materia', 'main/MateriaDetailScreen.js', 'Descripción, valoración y tutores que la dictan'],
       ['Mis tutorías', 'main/TutoriasScreen.js', 'Historial y estados de las tutorías'],
       ['Nueva tutoría', 'main/CreateTutoriaScreen.js', 'Formulario alternativo de reserva'],
       ['Chatbot', 'main/ChatbotScreen.js', 'Conversación con el asistente'],
       ['Perfil', 'main/ProfileScreen.js', 'Datos de la cuenta y cierre de sesión']],
      [3.4, 5.6, 6.8], 'Pantallas de la aplicación móvil')
    H('15.2 Cliente HTTP y sesión', 2, False)
    P('Todas las llamadas pasan por un único cliente Axios (services/api.js) que agrega el token a cada solicitud. Si la API responde 401 porque el token venció, el cliente intenta renovarlo con el refresco y repite la solicitud; si el refresco también falla, borra los tokens y obliga a iniciar sesión de nuevo. La sesión se guarda en el almacenamiento local del teléfono.')
    H('15.3 Calendario mensual en el perfil del tutor', 2, False)
    P('En el perfil de cada tutor aparece un calendario del mes con los días que tienen horarios libres. El estudiante puede cambiar de mes, elegir la duración, tocar un día y escoger una hora; al confirmar, la aplicación crea la tutoría. Si el servidor rechaza la reserva, se muestra su mensaje en español y se recarga la agenda.')
    H('15.4 Materias con la misma presentación que los tutores', 2, False)
    P('Las materias se rediseñaron como tarjetas parecidas a las de los tutores: nombre, descripción, valoración con estrellas y número de tutores. Esa valoración la calcula el backend como el promedio de la calificación de los tutores que dictan la materia. En el detalle de la materia aparecen los tutores con el mismo estilo de tarjeta.')
    H('15.5 Compilación del APK', 2, False)
    CODE('cd mobile\nnpm install\nnpx eas-cli login\nnpx eas-cli build --platform android --profile preview')
    P('El perfil preview genera un APK instalable directamente. Android bloquea por defecto las conexiones HTTP sin cifrar, y el servidor de demostración atiende por HTTP; por eso la configuración de compilación habilita el tráfico en texto claro mediante expo-build-properties. Esta fue la causa del error de registro que se reportó en una de las primeras pruebas (capítulo 21).')
    P('Limitación declarada: el APK se verificó inspeccionando el paquete generado y probando contra la API desplegada, pero no se ejecutó en un teléfono durante la redacción de este documento. Si se dispone de capturas del teléfono, conviene agregarlas a este capítulo.')

    # ---------------------------------------------------------------
    H('16. Evidencia de la ejecución')
    P('Las capturas siguientes se tomaron sobre el sistema desplegado en Azure (http://4.206.201.129) con un navegador automatizado, usando cuentas de demostración creadas para ese fin. Cada una muestra datos que vienen de la base de datos en la nube, no de maquetas.')
    fotos = [
        ('docs/capturas/01_inicio.png', 'Página de inicio de la web.', 'Es la puerta de entrada: presenta la plataforma y enlaza con tutores, materias y chatbot. Se muestra sin sesión iniciada.'),
        ('docs/capturas/02_tutores.png', 'Listado de tutores.', 'La lista viene de /api/tutores/ y está paginada. Cada tarjeta muestra nombre, especialidad, calificación, tarifa por hora y si el tutor está disponible.'),
        ('docs/capturas/03_materias.png', 'Catálogo de materias.', 'Cada materia muestra su descripción y el número de tutorías registradas. La primera tarjeta ya refleja la tutoría que se creó durante las pruebas.'),
        ('docs/capturas/04_registro.png', 'Formulario de registro.', 'Pide los datos básicos del usuario. Los errores de validación llegan del backend en español.'),
        ('docs/capturas/05_login.png', 'Inicio de sesión.', 'Formulario de acceso con usuario y contraseña. Al validar, la web guarda el token y redirige.'),
        ('docs/capturas/07_mis_tutorias.png', 'Mis tutorías.', 'Vista de un estudiante de prueba (Laura Gómez) con una tutoría pendiente de Arquitectura de Computadores con la tutora Ana García. Esa fila existe en la tabla api_tutoria.'),
        ('docs/capturas/08_dashboard.png', 'Dashboard de administración.', 'Resume 28 usuarios, 22 tutores, 25 materias y 1 tutoría, además de las gráficas. Solo lo ve un administrador.'),
        ('docs/capturas/12_responsive.png', 'Web en ancho de teléfono.', 'La misma interfaz en una ventana de 390 por 844 píxeles. Demuestra que el diseño se adapta a pantallas pequeñas.'),
        ('docs/capturas/10_admin_django.png', 'Panel de administración de Django.', 'Permite gestionar todas las tablas del sistema. Los nombres de modelos están en español.'),
        ('docs/capturas/11_admin_tutorias.png', 'Tutorías en el panel de administración.', 'La misma tutoría de la captura de «Mis tutorías» vista desde el administrador, con sus filtros por estado, fecha y materia. Es la prueba de que lo que se agenda en la interfaz queda guardado en la base de datos.')]
    for i, (ruta, pie, txt) in enumerate(fotos, 1):
        H(f'16.{i} {pie.rstrip(".")}', 2, False)
        P(txt)
        FIG(ruta, pie, 15 if 'responsive' not in ruta else 6)

    # ---------------------------------------------------------------
    H('17. Análisis exploratorio de datos')
    P('El directorio analytics contiene un script que descarga los datos de la API desplegada, los organiza con pandas y produce seis gráficas y un informe en Markdown. El objetivo era dar una primera lectura del sistema y mostrar cómo se podrían explotar los datos cuando haya más uso.')
    H('17.1 Hallazgos', 2, False)
    T(['Indicador', 'Resultado'],
      [['Tutores analizados', '20'],
       ['Materias en el catálogo', '25'],
       ['Franjas de disponibilidad', '84'],
       ['Tarifa promedio por hora', '$34.450 (mínimo $25.000, máximo $50.000)'],
       ['Calificación promedio', '5,0 (todos los tutores comparten el valor inicial)'],
       ['Especialidad con más tutores', 'Matemáticas'],
       ['Día con más disponibilidad', 'Jueves (el de menos es el lunes)'],
       ['Materias sin tutorías registradas', '20 de 25']],
      [6, 9.8], 'Resumen del análisis exploratorio')
    P('Hay que leer estos números con cuidado: provienen de datos de demostración. La correlación entre tarifa y calificación no se puede calcular porque todas las calificaciones valen lo mismo, y el hecho de que 20 de 25 materias no tengan tutorías refleja que apenas empezó el uso, no un problema del catálogo.')
    graf = [('analytics/output/01_tarifas.png', 'Distribución de tarifas por hora.', 'La mayoría de los tutores cobra entre 25.000 y 40.000 pesos la hora; unos pocos expertos llegan a 50.000.'),
            ('analytics/output/02_tarifa_nivel.png', 'Tarifa promedio por nivel de experiencia.', 'La tarifa crece con el nivel: alrededor de 27.700 para intermedios, 34.300 para avanzados y 40.400 para expertos.'),
            ('analytics/output/03_especialidades.png', 'Tutores por especialidad.', 'Muestra la oferta por área. Con 20 tutores y 25 materias, la oferta está repartida.'),
            ('analytics/output/04_disponibilidad_dia.png', 'Franjas de disponibilidad por día de la semana.', 'El jueves concentra más franjas y el lunes menos; información útil para animar a los tutores a abrir más horarios entre semana.'),
            ('analytics/output/05_tarifa_vs_calificacion.png', 'Tarifa frente a calificación.', 'Sin variación en la calificación no se ve relación; se volverá útil cuando haya reseñas reales.'),
            ('analytics/output/06_materias_top.png', 'Materias con más tutorías.', 'Sirve para detectar qué materias se piden más y dónde falta oferta.')]
    for i, (r, pie, txt) in enumerate(graf, 2):
        H(f'17.{i} {pie.rstrip(".")}', 2, False)
        P(txt)
        FIG(r, pie, 13.5)

    # ---------------------------------------------------------------
    H('18. Pruebas')
    H('18.1 Estrategia', 2, False)
    P('Se combinaron tres niveles de prueba. Las pruebas automatizadas del backend verifican las reglas de negocio de forma repetible. Las pruebas de extremo a extremo se hicieron contra el sistema desplegado en Azure creando usuarios, agendando tutorías y comprobando el resultado en la base de datos. Las pruebas manuales exploraron la web y revisaron el contenido del APK.')
    H('18.2 Pruebas automatizadas', 2, False)
    P('Se ejecutan con python manage.py test desde la carpeta backend. Las 18 pruebas pasan.')
    T(['Clase', 'Prueba', 'Qué verifica'],
      [['MateriaAPITestCase', 'test_create_materia', 'Un administrador puede crear una materia'],
       ['MateriaAPITestCase', 'test_anonymous_cannot_create_materia', 'Un anónimo no puede crearla'],
       ['MateriaAPITestCase', 'test_get_materias', 'El catálogo se puede consultar'],
       ['TutorAPITestCase', 'test_create_tutor', 'Alta de un tutor'],
       ['TutorAPITestCase', 'test_get_tutores', 'Lista de tutores'],
       ['DashboardAPITestCase', 'test_summary_returns_aggregates_only_to_admin', 'El administrador ve los agregados'],
       ['DashboardAPITestCase', 'test_summary_is_forbidden_for_regular_users', 'Un usuario común recibe 403'],
       ['ChatbotAPITestCase', 'test_rejects_empty_message', 'Un mensaje vacío se rechaza'],
       ['ChatbotAPITestCase', 'test_university_questions', 'Preguntas sobre la UdeC se responden'],
       ['ChatbotAPITestCase', 'test_unknown_question_admits_ignorance', 'Una pregunta fuera de alcance marca unknown'],
       ['ChatbotAPITestCase', 'test_returns_enterprise_5_json_payload', 'La respuesta incluye el JSON 5.0'],
       ['AuthFlowAPITestCase', 'test_register_tutor_and_student', 'Registro de estudiante y de tutor'],
       ['AuthFlowAPITestCase', 'test_password_reset_flow', 'Flujo completo de recuperación'],
       ['AuthFlowAPITestCase', 'test_reset_token_hidden_by_default', 'El token no se expone si la bandera está apagada'],
       ['AgendaMensualTestCase', 'test_disponibilidad_mensual', 'La agenda del mes devuelve días y horarios'],
       ['AgendaMensualTestCase', 'test_reserva_y_conflicto', 'Una segunda reserva en el mismo horario se rechaza'],
       ['AgendaMensualTestCase', 'test_rechaza_pasado', 'Una fecha pasada se rechaza'],
       ['AgendaMensualTestCase', 'test_materia_con_valoracion', 'La materia expone valoración y total de tutores']],
      [4.2, 5.6, 6], 'Pruebas automatizadas del backend', 8.5)
    H('18.3 Pruebas de extremo a extremo en Azure', 2, False)
    T(['Prueba', 'Resultado'],
      [['Registro de estudiante y de tutor contra la API desplegada', 'Correcto'],
       ['Inicio de sesión y renovación del token', 'Correcto'],
       ['Recuperación de contraseña de punta a punta', 'Correcto'],
       ['Consulta de la agenda mensual de un tutor', 'Correcto'],
       ['Reserva de una tutoría en un horario libre', 'Correcto, queda pendiente'],
       ['Segunda reserva en el mismo horario', 'Rechazada con mensaje en español'],
       ['Reserva en una fecha pasada', 'Rechazada'],
       ['Pregunta fuera de alcance al chatbot', 'Responde que no sabe'],
       ['Dashboard con un usuario administrador', 'Muestra datos reales'],
       ['Panel de administración de Django', 'Funciona y se ve con estilos (ver 21.6)']],
      [10, 5.8], 'Pruebas contra el entorno desplegado')
    H('18.4 Casos de prueba de aceptación', 2, False)
    T(['ID', 'Caso', 'Pasos', 'Esperado', 'Resultado'],
      [['CP-01', 'Registro válido', 'Completar el formulario con datos correctos', 'Cuenta creada, sesión iniciada', 'Aprobado'],
       ['CP-02', 'Registro con correo repetido', 'Registrar dos veces el mismo correo', 'Mensaje de error en español', 'Aprobado'],
       ['CP-03', 'Contraseña débil', 'Usar «12345678»', 'Rechazo por validadores', 'Aprobado'],
       ['CP-04', 'Recuperar contraseña', 'Solicitar, usar el token, iniciar sesión con la nueva', 'Acceso con la nueva', 'Aprobado'],
       ['CP-05', 'Token reutilizado', 'Usar dos veces el mismo token', 'Segunda vez rechazada', 'Aprobado'],
       ['CP-06', 'Agenda mensual', 'Abrir un tutor y cambiar de mes', 'Días con cupo marcados', 'Aprobado'],
       ['CP-07', 'Reserva válida', 'Elegir horario libre y confirmar', 'Tutoría pendiente en «Mis tutorías»', 'Aprobado'],
       ['CP-08', 'Choque de horario', 'Reservar el mismo horario', 'Error 400 en español', 'Aprobado'],
       ['CP-09', 'Chatbot sobre la UdeC', 'Preguntar por las sedes', 'Lista de sedes con aviso de verificación', 'Aprobado'],
       ['CP-10', 'Chatbot fuera de alcance', 'Preguntar la capital de Japón', 'Reconoce que no sabe', 'Aprobado'],
       ['CP-11', 'Acceso a dashboard', 'Entrar como estudiante', 'Sin acceso', 'Aprobado'],
       ['CP-12', 'APK en teléfono físico', 'Instalar y usar', 'Pendiente de ejecutar', 'No realizado']],
      [1.4, 3, 5, 4, 2.4], 'Casos de aceptación', 8.5)

    # ---------------------------------------------------------------
    H('19. Manual de instalación y operación')
    H('19.1 Requisitos previos', 2, False)
    B(['Python 3.12 o superior (requerido por Django 6)', 'Node.js 20 o superior y npm', 'PostgreSQL (local o en la nube)', 'Git', 'Para el APK: cuenta de Expo y EAS CLI'])
    H('19.2 Base de datos y backend', 2, False)
    CODE('git clone https://github.com/Parraxzy26/TutoUdecProyect.git\ncd TutoUdecProyect\npython -m venv .venv\n.venv\\Scripts\\activate\npip install -r backend/requirements.txt\n\n# Variables de entorno en backend/.env (ejemplo, sin valores reales)\nDEBUG=True\nSECRET_KEY=...\nDATABASE_URL=postgresql://usuario:clave@host:5432/basedatos\nALLOWED_HOSTS=localhost,127.0.0.1\n\ncd backend\npython manage.py migrate\npython manage.py createsuperuser\npython manage.py runserver 0.0.0.0:8000')
    P('Con el servidor levantado, la API responde en http://localhost:8000/api/ y la documentación en http://localhost:8000/docs/.')
    H('19.3 Aplicación web', 2, False)
    CODE('cd web\nnpm install\nnpm run dev        # desarrollo, normalmente en http://localhost:5173\nnpm run build      # genera la carpeta dist para producción')
    H('19.4 Aplicación móvil', 2, False)
    CODE('cd mobile\nnpm install\nnpx expo start          # desarrollo con Expo Go\nnpx eas-cli build --platform android --profile preview   # genera el APK')
    P('La dirección de la API que usa la aplicación se define en mobile/src/config.js. En desarrollo apunta al equipo local; en producción, al servidor de Azure.')
    H('19.5 Despliegue en Azure', 2, False)
    N(['Subir los cambios a la rama main de GitHub.',
       'Conectarse a la máquina virtual (o usar az vm run-command) y, como usuario del servicio, ejecutar git fetch y git reset --hard origin/main.',
       'Instalar dependencias en el entorno virtual si cambió requirements.txt.',
       'Ejecutar migraciones y, si hubo cambios en estáticos, python manage.py collectstatic.',
       'Reiniciar el servicio: sudo systemctl restart gunicorn.',
       'Para la web: compilar con npm run build y copiar dist a /var/www/tutoudec.',
       'Si cambió la configuración de nginx: nginx -t y systemctl reload nginx.'])
    P('Un detalle que costó tiempo descubrir: los comandos de Django deben ejecutarse con el mismo usuario y el mismo HOME que usa el servicio (en este caso /home/cristian). Si se ejecutan como root, PostgreSQL intenta leer certificados de /root/.postgresql y la conexión falla.')
    H('19.6 Revisar la base de datos en vivo', 2, False)
    CODE('cd backend\npython db_live.py')
    H('19.7 Orden de arranque completo', 2, False)
    T(['Orden', 'Componente', 'Comprobación'],
      [['1', 'Base de datos PostgreSQL', 'Acepta conexiones'],
       ['2', 'Backend (gunicorn o runserver)', 'GET /api/materias/ responde 200'],
       ['3', 'nginx (solo en servidor)', 'GET / entrega la web'],
       ['4', 'Aplicación web', 'Se abre en el navegador y lista tutores'],
       ['5', 'Aplicación móvil', 'Inicia sesión y muestra tutores']],
      [2, 6, 7.8], 'Orden de arranque')
    H('19.8 Variables de entorno', 2, False)
    T(['Variable', 'Uso'],
      [['DEBUG', 'Modo desarrollo; en producción debe ser False'],
       ['SECRET_KEY', 'Clave de firma de Django; obligatoria con DEBUG=False'],
       ['ALLOWED_HOSTS', 'Dominios o IP que la API acepta'],
       ['DATABASE_URL o DATABASE_*', 'Conexión a PostgreSQL'],
       ['CORS_ALLOWED_ORIGINS', 'Orígenes autorizados para la web'],
       ['EMAIL_HOST_USER / EMAIL_HOST_PASSWORD', 'Credenciales SMTP para los correos de recuperación'],
       ['PASSWORD_RESET_SHOW_TOKEN', 'Si es verdadero, la API devuelve el token (solo demostraciones)']],
      [6, 9.8], 'Variables de entorno principales')

    # ---------------------------------------------------------------
    H('20. Manual de usuario')
    H('20.1 Estudiante', 2, False)
    N(['Abra la aplicación y toque «Registrarse». Complete nombre, usuario, correo y contraseña, y elija el rol de estudiante.',
       'Entre en «Tutores» o en «Materias» y busque la asignatura que necesita.',
       'Abra el perfil de un tutor. Verá su calificación, sus materias y las reseñas.',
       'En el calendario, elija la duración y el día. Los días marcados tienen horarios libres.',
       'Toque la hora que le sirva, indique el lugar y confirme.',
       'En «Mis tutorías» podrá ver el estado de la tutoría y cancelarla si cambia de plan.',
       'Al terminar la tutoría, puede dejar una reseña.'])
    H('20.2 Tutor', 2, False)
    N(['Regístrese con el rol de tutor e indique especialidad, nivel y tarifa.',
       'En su panel verá las tutorías que le reservan, agrupadas por estado.',
       'Confirme las pendientes. Cuando llegue la hora, pulse «Iniciar»; al terminar, «Completar».',
       'Si necesita pausar las reservas, márquese como no disponible.'])
    H('20.3 Administrador', 2, False)
    N(['Inicie sesión con una cuenta de administrador.',
       'En la web, /dashboard muestra las métricas. En /admin/ puede crear, editar o eliminar usuarios, materias, tutores y tutorías.',
       'Para dar permisos a otro usuario puede usar el panel o el endpoint de make_admin.'])
    H('20.4 Recuperar la contraseña', 2, False)
    N(['En la pantalla de inicio de sesión toque «¿Olvidaste tu contraseña?».',
       'Escriba el correo con el que se registró.',
       'Ingrese el token recibido y la nueva contraseña.',
       'Inicie sesión con la contraseña nueva.'])
    H('20.5 Usar el chatbot', 2, False)
    P('Escriba su pregunta con naturalidad, por ejemplo «¿qué carreras hay en Girardot?» o «¿cómo agendo una tutoría?». Si no tiene la información, el asistente se lo dirá y le sugerirá otras preguntas. Para datos oficiales y actualizados, como fechas de matrícula, consulte siempre www.ucundinamarca.edu.co.')

    # ---------------------------------------------------------------
    H('21. Bitácora de problemas y soluciones')
    P('Esta sección reúne los problemas reales que aparecieron y cómo se resolvieron. Se incluye porque es lo más útil para quien herede el proyecto: son los mismos tropiezos que volverán a ocurrir si se cambia de servidor.')
    probs = [
        ('21.1 Error 500 en Azure al conectar con la base de datos', 'La API respondía 500 en todas las rutas que tocaban la base. La causa era el usuario con el que se ejecutaba Django: como root, PostgreSQL buscaba certificados en /root/.postgresql y fallaba. Solución: ejecutar siempre con el usuario del servicio y HOME=/home/cristian, y cargar las variables de backend/.env.'),
        ('21.2 «Error de registro» en el APK', 'Al crear un usuario o tutor desde el APK con todos los campos correctos aparecía un error genérico. Android 9 en adelante bloquea el tráfico HTTP sin cifrar por defecto, y el servidor de demostración atiende por HTTP. Solución: habilitar el tráfico en texto claro en la configuración de compilación y mostrar el mensaje real que devuelve el servidor cuando falla algo.'),
        ('21.3 Recuperación de contraseña que no hacía nada', 'La pantalla existía, pero no llamaba a la API. Solución: crear los endpoints request_password_reset y confirm_password_reset, el modelo PasswordResetToken y reescribir la pantalla para completar el flujo de verdad.'),
        ('21.4 Textos en inglés', 'Parte de la interfaz móvil y algunos mensajes estaban en inglés. Solución: traducir todas las pantallas, los mensajes de validación y los nombres del panel de administración, y fijar el idioma de Django en es-co.'),
        ('21.5 Disponibilidad semanal poco práctica', 'La disponibilidad se mostraba por día de la semana, sin fechas. Se reemplazó por la agenda mensual de la sección 13 y se agregó la validación de reservas en el servidor.'),
        ('21.6 Panel de administración sin estilos', 'Al tomar las capturas de la ejecución se notó que /admin/ se veía sin hojas de estilo. nginx reenviaba /static/ a gunicorn, que no sirve estáticos con DEBUG apagado. Solución: ejecutar collectstatic y hacer que nginx sirva directamente la carpeta staticfiles con un alias; además, dar permiso de lectura a esa carpeta al usuario de nginx. La configuración quedó en deploy/nginx-tutoudec.conf.'),
        ('21.7 Credenciales expuestas en una conversación', 'Durante el trabajo se compartieron un token de Expo y una contraseña de aplicación de Gmail. Se usaron solo en los comandos y no se guardaron en el repositorio, pero al haber circulado deben considerarse comprometidos: hay que revocarlos y generar otros nuevos.')]
    for t, x in probs:
        H(t, 2, False)
        P(x)

    # ---------------------------------------------------------------
    H('22. Verificación de requisitos del proyecto')
    T(['Requisito del cliente', 'Dónde se cumple', 'Evidencia'],
      [['Al menos ocho funcionalidades', 'Autenticación, recuperación, tutores, materias, tutorías con agenda, reseñas, grupos, chatbot y dashboard', 'Capítulos 3 y 10'],
       ['Base de datos en la nube', 'PostgreSQL en Azure', 'Capítulos 4 y 9; captura del admin con registros reales'],
       ['Aplicación móvil que consuma la API', 'Expo / React Native; APK generado', 'Capítulo 15'],
       ['Análisis exploratorio con dashboard', 'Carpeta analytics y /dashboard', 'Capítulo 17 y figura del dashboard'],
       ['Despliegue en la nube funcionando', 'Máquina virtual de Azure con nginx y gunicorn', 'Capítulos 4.4 y 19'],
       ['Chatbot extenso sobre la UdeC que admita no saber', 'Motor de conocimiento y respuesta JSON 5.0', 'Capítulo 12 y pruebas'],
       ['Todo en español', 'Interfaz, mensajes y panel de administración', 'RNF-01 y capítulo 21'],
       ['Disponibilidad mensual y reserva desde el perfil del tutor', 'Agenda mensual', 'Capítulo 13'],
       ['Materias con la presentación de los tutores', 'Pantallas de materias', 'Sección 15.4'],
       ['Diagramas de flujo, clases, E-R y casos de uso', 'Capítulos 5 a 8', 'Figuras de esos capítulos'],
       ['Fotos de la ejecución', 'Capítulo 16', 'Capturas del sistema desplegado'],
       ['Documentación de al menos 70 páginas', 'Este documento', 'Conteo de páginas en Word']],
      [5.4, 5.6, 4.8], 'Requisitos y evidencias')

    # ---------------------------------------------------------------
    H('23. Conclusiones')
    B(['La plataforma cumple el objetivo: un estudiante puede registrarse, ver la agenda mensual de un tutor, reservar sin choques y consultar al asistente, y todo queda guardado en una base de datos en la nube.',
       'Concentrar las reglas de negocio en la API fue la mejor decisión de diseño. Los errores de reserva, por ejemplo, se arreglaron una sola vez y beneficiaron a la web y al móvil.',
       'Un asistente basado en reglas y conocimiento propio es suficiente para un dominio acotado, y tiene una ventaja que los modelos generativos no garantizan: puede decir que no sabe.',
       'Muchos de los problemas más costosos fueron de infraestructura y no de código: el usuario con el que corre Django, el tráfico HTTP bloqueado por Android o los archivos estáticos. Documentarlos ahorra tiempo.',
       'Probar contra el entorno desplegado, y no solo en local, encontró errores que las pruebas automatizadas no podían ver, como el panel de administración sin estilos.'])
    H('23.1 Trabajo futuro', 2, False)
    B(['Servir todo por HTTPS con un dominio propio y quitar el tráfico en texto claro del APK.',
       'Notificaciones push y por correo cuando cambie el estado de una tutoría.',
       'Videollamada integrada para las tutorías virtuales.',
       'Límite de intentos en el inicio de sesión y en la recuperación de contraseña.',
       'Reseñas solo para tutorías completadas, y recálculo automático de la calificación del tutor.',
       'Ejecutar y documentar pruebas del APK en varios teléfonos.',
       'Ampliar la base de conocimiento del asistente con información oficial verificada por la universidad.'])

    H('24. Glosario')
    T(['Término', 'Significado'],
      [['API REST', 'Interfaz que expone recursos mediante URL y verbos HTTP'],
       ['APK', 'Paquete de instalación de una aplicación Android'],
       ['CORS', 'Mecanismo del navegador que controla qué orígenes pueden llamar a una API'],
       ['Dashboard', 'Tablero con indicadores'],
       ['EAS Build', 'Servicio de Expo para compilar aplicaciones móviles'],
       ['EDA', 'Análisis exploratorio de datos'],
       ['gunicorn', 'Servidor de aplicaciones WSGI para Python'],
       ['JWT', 'Token firmado que identifica a un usuario sin guardar sesión en el servidor'],
       ['Migración', 'Archivo que describe un cambio en el esquema de la base de datos'],
       ['nginx', 'Servidor web y proxy inverso'],
       ['ORM', 'Capa que traduce objetos de Python a consultas SQL'],
       ['Serializador', 'Componente que convierte modelos en JSON y valida la entrada'],
       ['Tutoría', 'Sesión de apoyo académico entre un tutor y un estudiante'],
       ['UdeC', 'Universidad de Cundinamarca']],
      [4, 11.8], 'Glosario')

    H('25. Bibliografía y fuentes')
    B(['Django Software Foundation. Documentación de Django. https://docs.djangoproject.com',
       'Encode. Django REST Framework. https://www.django-rest-framework.org',
       'Jazzband. djangorestframework-simplejwt. https://django-rest-framework-simplejwt.readthedocs.io',
       'Vue.js. Guía oficial de Vue 3. https://vuejs.org',
       'Expo. Documentación de Expo y EAS Build. https://docs.expo.dev',
       'React Native. Documentación. https://reactnative.dev',
       'PostgreSQL Global Development Group. Documentación de PostgreSQL. https://www.postgresql.org/docs',
       'Microsoft. Documentación de Azure Virtual Machines. https://learn.microsoft.com/azure',
       'Comisión Europea. Industry 5.0: Towards a sustainable, human-centric and resilient European industry (2021).',
       'Universidad de Cundinamarca. Sitio oficial. https://www.ucundinamarca.edu.co (información general citada por el asistente).'])
