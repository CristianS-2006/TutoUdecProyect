"""Motor conversacional de TutoUdec: puntuación por coincidencias, contexto y fallback honesto."""
import difflib
import random
import re
import unicodedata


def normalize(text):
    text = unicodedata.normalize('NFD', text.lower())
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z0-9ñ\s@.]', ' ', text)


def _tokens(text):
    return set(normalize(text).split())


# Cada tema: palabras/frases clave (sin tildes), respuesta completa y sugerencias de seguimiento.
TOPICS = {
    'bienvenida': {
        'keywords': ['hola', 'buenos dias', 'buenas tardes', 'buenas noches', 'buenas', 'hey', 'hello',
                     'que tal', 'como estas', 'saludos'],
        'answer': '¡Hola! 👋 Soy el asistente virtual de TutoUdec. Puedo contarte sobre la Universidad de '
                  'Cundinamarca (UdeC), cómo funcionan las tutorías, materias, horarios, pagos, tu cuenta y '
                  'más. Puedes escribirme con tus propias palabras. ¿Qué quieres saber?',
        'follow': ['¿Qué es TutoUdec?', '¿Cómo agendo una tutoría?', '¿Qué es la UdeC?'],
    },
    'identidad': {
        'keywords': ['quien eres', 'que eres', 'como te llamas', 'eres un bot', 'eres humano', 'eres una ia',
                     'inteligencia artificial', 'que puedes hacer', 'para que sirves', 'que sabes'],
        'answer': 'Soy el asistente virtual de TutoUdec. Respondo con información de la plataforma y de la '
                  'Universidad de Cundinamarca. Puedo ayudarte con: tutorías, materias, horarios, costos, '
                  'pagos, registro, inicio de sesión, perfil, calificaciones, cómo ser tutor y seguridad. '
                  'No soy una persona ni tengo acceso a tus datos privados; si algo requiere revisión humana, '
                  'te indicaré cómo contactar a soporte.',
        'follow': ['¿Qué es TutoUdec?', '¿Cómo contacto a soporte?'],
    },
    'tutoudec': {
        'keywords': ['tutoudec', 'que es tutoudec', 'de que trata', 'proyecto', 'plataforma', 'aplicacion',
                     'app', 'para que sirve la app', 'objetivo', 'como funciona'],
        'answer': 'TutoUdec es una plataforma (app móvil y web) de tutorías académicas para estudiantes de la '
                  'Universidad de Cundinamarca. Conecta a estudiantes que necesitan apoyo en una materia con '
                  'tutores que la dominan.\n\nCon ella puedes:\n• Buscar tutores y materias.\n• Agendar tutorías '
                  'individuales o unirte a grupos de tutoría con cupos.\n• Ver tu historial, calificar a tus '
                  'tutores y gestionar tu perfil.\n• Registrarte como tutor y ofrecer tus conocimientos.',
        'follow': ['¿Cómo agendo una tutoría?', '¿Cómo ser tutor?', '¿Qué materias hay?'],
    },
    'registro': {
        'keywords': ['registrarme', 'registro', 'crear cuenta', 'nueva cuenta', 'inscribirme', 'inscripcion',
                     'sign up', 'darme de alta', 'abrir cuenta', 'como me registro', 'me inscribo', 'como me inscribo',
                     'inscribir', 'registro de cuenta'],
        'answer': 'Para crear tu cuenta en TutoUdec:\n1. Abre la app y toca "Registrarse".\n2. Completa tus datos '
                  '(nombre, usuario, correo y contraseña).\n3. Elige si eres estudiante o tutor.\n4. Confirma y '
                  'ya puedes iniciar sesión.\n\nSi te marca error, revisa que todos los campos estén completos, '
                  'que el correo no esté ya registrado y que tu contraseña cumpla los requisitos.',
        'follow': ['No puedo iniciar sesión', '¿Cómo ser tutor?'],
    },
    'login': {
        'keywords': ['login', 'iniciar sesion', 'entrar', 'acceder', 'no puedo entrar', 'contrasena',
                     'olvide', 'recuperar', 'clave', 'password', 'cerrar sesion', 'cambiar contrasena'],
        'answer': 'Si tienes problemas con tu acceso:\n• Verifica usuario y contraseña (mayúsculas y espacios '
                  'extra).\n• Comprueba tu conexión a internet.\n• Si olvidaste la contraseña, usa la opción de '
                  'recuperación en la pantalla de inicio de sesión.\n• Para cambiarla estando dentro, ve a '
                  'Perfil → Seguridad.\n\nSi nada funciona, escribe a tutoudec.soporte@gmail.com indicando tu '
                  'usuario (nunca envíes tu contraseña).',
        'follow': ['¿Cómo contacto a soporte?', '¿Cómo edito mi perfil?'],
    },
    'tutorias': {
        'keywords': ['tutoria', 'tutorias', 'tutor', 'tutores', 'clase', 'clases', 'agendar', 'reservar',
                     'pedir tutoria', 'buscar tutor', 'sesion', 'cancelar', 'cancelar tutoria', 'reprogramar',
                     'cambiar horario', 'ayuda academica', 'refuerzo', 'asesoria'],
        'answer': 'Así funcionan las tutorías en TutoUdec:\n1. Busca un tutor por materia o nombre.\n2. Revisa su '
                  'perfil, calificaciones y disponibilidad.\n3. Elige un horario y confirma la reserva (también '
                  'puedes unirte a grupos de tutoría con cupos).\n4. Asiste en la modalidad acordada, presencial '
                  'o virtual.\n5. Al terminar, califica la sesión.\n\nPara cancelar o cambiar una tutoría entra a '
                  'tu lista de tutorías, selecciónala y usa la opción de cancelar. Hazlo con anticipación para no '
                  'afectar al tutor.',
        'follow': ['¿Qué materias hay?', '¿Cuánto cuestan?', '¿Cómo califico a un tutor?'],
    },
    'grupos': {
        'keywords': ['grupo', 'grupos', 'cupos', 'cupo', 'grupal', 'unirme a un grupo', 'grupo de tutoria'],
        'answer': 'Los grupos de tutoría son sesiones con un tutor y varios estudiantes, con un número limitado '
                  'de cupos. Puedes ver el nombre, materia, modalidad, fecha de inicio y cupos disponibles, y '
                  'unirte mientras haya espacio. Son una buena opción para temas que varios compañeros necesitan '
                  'repasar y suelen salir más económicos que una sesión individual.',
        'follow': ['¿Cómo agendo una tutoría?', '¿Cuánto cuestan?'],
    },
    'materias': {
        'keywords': ['materia', 'materias', 'asignatura', 'asignaturas', 'curso', 'cursos', 'calculo', 'algebra',
                     'fisica', 'quimica', 'programacion', 'estadistica', 'economia', 'ingles', 'matematicas',
                     'biologia', 'filosofia', 'que materias'],
        'answer': 'Las materias dependen de los tutores registrados. Normalmente hay apoyo en áreas como '
                  'cálculo, álgebra, física, química, programación, estadística, economía, inglés y biología. '
                  'Puedes ver el listado actualizado en la sección de Materias de la app y filtrar tutores por '
                  'cada una. Si no aparece la que necesitas, cuéntanos por soporte o anímate a ser tutor de ella.',
        'follow': ['¿Cómo busco un tutor?', '¿Cómo ser tutor?'],
    },
    'horarios': {
        'keywords': ['horario', 'horarios', 'disponibilidad', 'cuando', 'que dias', 'hora', 'fechas',
                     'disponible', 'presencial', 'virtual', 'modalidad', 'online'],
        'answer': 'Cada tutor define su propia disponibilidad, que verás en su perfil o en el detalle del grupo. '
                  'Las tutorías pueden ser presenciales (en el campus) o virtuales, según lo que ofrezca el '
                  'tutor. Elige el horario que te acomode, confirma tu reserva y, si no puedes asistir, '
                  'cancélala con antelación.',
        'follow': ['¿Cómo cancelo una tutoría?', '¿Cómo agendo una tutoría?'],
    },
    'costos': {
        'keywords': ['precio', 'precios', 'costo', 'costos', 'tarifa', 'cuanto cuesta', 'cuesta', 'valor',
                     'gratis', 'gratuito', 'subsidio', 'descuento', 'cobran'],
        'answer': 'Registrarse en TutoUdec no tiene costo. El valor de cada tutoría lo define el tutor y se ve '
                  'en su perfil o en el detalle del grupo; algunas pueden ser gratuitas o con condiciones '
                  'especiales. Los grupos suelen salir más económicos por persona. Revisa siempre el valor antes '
                  'de confirmar. No tengo un precio fijo porque varía por tutor y materia.',
        'follow': ['¿Cómo pago?', '¿Cómo agendo una tutoría?'],
    },
    'pago': {
        'keywords': ['pagar', 'pago', 'pagos', 'metodo de pago', 'efectivo', 'transferencia', 'nequi',
                     'daviplata', 'como pagar', 'factura', 'comprobante', 'reembolso'],
        'answer': 'Los medios de pago los acuerdas con el tutor (por ejemplo efectivo o transferencia, según lo '
                  'que él acepte). Recomendaciones:\n• Confirma el valor y el método antes de la sesión.\n• '
                  'Guarda el comprobante de cualquier transferencia.\n• Nunca compartas claves ni datos '
                  'completos de tu tarjeta por el chat.\n\nPara disputas o problemas con un pago escribe a '
                  'tutoudec.soporte@gmail.com.',
        'follow': ['¿Cuánto cuestan?', '¿Cómo contacto a soporte?'],
    },
    'ser_tutor': {
        'keywords': ['ser tutor', 'quiero ser tutor', 'requisitos tutor', 'registrarme como tutor',
                     'convertirme en tutor', 'dar tutorias', 'ofrecer tutorias', 'soy tutor', 'ensenar'],
        'answer': 'Para ser tutor en TutoUdec:\n1. Regístrate eligiendo el rol de tutor (o actualiza tu perfil).\n'
                  '2. Indica las materias que dominas y tu experiencia.\n3. Define tu disponibilidad y tu tarifa.\n'
                  '4. Crea tutorías o grupos para que los estudiantes te encuentren.\n\nLos requisitos '
                  'específicos (por ejemplo promedio o semestre mínimo) los define el equipo de la plataforma; '
                  'si quieres confirmarlos, escribe a tutoudec.soporte@gmail.com.',
        'follow': ['¿Cómo creo un grupo de tutoría?', '¿Cómo me califican?'],
    },
    'perfil': {
        'keywords': ['perfil', 'mi perfil', 'editar perfil', 'actualizar perfil', 'cambiar datos', 'foto',
                     'datos personales', 'mi cuenta'],
        'answer': 'En la pestaña Perfil puedes ver y editar tus datos, cambiar tu foto, revisar tu historial de '
                  'tutorías y cerrar sesión. Si eres tutor, también gestionas tus materias y disponibilidad. '
                  'Mantén tu información actualizada para que otros usuarios te conozcan mejor.',
        'follow': ['¿Cómo cambio mi contraseña?', '¿Cómo ser tutor?'],
    },
    'calificacion': {
        'keywords': ['calificar', 'calificacion', 'calificaciones', 'resena', 'estrellas', 'puntuacion',
                     'opinion', 'valorar', 'comentario'],
        'answer': 'Al terminar una tutoría puedes calificar a tu tutor con estrellas y dejar un comentario. '
                  'Entra a tus tutorías completadas, selecciona la sesión y elige calificar. Tu opinión ayuda a '
                  'otros estudiantes a elegir bien y a mantener la calidad; sé honesto y respetuoso.',
        'follow': ['¿Cómo agendo una tutoría?'],
    },
    'seguridad': {
        'keywords': ['seguridad', 'privacidad', 'datos', 'proteccion', 'cuenta segura', 'hackeo', 'hackearon',
                     'sospechosa', 'robaron', 'phishing', 'estafa'],
        'answer': 'Cuida tu cuenta así:\n• Usa una contraseña larga con letras, números y símbolos, y no la '
                  'compartas.\n• Cierra sesión en dispositivos compartidos.\n• No envíes datos bancarios por el '
                  'chat.\n• Si ves actividad sospechosa, cambia tu contraseña de inmediato y avisa a '
                  'tutoudec.soporte@gmail.com.',
        'follow': ['¿Cómo cambio mi contraseña?', '¿Cómo contacto a soporte?'],
    },
    'soporte': {
        'keywords': ['soporte', 'problema', 'error', 'no funciona', 'falla', 'bug', 'se cierra', 'se traba',
                     'no carga', 'queja', 'reclamo', 'reportar', 'contacto', 'contactar', 'correo', 'email',
                     'telefono', 'comunicarme', 'humano', 'persona'],
        'answer': 'Si algo no funciona o necesitas atención humana, escribe a tutoudec.soporte@gmail.com. '
                  'Para resolverlo más rápido incluye: qué estabas haciendo, qué mensaje de error apareció, tu '
                  'dispositivo (Android/iOS/web) y capturas si puedes. Mientras tanto, prueba cerrar y abrir la '
                  'app y revisar tu conexión.',
        'follow': ['No puedo iniciar sesión', '¿Qué es TutoUdec?'],
    },
    'estudio': {
        'keywords': ['consejos', 'estudiar', 'tecnicas de estudio', 'como estudiar', 'concentrarme',
                     'organizar', 'parcial', 'examen', 'motivacion', 'procrastinar', 'tiempo'],
        'answer': 'Algunos consejos que funcionan:\n• Planifica por semanas y divide los temas en bloques de '
                  '25–45 min con descansos cortos.\n• Practica con ejercicios en lugar de solo releer.\n• Explica '
                  'el tema en voz alta como si enseñaras a alguien.\n• Repasa un poco cada día en vez de todo '
                  'la víspera.\n• Si algo se te atasca, agenda una tutoría a tiempo: preguntar pronto ahorra '
                  'mucho esfuerzo.',
        'follow': ['¿Cómo busco un tutor?', '¿Qué materias hay?'],
    },
    'despedida': {
        'keywords': ['adios', 'chao', 'chau', 'hasta luego', 'gracias', 'muchas gracias', 'bye', 'listo',
                     'perfecto', 'excelente', 'vale gracias', 'nos vemos'],
        'answer': '¡Con gusto! 😊 Si te surge otra duda sobre TutoUdec o la UdeC, aquí estaré. ¡Mucho éxito en '
                  'tus estudios!',
        'follow': [],
    },
}

