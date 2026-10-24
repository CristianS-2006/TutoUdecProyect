"""Genera los diagramas del documento técnico en docs/diagramas/*.png (matplotlib)."""
import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Ellipse, Rectangle, Polygon, Circle

OUT = os.path.join(os.path.dirname(__file__), 'diagramas')
os.makedirs(OUT, exist_ok=True)
VERDE, VERDE_C, GRIS, AZUL, AMAR = '#2e7d32', '#e8f5e9', '#455a64', '#e3f2fd', '#fff8e1'


def lienzo(w, h):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, w * 10)
    ax.set_ylim(0, h * 10)
    ax.axis('off')
    return fig, ax


def caja(ax, x, y, w, h, texto, fc=VERDE_C, ec=VERDE, fs=9, bold=False, r=1.2):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle=f'round,pad=0.2,rounding_size={r}', fc=fc, ec=ec, lw=1.4))
    ax.text(x + w / 2, y + h / 2, texto, ha='center', va='center', fontsize=fs,
            fontweight='bold' if bold else 'normal', wrap=True)


def flecha(ax, p1, p2, txt='', style='->', color=GRIS, off=(0, 0.8), fs=8):
    ax.annotate('', xy=p2, xytext=p1, arrowprops=dict(arrowstyle=style, color=color, lw=1.3))
    if txt:
        ax.text((p1[0] + p2[0]) / 2 + off[0], (p1[1] + p2[1]) / 2 + off[1], txt, fontsize=fs, ha='center', color=color)


def guardar(fig, nombre):
    fig.savefig(os.path.join(OUT, nombre), dpi=170, bbox_inches='tight', facecolor='white')
    plt.close(fig)


# ---------- 1. Arquitectura ----------
def arquitectura():
    fig, ax = lienzo(11, 7)
    caja(ax, 5, 52, 28, 12, 'App móvil\nReact Native + Expo\n(APK Android)', AZUL, '#1565c0', 10, True)
    caja(ax, 5, 33, 28, 12, 'Aplicación web\nVue 3 + Vite + Pinia', AZUL, '#1565c0', 10, True)
    caja(ax, 5, 14, 28, 12, 'Swagger / ReDoc\nDocumentación OpenAPI', AMAR, '#f9a825', 10, True)
    caja(ax, 45, 33, 24, 14, 'nginx\npuerto 80\n(HTTP)', '#eeeeee', GRIS, 10, True)
    caja(ax, 78, 44, 28, 14, 'gunicorn + Django REST\nJWT · chatbot · agenda', VERDE_C, VERDE, 10, True)
    caja(ax, 78, 22, 28, 12, 'PostgreSQL\nbase tutoudec', '#ede7f6', '#5e35b1', 10, True)
    caja(ax, 78, 4, 28, 11, 'Servicio de IA (opcional)\nOpenAI · modo JSON 5.0', AMAR, '#f9a825', 9, True)
    for y in (58, 39, 20):
        flecha(ax, (34, y), (44, 40), '', '->')
    flecha(ax, (70, 40), (77, 50), '/api  /docs  /admin', '->', off=(2, 2.5))
    flecha(ax, (92, 43), (92, 35), 'SQL', '->', off=(3, 0))
    flecha(ax, (92, 21), (92, 16), 'opcional', '<->', off=(5, 0))
    ax.text(55, 66, 'Máquina virtual Azure (Ubuntu) - IP 4.206.201.129', ha='center', fontsize=10, color=GRIS, style='italic')
    ax.add_patch(Rectangle((42, 2), 68, 62, fill=False, ec=GRIS, ls='--', lw=1))
    guardar(fig, '01_arquitectura.png')


