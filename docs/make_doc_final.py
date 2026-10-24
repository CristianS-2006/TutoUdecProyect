import sys
from docgen_base import *
from docgen_p1 import parte1
from docgen_p2 import parte2
from docgen_p3 import parte3

SALIDA = os.path.join(RAIZ, 'Documentacion_Tecnica_TutoUdec_Final.docx')

ANEXOS = [
    ('A.1 backend/api/models.py', 'Modelos del dominio.', 'backend/api/models.py'),
    ('A.2 backend/api/serializers.py', 'Serializadores y campos calculados.', 'backend/api/serializers.py'),
    ('A.3 backend/api/agenda.py', 'Agenda mensual y validación de reservas.', 'backend/api/agenda.py'),
    ('A.4 backend/api/permissions.py y pagination.py', 'Permisos y paginación.', None),
    ('A.5 backend/api/urls.py y backend/urls.py', 'Enrutamiento.', None),
    ('A.6 backend/api/views.py', 'Vistas y acciones de la API.', 'backend/api/views.py'),
    ('A.7 backend/api/chatbot_engine.py', 'Motor del asistente.', 'backend/api/chatbot_engine.py'),
    ('A.8 backend/api/ai_chatbot.py', 'Conexión opcional con un proveedor de IA.', 'backend/api/ai_chatbot.py'),
    ('A.9 backend/api/tests.py', 'Pruebas automatizadas.', 'backend/api/tests.py'),
    ('A.10 backend/settings.py', 'Configuración de Django (sin secretos: se leen del entorno).', 'backend/settings.py'),
    ('A.11 deploy/nginx-tutoudec.conf', 'Configuración de nginx.', 'deploy/nginx-tutoudec.conf'),
    ('A.12 mobile/src/services/api.js', 'Cliente HTTP de la aplicación móvil.', 'mobile/src/services/api.js'),
    ('A.13 mobile/src/screens/main/TutorDetailScreen.js', 'Perfil del tutor con calendario mensual.', 'mobile/src/screens/main/TutorDetailScreen.js'),
    ('A.14 mobile/src/screens/main/MateriasScreen.js', 'Pantalla de materias.', 'mobile/src/screens/main/MateriasScreen.js'),
    ('A.15 web/src/router/index.js', 'Rutas y guardas de la web.', 'web/src/router/index.js'),
    ('A.16 web/src/views/TutoresView.vue', 'Vista de tutores.', 'web/src/views/TutoresView.vue'),
]


def anexos():
    H('Anexos: código fuente')
    P('Los anexos reproducen el código fuente más relevante tal como está en el repositorio en el momento de generar este documento. Se incluyen para que quien evalúe el trabajo pueda comprobar que lo descrito en los capítulos anteriores corresponde a código real. El repositorio completo está en https://github.com/Parraxzy26/TutoUdecProyect.')
    for titulo, desc, ruta in ANEXOS:
        H(titulo, 2, True)
        P(desc)
        if ruta:
            CODE(LEER(ruta), 7)
        elif 'permissions' in titulo:
            CODE(LEER('backend/api/permissions.py') + '\n\n' + LEER('backend/api/pagination.py'), 7)
        else:
            CODE('# backend/api/urls.py\n' + LEER('backend/api/urls.py') + '\n\n# backend/urls.py\n' + LEER('backend/urls.py'), 7)


def main():
    configurar()
    pie_y_encabezado('TutoUdec · Documentación técnica final')
    portada('TutoUdec', 'Plataforma de tutorías para la Universidad de Cundinamarca',
            ['Documentación técnica final', 'API Django · Web Vue 3 · App móvil Expo · PostgreSQL en Azure', 'Octubre de 2026',
             'Repositorio: github.com/Parraxzy26/TutoUdecProyect'])
    d.add_page_break()
    tp = d.add_paragraph(); rr = tp.add_run('Contenido'); rr.bold = True; rr.font.size = Pt(18); rr.font.color.rgb = VERDE
    TOC()
    parte1()
    parte2()
    parte3()
    anexos()
    d.save(SALIDA)
    print('guardado', SALIDA)


if __name__ == '__main__':
    main()