try:
    from .udec_knowledge import UDEC_TOPICS
except ImportError:  # ejecución directa fuera del paquete
    from udec_knowledge import UDEC_TOPICS
TOPICS.update(UDEC_TOPICS)

FALLBACK_SUGGESTIONS = ['¿Qué es TutoUdec?', '¿Qué es la UdeC?', '¿Cómo agendo una tutoría?',
                        '¿Cuánto cuestan las tutorías?', '¿Cómo contacto a soporte?']

# Palabras demasiado comunes que no deben puntuar solas.
WEAK = {'hora', 'tiempo', 'datos', 'clase', 'app', 'proyecto', 'listo', 'perfecto', 'excelente', 'entrar',
        'valor', 'persona', 'opinion', 'organizar', 'cuando', 'cancelar'}


def _score(norm_msg, tokens, keywords):
    total = 0.0
    for kw in keywords:
        if ' ' in kw:
            if kw in norm_msg:
                total += 3 * len(kw.split())
        elif kw in tokens:
            total += 1 if kw in WEAK else 3
    return total


GREETING_WORDS = ['hola', 'holi', 'holis', 'holaa', 'ola', 'buenas', 'wenas', 'hey', 'hi', 'hello', 'saludos',
                  'epa', 'quiubo', 'quihubo', 'buenos', 'ey']