# ---------- 2. Casos de uso ----------
def casos_uso():
    fig, ax = lienzo(12, 9)
    ax.add_patch(Rectangle((26, 3), 66, 84, fill=False, ec=GRIS, lw=1.4))
    ax.text(59, 89, 'Sistema TutoUdec', ha='center', fontsize=12, fontweight='bold')

    def actor(x, y, nombre):
        ax.add_patch(Circle((x, y + 8), 1.6, fc='white', ec='black'))
        ax.plot([x, x], [y + 6.4, y + 2], 'k')
        ax.plot([x - 3, x + 3], [y + 5, y + 5], 'k')
        ax.plot([x, x - 2.5], [y + 2, y - 1.5], 'k')
        ax.plot([x, x + 2.5], [y + 2, y - 1.5], 'k')
        ax.text(x, y - 4, nombre, ha='center', fontsize=10, fontweight='bold')

    def cu(x, y, texto):
        ax.add_patch(Ellipse((x, y), 27, 7, fc=VERDE_C, ec=VERDE, lw=1.2))
        ax.text(x, y, texto, ha='center', va='center', fontsize=8)
        return (x, y)

    estudiante = (12, 52)
    tutor = (106, 60)
    admin = (106, 22)
    actor(*estudiante, 'Estudiante')
    actor(*tutor, 'Tutor')
    actor(*admin, 'Administrador')

    est_cu = [('Registrarse / iniciar sesión', 80), ('Recuperar contraseña', 72), ('Buscar tutores y materias', 64),
              ('Consultar agenda mensual', 56), ('Agendar tutoría', 48), ('Ver mis tutorías', 40),
              ('Cancelar tutoría', 32), ('Conversar con el asistente', 24), ('Calificar tutor', 16)]
    for t, y in est_cu:
        c = cu(42, y, t)
        ax.plot([16, 28.5], [estudiante[1] + 6, c[1]], color='#90a4ae', lw=0.8)
    tut_cu = [('Gestionar disponibilidad', 74), ('Confirmar / iniciar tutoría', 62), ('Completar tutoría', 50)]
    for t, y in tut_cu:
        c = cu(76, y, t)
        ax.plot([103, 89.5], [tutor[1] + 6, c[1]], color='#90a4ae', lw=0.8)
    adm_cu = [('Ver dashboard', 34), ('Administrar usuarios', 24), ('Administrar materias y tutores', 14)]
    for t, y in adm_cu:
        c = cu(76, y, t)
        ax.plot([103, 89.5], [admin[1] + 6, c[1]], color='#90a4ae', lw=0.8)
    # Un tutor también puede hacer lo que hace un estudiante: se indica con una nota
    ax.text(76, 84, 'El tutor también usa el chatbot\ny consulta tutores', ha='center', fontsize=8, color=GRIS, style='italic')
    guardar(fig, '02_casos_de_uso.png')


# ---------- 3. Diagrama E-R ----------
def tabla(ax, x, top, titulo, campos, w=26):
    h = 4.5 + 3.4 * len(campos) + 1.5
    ax.add_patch(Rectangle((x, top - h), w, h, fc='white', ec=VERDE, lw=1.4))
    ax.add_patch(Rectangle((x, top - 4.5), w, 4.5, fc=VERDE, ec=VERDE))
    ax.text(x + w / 2, top - 2.3, titulo, ha='center', va='center', color='white', fontsize=9, fontweight='bold')
    for i, c in enumerate(campos):
        ax.text(x + 1.2, top - 4.5 - 2.4 - 3.4 * i, c, fontsize=7.5, va='center', fontweight='bold' if i == 0 else 'normal')
    return {'x': x, 'top': top, 'w': w, 'h': h, 'bot': top - h}


def linea(ax, pts, ca=None, cb=None, color=VERDE, estilo='-'):
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color=color, lw=1.4, ls=estilo)
    if ca:
        ax.text(pts[0][0] + 1.2, pts[0][1] + 1.2, ca, fontsize=9, color=color, fontweight='bold')
    if cb:
        ax.text(pts[-1][0] - 2.2, pts[-1][1] + 1.2, cb, fontsize=9, color=color, fontweight='bold')