GREETING_REPLIES = [
    '¡Holi! 😄 Qué bueno verte por aquí. Soy el asistente de TutoUdec. ¿Cómo vas hoy? Cuéntame en qué te '
    'puedo ayudar: tutorías, materias, tu cuenta o lo que quieras saber de la UdeC.',
    '¡Hola! 👋 Me alegra que me escribas. ¿Cómo te va? Estoy listo para ayudarte con lo que necesites de '
    'TutoUdec o de la Universidad de Cundinamarca.',
    '¡Hey, hola! 😊 Aquí estoy. ¿Qué tienes en mente hoy? Puedo ayudarte a encontrar un tutor, resolver '
    'dudas de la app o simplemente conversar un rato.',
]
HOW_ARE_YOU = [
    '¡Muy bien, gracias por preguntar! 😊 Con ganas de ayudarte. ¿Y tú, cómo estás? Cuéntame qué necesitas.',
    'Todo en orden por acá, ¡gracias! 🙌 ¿Y tú cómo te sientes hoy? Si quieres, te ayudo con tus tutorías.',
]
FEELINGS_NEG = {'triste', 'estresado', 'estresada', 'estres', 'cansado', 'cansada', 'agotado', 'agotada',
                'ansioso', 'ansiosa', 'preocupado', 'preocupada', 'mal', 'desanimado', 'desanimada',
                'frustrado', 'frustrada', 'agobiado', 'agobiada', 'deprimido', 'deprimida', 'nervioso',
                'nerviosa', 'perdido', 'perdida', 'aburrido', 'aburrida'}
FEELINGS_POS = {'feliz', 'contento', 'contenta', 'emocionado', 'emocionada', 'genial', 'bien', 'super',
                'tranquilo', 'tranquila', 'alegre', 'motivado', 'motivada'}
JOKES = [
    '¿Por qué el estudiante llevó una escalera a clase? Porque quería llegar a un nivel más alto. 😄',
    '¿Sabes por qué los programadores confunden Halloween con Navidad? Porque 31 OCT = 25 DEC. 🎃',
    '—Profe, ¿puedo entregar el trabajo mañana? —Claro. —¡Gracias! —De nada... del año pasado. 😅',
]
COMPLIMENTS = {'genial', 'crack', 'buenisimo', 'buenisima', 'inteligente', 'increible', 'chevere', 'util',
               'bacano', 'maquina', 'capo'}
INSULTS = {'tonto', 'inutil', 'estupido', 'torpe', 'malo', 'pesimo', 'bobo', 'idiota'}
CONVERSATIONAL_FALLBACKS = [
    'Mmm, con eso no te sé responder bien todavía 🤔, pero me interesa entenderte. ¿Me lo cuentas con otras '
    'palabras? Mientras tanto, puedo ayudarte con tutorías, materias, horarios, pagos, tu cuenta y la UdeC.',
    'Te leo, aunque de eso no tengo información confiable y prefiero no inventarte nada. 🙏 Si quieres, '
    'cuéntame un poco más de lo que buscas, o elige una de estas opciones y avanzamos.',
    'Ese tema se me escapa un poco 😅. Lo mío es TutoUdec y la Universidad de Cundinamarca, pero puedo '
    'conversar contigo y ayudarte a orientarte. ¿Qué te gustaría resolver?',
]