def er():
    fig, ax = lienzo(14, 15)
    u = tabla(ax, 3, 146, 'auth_user', ['id (PK)', 'username', 'email', 'first_name', 'last_name', 'password', 'is_staff', 'date_joined'])
    pf = tabla(ax, 3, 106, 'api_userprofile', ['id (PK)', 'user_id (FK, 1:1)', 'phone_number', 'email_verified', 'phone_verified'])
    tk = tabla(ax, 3, 78, 'api_passwordresettoken', ['id (PK)', 'user_id (FK)', 'token (único)', 'created_at', 'expires_at', 'used'])
    t = tabla(ax, 52, 146, 'api_tutor', ['id (PK)', 'usuario_id (FK, 1:1)', 'especialidad', 'nivel_experiencia', 'bio', 'tarifa_por_hora', 'calificacion', 'disponible', 'creado_en'])
    d = tabla(ax, 52, 100, 'api_disponibilidad', ['id (PK)', 'tutor_id (FK)', 'dia_semana (0-6)', 'hora_inicio', 'hora_fin', 'activo'])
    r = tabla(ax, 52, 72, 'api_resena', ['id (PK)', 'tutor_id (FK)', 'estudiante_id (FK)', 'tutoria_id (FK)', 'calificacion', 'comentario'])
    ins = tabla(ax, 52, 38, 'api_inscripciongrupo', ['id (PK)', 'grupo_id (FK)', 'estudiante_id (FK)', 'estado', 'asistio'])
    m = tabla(ax, 100, 146, 'api_materia', ['id (PK)', 'nombre (único)', 'descripcion', 'creado_en'])
    tm = tabla(ax, 100, 120, 'api_tutor_materias', ['id (PK)', 'tutor_id (FK)', 'materia_id (FK)'])
    tu = tabla(ax, 100, 98, 'api_tutoria', ['id (PK)', 'tutor_id (FK)', 'materia_id (FK)', 'estudiante_id (FK)', 'fecha_inicio', 'fecha_fin', 'duracion_minutos', 'estado', 'lugar', 'tarifa', 'nota'])
    g = tabla(ax, 100, 52, 'api_grupotutoria', ['id (PK)', 'tutor_id (FK)', 'materia_id (FK)', 'nombre', 'cupos_maximos', 'cupos_disponibles', 'fecha_inicio', 'modalidad', 'estado'])

    linea(ax, [(29, 135), (52, 135)], '1', '1')                                   # user - tutor
    linea(ax, [(16, u['bot']), (16, pf['top'])], None, None)
    ax.text(17.5, u['bot'] - 1.8, '1', fontsize=9, color=VERDE, fontweight='bold')
    ax.text(17.5, pf['top'] + 0.8, '1', fontsize=9, color=VERDE, fontweight='bold')
    linea(ax, [(3, 130), (0.8, 130), (0.8, 70), (3, 70)], '1', 'N')                # user - token
    linea(ax, [(65, t['bot']), (65, d['top'])], None, None)
    ax.text(66.5, t['bot'] - 1.8, '1', fontsize=9, color=VERDE, fontweight='bold')
    ax.text(66.5, d['top'] + 0.8, 'N', fontsize=9, color=VERDE, fontweight='bold')
    linea(ax, [(52, 118), (47, 118), (47, 58), (52, 58)], None, None)             # tutor - resena
    ax.text(48.5, 119, '1', fontsize=9, color=VERDE, fontweight='bold')
    ax.text(46.5, 59.5, 'N', fontsize=9, color=VERDE, fontweight='bold')
    linea(ax, [(78, 112), (100, 112)], '1', 'N')                                   # tutor - tutor_materias
    linea(ax, [(113, m['bot']), (113, tm['top'])], None, None)                     # materia - tutor_materias
    ax.text(114.5, m['bot'] - 1.8, '1', fontsize=9, color=VERDE, fontweight='bold')
    ax.text(114.5, tm['top'] + 0.8, 'N', fontsize=9, color=VERDE, fontweight='bold')
    linea(ax, [(78, 124), (89, 124), (89, 90), (100, 90)], '1', 'N')               # tutor - tutoria
    linea(ax, [(78, 28), (100, 28)], 'N', '1')                                      # inscripcion - grupo
    ax.text(75, 5, 'Notación: 1 = uno, N = muchos. api_tutor_materias es la tabla intermedia de la relación N:M entre tutor y materia.\n'
                   'api_tutoria, api_resena e api_inscripciongrupo también apuntan a auth_user mediante estudiante_id (N:1);\n'
                   'api_tutoria y api_grupotutoria apuntan además a api_materia mediante materia_id (N:1).',
            fontsize=8, ha='center', color=GRIS)
    guardar(fig, '03_modelo_entidad_relacion.png')


# ---------- 4. Diagrama de clases ----------
def clase(ax, x, top, nombre, attrs, metodos, w=32, color=VERDE_C):
    h = 5.5 + 3 * len(attrs) + (3 * len(metodos) + 2 if metodos else 2)
    ax.add_patch(Rectangle((x, top - h), w, h, fc='white', ec=VERDE, lw=1.4))
    ax.add_patch(Rectangle((x, top - 4.5), w, 4.5, fc=color, ec=VERDE, lw=1.4))
    ax.text(x + w / 2, top - 2.3, nombre, ha='center', va='center', fontsize=9, fontweight='bold')
    yy = top - 7.2
    for a in attrs:
        ax.text(x + 1, yy, '+ ' + a, fontsize=7, va='center')
        yy -= 3
    sep = yy + 1.5
    ax.plot([x, x + w], [sep, sep], color=VERDE, lw=1)
    yy = sep - 2.2
    for mt in metodos:
        ax.text(x + 1, yy, '+ ' + mt, fontsize=7, va='center')
        yy -= 3
    return {'x': x, 'top': top, 'w': w, 'bot': top - h}


def asoc(ax, p1, p2, txt='', estilo='-', off=(0, 1)):
    ax.annotate('', xy=p2, xytext=p1, arrowprops=dict(arrowstyle='->', color=VERDE, lw=1.4, ls=estilo))
    if txt:
        ax.text((p1[0] + p2[0]) / 2 + off[0], (p1[1] + p2[1]) / 2 + off[1], txt, fontsize=8, color=VERDE, ha='center')