def _is_greeting_token(tok):
    return tok in GREETING_WORDS or bool(difflib.get_close_matches(tok, GREETING_WORDS, n=1, cutoff=0.78))


def _small_talk(norm_msg, tokens, raw_tokens):
    """Respuestas conversacionales para charla corta. Devuelve (respuesta, intent, sugerencias) o None."""
    follow = ['¿Qué es TutoUdec?', '¿Cómo agendo una tutoría?', '¿Qué materias hay?']
    m = re.search(r'\b(?:me llamo|mi nombre es|soy)\s+([a-zñ]{2,20})\b', norm_msg)
    if m and m.group(1) not in ('tutor', 'estudiante', 'nuevo', 'nueva', 'de', 'un', 'una', 'el', 'la'):
        name = m.group(1).capitalize()
        return (f'¡Mucho gusto, {name}! 😊 Yo soy el asistente de TutoUdec. ¿En qué te puedo ayudar hoy?',
                'bienvenida', follow)
    if re.search(r'\b(como estas|como esta|como vas|como te va|como andas|que tal|que hay|que mas|que haces)\b',
                 norm_msg):
        return random.choice(HOW_ARE_YOU), 'bienvenida', follow
    if 'chiste' in tokens or 'chistoso' in tokens or 'hazme reir' in norm_msg:
        return random.choice(JOKES) + '\n\n¿Quieres otro o prefieres que te ayude con tus tutorías?', 'chiste', follow
    if tokens & INSULTS:
        return ('Lamento no haber sido de ayuda 🙏. Dame otra oportunidad: cuéntame con más detalle qué '
                'necesitas y lo intento de nuevo.', 'bienvenida', follow)
    if tokens & COMPLIMENTS and len(tokens) <= 4 and ('eres' in tokens or 'que' in tokens or len(tokens) == 1):
        return ('¡Gracias, qué amable! 😊 Me motiva ayudarte. ¿Hay algo más en lo que pueda apoyarte?',
                'bienvenida', follow)
    if tokens & FEELINGS_NEG:
        return ('Lamento que te sientas así 💛. A veces la carga académica pesa mucho, pero se puede '
                'organizar paso a paso. Si quieres, te ayudo a encontrar un tutor, te doy consejos de estudio '
                'o simplemente me cuentas qué pasa.',
                'estudio', ['Dame consejos para estudiar', '¿Cómo busco un tutor?'])
    if tokens & FEELINGS_POS and len(tokens) <= 5:
        return ('¡Qué bueno leer eso! 🎉 Aprovechemos esa energía: ¿en qué te ayudo hoy?', 'bienvenida', follow)
    if tokens & {'si', 'sip', 'dale', 'claro', 'ok', 'okay', 'vale'} and len(tokens) <= 2:
        return ('¡Perfecto! 👍 Cuéntame un poco más: ¿buscas un tutor, quieres saber de materias, o tienes '
                'un problema con la app?', 'bienvenida', follow)
    if tokens & {'no', 'nop', 'nada'} and len(tokens) <= 2:
        return ('Está bien 😊. Si más adelante necesitas algo, aquí estaré. ¿Quieres que te cuente algo de '
                'TutoUdec mientras tanto?', 'bienvenida', follow)
    if tokens & {'ayuda', 'ayudame', 'help', 'menu'} and len(tokens) <= 3:
        return ('¡Claro que sí! 🙌 Puedo ayudarte con: buscar y agendar tutorías, materias y horarios, costos y '
                'pagos, tu cuenta y contraseña, cómo ser tutor y datos de la UdeC. ¿Por cuál empezamos?',
                'bienvenida', follow)
    if raw_tokens and all(_is_greeting_token(t) for t in raw_tokens[:2]) and len(raw_tokens) <= 3:
        return random.choice(GREETING_REPLIES), 'bienvenida', follow
    if raw_tokens and _is_greeting_token(raw_tokens[0]) and len(raw_tokens) <= 6 and not (
            tokens & {'inscribo', 'tutor', 'tutoria', 'materia', 'pago'}):
        return random.choice(GREETING_REPLIES), 'bienvenida', follow
    return None