def clases():
    fig, ax = lienzo(15, 13)
    us = clase(ax, 2, 126, 'User (Django)', ['id: int', 'username: str', 'email: str', 'first_name: str', 'last_name: str'], ['check_password()', 'get_full_name()'])
    pf = clase(ax, 2, 90, 'UserProfile', ['user: User', 'phone_number', 'email_verified: bool'], [])
    tk = clase(ax, 2, 66, 'PasswordResetToken', ['user: User', 'token: str', 'expires_at: datetime', 'used: bool'], ['is_valid(): bool'])
    tu = clase(ax, 40, 126, 'Tutor', ['usuario: User', 'especialidad: str', 'nivel_experiencia: str', 'tarifa_por_hora: Decimal', 'calificacion: float', 'disponible: bool', 'materias: [Materia]'], [])
    di = clase(ax, 40, 88, 'Disponibilidad', ['tutor: Tutor', 'dia_semana: int', 'hora_inicio: time', 'hora_fin: time', 'activo: bool'], [])
    re = clase(ax, 40, 56, 'Resena', ['tutor: Tutor', 'estudiante: User', 'tutoria: Tutoria', 'calificacion: float', 'comentario: str'], [])
    ma = clase(ax, 78, 126, 'Materia', ['nombre: str', 'descripcion: str', 'creado_en: datetime'], ['__str__()'])
    tt = clase(ax, 78, 98, 'Tutoria', ['tutor: Tutor', 'materia: Materia', 'estudiante: User', 'fecha_inicio: datetime', 'fecha_fin: datetime', 'duracion_minutos: int', 'estado: str', 'tarifa: Decimal'], ['save()'])
    ag = clase(ax, 78, 54, 'agenda (módulo)', [], ['ventanas_del_tutor()', 'horarios_libres()', 'disponibilidad_mensual()', 'validar_reserva()'], 32, AMAR)
    gr = clase(ax, 116, 126, 'GrupoTutoria', ['tutor: Tutor', 'materia: Materia', 'cupos_maximos: int', 'cupos_disponibles: int', 'modalidad: str', 'estado: str'], ['esta_lleno: bool'])
    ins = clase(ax, 116, 88, 'InscripcionGrupo', ['grupo: GrupoTutoria', 'estudiante: User', 'estado: str', 'asistio: bool'], [])
    ch = clase(ax, 116, 54, 'ChatbotEngine', ['conocimiento UdeC', 'temas TutoUdec'], ['responder(mensaje, contexto)', 'normalizar(texto)', 'puntuar(tema)'], 32, AMAR)
    asoc(ax, (34, 112), (40, 112), '1:1', off=(0, 1.5))
    asoc(ax, (18, 90), (18, us['bot']), '1:1', off=(3, 0))
    asoc(ax, (18, 66), (18, pf['bot']), 'N:1', off=(3, 0))
    asoc(ax, (56, tu['bot']), (56, 88), '1:N', off=(3, 0))
    asoc(ax, (56, di['bot']), (56, 56), '', '--')
    asoc(ax, (72, 115), (78, 115), 'N:M', off=(0, 1.5))
    asoc(ax, (78, 92), (72, 100), 'N:1', off=(-2, 1.5))
    asoc(ax, (94, ma['bot']), (94, 98), 'N:1', off=(3, 0))
    asoc(ax, (116, 115), (110, 115), 'N:1', off=(0, 1.5))
    asoc(ax, (132, 88), (132, gr['bot']), 'N:1', off=(3, 0))
    asoc(ax, (94, 54), (94, tt['bot']), 'usa', '--', off=(3, 0))
    ax.text(75, 12, 'Flechas continuas: asociación (clave foránea) con su multiplicidad. Flechas punteadas: dependencia de uso.\n'
                    'Color ámbar: clases de servicio (lógica de agenda y motor del chatbot) que no tienen tabla propia.',
            fontsize=8, ha='center', color=GRIS)
    guardar(fig, '04_diagrama_de_clases.png')


# ---------- Flujos ----------
def inicio_fin(ax, x, y, texto, w=22):
    ax.add_patch(FancyBboxPatch((x, y), w, 6, boxstyle='round,pad=0.2,rounding_size=3', fc=GRIS, ec=GRIS))
    ax.text(x + w / 2, y + 3, texto, ha='center', va='center', color='white', fontsize=9, fontweight='bold')


def decision(ax, cx, cy, texto, w=26, h=11):
    ax.add_patch(Polygon([(cx, cy + h / 2), (cx + w / 2, cy), (cx, cy - h / 2), (cx - w / 2, cy)], fc=AMAR, ec='#f9a825', lw=1.3))
    ax.text(cx, cy, texto, ha='center', va='center', fontsize=8)


def flujo_agendar():
    fig, ax = lienzo(10, 13)
    cx = 40
    inicio_fin(ax, cx - 11, 122, 'Inicio')
    pasos = [(112, 'El estudiante abre el perfil de un tutor'), (101, 'La app pide GET /tutores/{id}/\n(datos, materias y reseñas)'),
             (90, 'La app pide la agenda del mes\nGET /disponibilidad_mensual/?mes&duracion'),
             (79, 'El estudiante elige día, hora,\nmateria, duración y lugar')]
    for y, t in pasos:
        caja(ax, cx - 18, y, 36, 7, t, fs=8.5)
    for y in (122, 112, 101, 90):
        flecha(ax, (cx, y), (cx, y - 4.3))
    caja(ax, cx - 18, 68, 36, 7, 'POST /api/tutorias/ con JWT', fs=8.5)
    flecha(ax, (cx, 79), (cx, 75.3))
    flecha(ax, (cx, 68), (cx, 63.5))
    decision(ax, cx, 57, '¿Fecha futura, dentro\nde la disponibilidad\ny sin choque?', 34, 14)
    caja(ax, 62, 53, 26, 8, 'Error 400 con mensaje\nen español', '#ffebee', '#c62828', 8.5)
    flecha(ax, (cx + 17, 57), (62, 57), 'No', off=(0, 1))
    flecha(ax, (75, 53), (75, 36))
    caja(ax, cx - 18, 38, 36, 8, 'Se guarda la tutoría: estado pendiente,\nfecha_fin y tarifa calculadas', fs=8.5)
    flecha(ax, (cx, 50), (cx, 46.3), 'Sí', off=(2, 0))
    caja(ax, cx - 18, 25, 36, 8, 'La app muestra confirmación\ny actualiza la agenda', fs=8.5)
    flecha(ax, (cx, 38), (cx, 33.3))
    flecha(ax, (cx, 25), (cx, 19.5))
    inicio_fin(ax, cx - 11, 13, 'Fin')
    ax.annotate('', xy=(cx + 18, 29), xytext=(75, 36), arrowprops=dict(arrowstyle='->', color=GRIS))
    ax.text(75, 49, '', fontsize=1)
    caja(ax, 62, 32, 26, 6, 'El usuario elige otro horario', '#ffebee', '#c62828', 8)
    ax.annotate('', xy=(cx + 18, 29), xytext=(62, 35), arrowprops=dict(arrowstyle='->', color=GRIS))
    guardar(fig, '05_flujo_agendar_tutoria.png')


def flujo_chatbot():
    fig, ax = lienzo(10, 13)
    cx = 38
    inicio_fin(ax, cx - 11, 122, 'Inicio')
    caja(ax, cx - 18, 111, 36, 7, 'El usuario escribe un mensaje', fs=8.5)
    flecha(ax, (cx, 122), (cx, 118.3))
    caja(ax, cx - 18, 100, 36, 7, 'POST /api/chatbot/chat/\n(mensaje + intenciones previas)', fs=8.5)
    flecha(ax, (cx, 111), (cx, 107.3))
    caja(ax, cx - 18, 89, 36, 7, 'Se normaliza el texto\n(minúsculas, sin tildes)', fs=8.5)
    flecha(ax, (cx, 100), (cx, 96.3))
    caja(ax, cx - 18, 78, 36, 7, 'Se puntúa contra los temas de\nTutoUdec y de la UdeC', fs=8.5)
    flecha(ax, (cx, 89), (cx, 85.3))
    decision(ax, cx, 66, '¿Algún tema supera\nel umbral?', 30, 12)
    flecha(ax, (cx, 78), (cx, 72))
    caja(ax, cx - 18, 46, 36, 7, 'Respuesta del tema\n+ preguntas sugeridas', fs=8.5)
    flecha(ax, (cx, 60), (cx, 53.3), 'Sí', off=(2, 0))
    decision(ax, 72, 66, '¿IA activa\ny con clave?', 22, 11)
    flecha(ax, (cx + 15, 66), (61, 66), 'No', off=(0, 1))
    caja(ax, 62, 46, 24, 8, 'Se consulta al modelo\nde IA (OpenAI)', fs=8)
    flecha(ax, (72, 60.5), (74, 54), 'Sí', off=(3, 0))
    caja(ax, 62, 80, 26, 8, 'Respuesta honesta:\n"no tengo información confiable"\n+ remite a soporte', '#ffebee', '#c62828', 8)
    flecha(ax, (72, 71.5), (75, 80), 'No', off=(3, 0))
    caja(ax, cx - 18, 33, 36, 7, 'Se arma el JSON empresarial 5.0\n(answer, follow_up_question, confidence...)', fs=8.5)
    flecha(ax, (cx, 46), (cx, 40.3))
    ax.annotate('', xy=(cx + 18, 36), xytext=(74, 46), arrowprops=dict(arrowstyle='->', color=GRIS))
    ax.annotate('', xy=(cx + 18, 38), xytext=(88, 83), arrowprops=dict(arrowstyle='->', color=GRIS, connectionstyle='arc3,rad=-0.25'))
    caja(ax, cx - 18, 20, 36, 7, 'La web o la app muestran la respuesta\ny la pregunta de seguimiento', fs=8.5)
    flecha(ax, (cx, 33), (cx, 27.3))
    flecha(ax, (cx, 20), (cx, 14.5))
    inicio_fin(ax, cx - 11, 8, 'Fin')
    guardar(fig, '06_flujo_chatbot.png')