def respond(message, history=None):
    """Devuelve (respuesta, intent, sugerencias)."""
    norm_msg = ' ' + ' '.join(normalize(message).split()) + ' '
    tokens = set(norm_msg.split())
    raw_tokens = norm_msg.split()
    norm_msg = norm_msg.strip()
    feeling_neg = bool(tokens & FEELINGS_NEG)

    scores = {}
    for name, topic in TOPICS.items():
        kws = [normalize(k).strip() for k in topic['keywords']]
        s = _score(norm_msg, tokens, kws)
        if s:
            scores[name] = s

    # Los saludos/despedidas solo valen cuando el mensaje es corto; si no, ceden ante temas reales.
    if len(tokens) > 4:
        for soft in ('bienvenida', 'despedida'):
            if soft in scores and len(scores) > 1:
                scores[soft] = 0

    ranked = sorted(scores.items(), key=lambda x: -x[1])
    ranked = [r for r in ranked if r[1] > 0]

    strong_topic = any(s >= 3 and n not in ('bienvenida', 'despedida') for n, s in ranked)
    if len(raw_tokens) <= 8 and not strong_topic:
        talk = _small_talk(norm_msg, tokens, raw_tokens)
        if talk:
            return talk

    # Preguntas de seguimiento muy cortas ("y eso?", "cuánto?") usan el tema anterior.
    if (not ranked or ranked[0][1] < 3) and history and len(tokens) <= 4:
        last = next((h.get('intent') for h in reversed(history) if h.get('intent') in TOPICS), None)
        if last and last not in ('bienvenida', 'despedida') and tokens & {
                'eso', 'mas', 'como', 'donde', 'cuando', 'cuanto', 'detalle', 'detalles', 'explica', 'explicame',
                'otra', 'y', 'porque', 'si'}:
            topic = TOPICS[last]
            return ('Sobre ese mismo tema: ' + topic['answer'], last, topic['follow'])

    if not ranked or ranked[0][1] < 2:
        return random.choice(CONVERSATIONAL_FALLBACKS), 'default', FALLBACK_SUGGESTIONS

    best = ranked[0][0]
    topic = TOPICS[best]
    answer = topic['answer']
    if feeling_neg:
        answer = 'Te entiendo, y lamento que estés pasando por eso 💛. Vamos paso a paso.\n\n' + answer
    # Si hay un segundo tema relevante, se menciona para respuestas más completas.
    if len(ranked) > 1 and ranked[1][1] >= 3 and ranked[1][1] >= ranked[0][1] * 0.6:
        second = TOPICS[ranked[1][0]]
        if ranked[1][0] not in ('bienvenida', 'despedida'):
            answer += '\n\nTambién te puede interesar: ' + second['answer']
    return answer, best, topic['follow']