def flujo_recuperar():
    fig, ax = lienzo(10, 11)
    cx = 38
    inicio_fin(ax, cx - 11, 102, 'Inicio')
    caja(ax, cx - 18, 91, 36, 7, 'El usuario escribe su correo o usuario', fs=8.5)
    flecha(ax, (cx, 102), (cx, 98.3))
    caja(ax, cx - 18, 80, 36, 7, 'POST /auth/request_password_reset/', fs=8.5)
    flecha(ax, (cx, 91), (cx, 87.3))
    decision(ax, cx, 66, '¿Existe la cuenta?', 28, 11)
    flecha(ax, (cx, 80), (cx, 71.5))
    caja(ax, 60, 62, 28, 8, 'Se responde igual (no se revela\nsi la cuenta existe)', '#f5f5f5', GRIS, 8)
    flecha(ax, (cx + 14, 66), (60, 66), 'No', off=(0, 1))
    caja(ax, cx - 18, 46, 36, 8, 'Se crea un token de 64 caracteres\n(vence en 1 hora) y se envía por correo', fs=8.5)
    flecha(ax, (cx, 60.5), (cx, 54.3), 'Sí', off=(2, 0))
    caja(ax, cx - 18, 33, 36, 7, 'El usuario escribe el código y la\nnueva contraseña (mínimo 8 caracteres)', fs=8.5)
    flecha(ax, (cx, 46), (cx, 40.3))
    caja(ax, cx - 18, 21, 36, 7, 'POST /auth/confirm_password_reset/', fs=8.5)
    flecha(ax, (cx, 33), (cx, 28.3))
    caja(ax, cx - 18, 9, 36, 7, 'Token válido y sin usar: se cambia la\ncontraseña y el token queda usado', fs=8.5)
    flecha(ax, (cx, 21), (cx, 16.3))
    inicio_fin(ax, cx - 11, 0, 'Fin')
    flecha(ax, (cx, 9), (cx, 6.3))
    guardar(fig, '07_flujo_recuperar_contrasena.png')


def despliegue():
    fig, ax = lienzo(11, 6)
    caja(ax, 3, 38, 22, 14, 'Equipo del desarrollador\nGit + VS Code\nPython · Node', AZUL, '#1565c0', 9, True)
    caja(ax, 36, 38, 22, 14, 'GitHub\nParraxzy26/\nTutoUdecProyect', '#eeeeee', GRIS, 9, True)
    caja(ax, 69, 38, 36, 14, 'Azure VM "Backend"\ngit pull + reinicio de gunicorn\nnginx publica /var/www/tutoudec', VERDE_C, VERDE, 9, True)
    caja(ax, 36, 10, 22, 14, 'Expo EAS Build\n(nube)\ngenera el APK', AMAR, '#f9a825', 9, True)
    caja(ax, 69, 10, 36, 14, 'Repositorio\nTutoUdec-Final.apk\ninstalable en Android', '#ede7f6', '#5e35b1', 9, True)
    flecha(ax, (25, 45), (36, 45), 'git push', off=(0, 1.5))
    flecha(ax, (58, 45), (69, 45), 'az vm run-command', off=(0, 1.5))
    flecha(ax, (47, 38), (47, 24), 'código', off=(5, 0))
    flecha(ax, (58, 17), (69, 17), 'APK', off=(0, 1.5))
    guardar(fig, '08_despliegue.png')


if __name__ == '__main__':
    arquitectura(); casos_uso(); er(); clases(); flujo_agendar(); flujo_chatbot(); flujo_recuperar(); despliegue()
    print('listo')
