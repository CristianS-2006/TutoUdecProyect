"""Base de conocimiento de la Universidad de Cundinamarca (compilada el 23/10/2026).

Los datos marcados como variables (fechas, costos, oferta por sede) siempre remiten al sitio oficial.
"""

WEB = 'www.ucundinamarca.edu.co'
VERIFY = f'\n\nℹ️ Este dato puede cambiar; confírmalo en {WEB}.'

UDEC_TOPICS = {
    'universidad': {
        'keywords': ['universidad', 'udec', 'ucundinamarca', 'cundinamarca', 'unicundi', 'que es la udec',
                     'que es la universidad', 'es publica', 'es privada', 'publica o privada', 'naturaleza',
                     'cuantos estudiantes', 'estudiantes tiene', 'sue'],
        'answer': 'La Universidad de Cundinamarca (UCundinamarca, también llamada UdeC) es una universidad '
                  'pública del orden territorial (departamental), vinculada al Ministerio de Educación y '
                  'parte del Sistema Universitario Estatal. Su sede principal está en Fusagasugá.\n\nNació en '
                  '1969 como Instituto Técnico Universitario de Cundinamarca (ITUC) y fue reconocida como '
                  'universidad en 1992. Hoy tiene 1 sede principal, 2 seccionales (Girardot y Ubaté) y '
                  'extensiones en Chía, Facatativá, Soacha y Zipaquirá, con cerca de 12.000 estudiantes (2024). '
                  'Su lema es "Ex umbra in solem" (De la oscuridad a la luz).'
                  '\n\nNo confundas: la Universidad Colegio Mayor de Cundinamarca es otra institución, en Bogotá.',
        'follow': ['¿Cuál es su historia?', '¿Qué sedes tiene?', '¿Qué carreras hay?'],
    },
    'historia': {
        'keywords': ['historia de la universidad', 'historia de la udec', 'historia', 'fundada', 'fundacion', 'cuando se creo', 'cuando nacio', 'origen', 'ituc',
                     'anos tiene', 'antigua', 'lema', 'escudo'],
        'answer': 'Línea de tiempo de la UCundinamarca:\n• 1969: la Asamblea de Cundinamarca crea el Instituto '
                  'Técnico Universitario de Cundinamarca (ITUC), Ordenanza 045.\n• 1970: inician clases en '
                  'Fusagasugá.\n• 1972–1974: nacen las seccionales de Girardot y Ubaté.\n• 1992: se reconoce como '
                  'Universidad (Resolución 19530) y se crea la extensión Facatativá.\n• 1999: extensiones de Chía '
                  'y Zipaquirá (Soacha hacia el año 2000).\n• 2015: nuevo Estatuto General.\n• 2016: sede propia en '
                  'Chía y primer posgrado virtual.\n• 2021–2022: aprobación e inicio del Doctorado en Ciencias de '
                  'la Educación y convenio de "Matrícula Cero".\n• 2024: nueva misión y visión.',
        'follow': ['¿Cuál es su misión y visión?', '¿Qué sedes tiene?'],
    },
    'mision': {
        'keywords': ['mision', 'vision', 'valores', 'proposito', 'meit', 'medit', 'modelo educativo',
                     'transmoderna', 'translocal', 'transmoderno', 'campo de aprendizaje', 'gestores'],
        'answer': 'Misión: la UCundinamarca se define como una universidad pública "translocal" y '
                  '"transmoderna", una organización social del conocimiento y del aprendizaje, democrática y '
                  'autónoma, cuya calidad viene de la formación, la ciencia, la tecnología, la investigación, la '
                  'innovación y la interacción social.\n\nVisión: para 2035 aspira a ser reconocida en '
                  'Cundinamarca como una organización de alta calidad, con impacto y carácter emprendedor.\n\n'
                  'Su modelo educativo es el MEDIT (Modelo Educativo Digital Transmoderno): está centrado en la '
                  'persona, usa la metodología de Campos de Aprendizaje y se apoya en tecnología y territorio. '
                  'A los docentes los llama "Gestores del Conocimiento y el Aprendizaje".',
        'follow': ['¿Qué sedes tiene?', '¿Tiene acreditación?'],
    },
    'sedes': {
        'keywords': ['sedes', 'seccional', 'seccionales', 'extension', 'extensiones', 'donde queda', 'donde esta',
                     'direccion', 'ubicacion', 'ubicada', 'fusagasuga', 'facatativa', 'girardot', 'zipaquira',
                     'soacha', 'ubate', 'chia', 'campus', 'sede', 'en que ciudades', 'cundinamarca sedes',
                     'chocontá', 'choconta'],
        'answer': 'Sedes de la UCundinamarca:\n• Fusagasugá (sede principal): Diagonal 18 No. 20-29.\n• '
                  'Seccional Girardot: Carrera 19 No. 24-209, barrio Gaitán.\n• Seccional Ubaté: Calle 6 No. '
                  '9-80.\n• Extensión Chía: Autopista Chía–Cajicá, sector El Cuarenta.\n• Extensión Facatativá.\n• '
                  'Extensión Soacha (se anunció una nueva sede).\n• Extensión Zipaquirá (sede de Música).\n\n'
                  'Las más grandes por matrícula son Fusagasugá, Facatativá, Chía y Soacha. No tengo verificadas '
                  'las direcciones exactas de Facatativá, Soacha y Zipaquirá; consúltalas en ' + WEB + '.',
        'follow': ['¿Qué carreras hay por sede?', '¿Cómo contacto a la universidad?'],
    },
    'programas': {
        'keywords': ['programas', 'carreras', 'carrera', 'pregrado', 'que puedo estudiar', 'oferta academica',
                     'que se estudia', 'facultades', 'facultad', 'ofrece', 'licenciatura', 'ingenieria',
                     'que carreras', 'programas academicos'],
        'answer': 'La UCundinamarca tiene 7 facultades y alrededor de 18–20 programas de pregrado, entre ellos:\n'
                  '• Administrativas, Económicas y Contables: Administración de Empresas, Contaduría Pública.\n'
                  '• Agropecuarias: Ingeniería Agronómica, Ambiental, Topográfica y Geomática, Zootecnia, '
                  'Medicina Veterinaria y Zootecnia.\n• Deporte y Educación Física: Profesional en Ciencias del '
                  'Deporte, Lic. en Educación Física.\n• Educación: Lic. en Ciencias Sociales.\n• Ingeniería: '
                  'Sistemas y Computación, Software, Industrial, Electrónica, Mecatrónica.\n• Salud: Enfermería, '
                  'Psicología.\n• Sociales y Humanidades: Música.\n\nCada programa se ofrece solo en algunas '
                  'sedes y la oferta cambia por convocatoria, así que confirma sede y disponibilidad en ' + WEB + '.',
        'follow': ['¿Qué carreras hay en Girardot?', '¿Dónde estudio Ingeniería de Sistemas?',
                   '¿Hay posgrados?'],
    },
    'carreras_sede': {
        'keywords': ['que carreras hay en', 'carreras en girardot', 'carreras hay en', 'que hay en girardot', 'donde puedo estudiar',
                     'donde estudio', 'donde se estudia', 'carreras en soacha', 'que hay en soacha',
                     'carreras en chia', 'carreras en ubate', 'carreras en facatativa', 'carreras en fusagasuga',
                     'carreras en zipaquira', 'por sede', 'musica', 'psicologia', 'enfermeria', 'sistemas',
                     'software', 'zootecnia', 'agronomia', 'veterinaria', 'contaduria', 'administracion de empresas',
                     'electronica', 'industrial', 'topografica', 'deporte', 'mecatronica'],
        'answer': 'Según la información que manejo (puede haber cambios):\n• Fusagasugá: Administración, '
                  'Contaduría, Agronómica, Zootecnia, Sistemas y Computación, Electrónica, Lic. Ciencias Sociales.\n'
                  '• Girardot: Enfermería, Administración, Ingeniería Ambiental e Ingeniería de Software.\n'
                  '• Ubaté: Administración, Contaduría, Sistemas y Computación, Zootecnia.\n• Chía: '
                  'Administración, Contaduría, Sistemas y Computación, Industrial.\n• Facatativá: Administración, '
                  'Contaduría, Sistemas y Computación, Agronómica, Ambiental, Psicología.\n• Soacha: '
                  'Administración, Contaduría, Ciencias del Deporte, Industrial, Software, Topográfica y '
                  'Geomática.\n• Zipaquirá: Música.' + VERIFY,
        'follow': ['¿Cómo me inscribo?', '¿Cuánto cuesta la matrícula?'],
    },
    'posgrados': {
        'keywords': ['posgrado', 'posgrados', 'maestria', 'maestrias', 'especializacion', 'especializaciones',
                     'doctorado', 'virtual', 'educacion continuada', 'diplomado', 'curso de extension'],
        'answer': 'El Instituto de Posgrados ofrece:\n• Especializaciones (la mayoría 100 % virtuales), por ejemplo '
                  'en Gestión Pública, Marketing Digital, Analítica y Ciencia de Datos, Seguridad de la '
                  'Información, Gerencia para la Transformación Digital, Agronegocios Sostenibles, Intervención '
                  'Psicosocial.\n• Maestrías virtuales en Ciencias Agrarias (Hortifruticultura), Gestión '
                  'Ambiental para el Desarrollo Sostenible y Nutrición y Alimentación Animal.\n• Doctorado en '
                  'Ciencias de la Educación (desde 2022).\n• Educación continuada.\n\nInformación por WhatsApp de '
                  'posgrados: 317 401 5845.' + VERIFY,
        'follow': ['¿Qué requisitos piden?', '¿Cómo contacto a la universidad?'],
    },
    'admision_universidad': {
        'keywords': ['admision', 'admisiones', 'aspirante', 'inscribirme en la universidad', 'entrar a la udec',
                     'inscribo en la universidad', 'inscribo en la udec', 'inscripcion en la universidad',
                     'ingresar a la universidad', 'proceso de admision', 'requisitos de inscripcion',
                     'requisitos para entrar', 'pin', 'icfes', 'saber 11', 'puntaje', 'examen de admision',
                     'prueba de admision', 'como entro', 'como ingreso', 'documentos para inscribirme',
                     'como estudiar en la udec', 'como estudiar en la universidad'],
        'answer': 'Para inscribirte a un pregrado en la UCundinamarca:\n1. Diligencia el formulario de '
                  'inscripción en la web.\n2. Adquiere el PIN y paga los derechos de inscripción (PSE se refleja '
                  'al instante; en banco puede tardar hasta 72 horas).\n3. Reúne: título y acta de bachiller, '
                  'resultado de la prueba Saber 11 (ICFES), documento de identidad y afiliación vigente a salud.\n'
                  '4. Espera los resultados y, si te admiten, formaliza la matrícula en Admisiones y Registro.\n\n'
                  'Solo puedes inscribirte a un programa por convocatoria. Según el FAQ oficial no hay puntaje '
                  'mínimo de ICFES, aunque algunos programas pueden tener pruebas o procesos de selección '
                  'adicionales. Las fechas cambian cada periodo: consulta el calendario académico en ' + WEB + '.',
        'follow': ['¿Cuánto cuesta la matrícula?', '¿Cuándo son las inscripciones?', '¿Hay gratuidad?'],
    },
    'calendario': {
        'keywords': ['calendario', 'calendario academico', 'cuando son las inscripciones', 'fechas de inscripcion',
                     'cuando inicia', 'inicio de clases', 'cierre de inscripciones', 'proximo semestre',
                     'proxima convocatoria', '2027', 'periodo academico', 'fecha de grado', 'grados'],
        'answer': 'No tengo las fechas del próximo periodo (por ejemplo 2027-1) y prefiero no inventarlas. '
                  'Como referencia: las inscripciones del primer periodo de 2026 cerraron el 15 de mayo de 2026, y '
                  'en otros años las de pregrado se anunciaron entre septiembre y octubre. Para fechas exactas de '
                  'inscripción, pruebas, matrícula, clases y grados, mira el Calendario académico y la sección '
                  'Admisiones y Registro en ' + WEB + '.',
        'follow': ['¿Cómo me inscribo?', '¿Cómo contacto a la universidad?'],
    },
    'matricula_costos': {
        'keywords': ['matricula', 'cuanto cuesta la matricula', 'valor de la matricula', 'costo del semestre',
                     'cuanto cuesta estudiar', 'derechos pecuniarios', 'cuanto vale la universidad',
                     'pago de matricula', 'valor del semestre', 'cuanto se paga', 'icetex', 'financiacion',
                     'semestre cuesta', 'costo de estudiar'],
        'answer': 'La UCundinamarca es pública, así que la matrícula es mucho menor que en una privada, y se '
                  'liquida según tu situación. Hay política de gratuidad para estudiantes de estratos 1, 2 y 3 '
                  'que cumplan requisitos. Los derechos pecuniarios (carné, seguro estudiantil, etc.) no entran '
                  'en la gratuidad. También aparece Icetex como opción de financiación.\n\nNo cuento con la tabla '
                  'vigente de valores, así que no te daré una cifra que pueda estar mal. Consúltala en ' + WEB +
                  ' (Admisiones y Registro) o escribe a info@ucundinamarca.edu.co.',
        'follow': ['¿Cómo funciona la gratuidad?', '¿Qué apoyos ofrece Bienestar?'],
    },
    'gratuidad': {
        'keywords': ['gratuidad', 'matricula cero', 'gratis la universidad', 'estudiar gratis',
                     'estrato 1', 'estrato 2', 'estrato 3', 'beneficio de gratuidad', 'subsidio', 'beca', 'becas'],
        'answer': 'La gratuidad en la matrícula es una política nacional (con el Ministerio de Educación) para '
                  'pregrado en estratos 1, 2 y 3 que cumplan requisitos, por ejemplo no tener ya un título '
                  'profesional ni estar cursando otro pregrado en una institución pública. Desde 2021 existe el '
                  'convenio "Matrícula Cero".\n\nNo es automática ni garantizada: el Ministerio valida cada caso y '
                  'la cobertura depende de los recursos asignados (se prioriza a estudiantes antiguos y luego a '
                  'nuevos). No doy asesoría legal ni financiera; para tu caso consulta Admisiones y Registro o ' + WEB + '.',
        'follow': ['¿Qué apoyos ofrece Bienestar?', '¿Cómo me inscribo?'],
    },
    'bienestar': {
        'keywords': ['bienestar', 'bienestar universitario', 'restaurante', 'restaurante universitario',
                     'salud mental', 'psicologo', 'deporte', 'cultura', 'apoyo socioeconomico', 'permanencia',
                     'discapacidad', 'inclusion', 'acoso', 'discriminacion', 'violencia de genero', 'apoyos'],
        'answer': 'Bienestar Universitario de la UCundinamarca (con coordinación en cada sede) ofrece:\n• Apoyos '
                  'socioeconómicos y restaurante universitario para estudiantes de pregrado con limitaciones '
                  'económicas.\n• Salud y apoyo psicosocial, y promoción de salud mental.\n• Actividades '
                  'culturales y deportivas (la universidad tiene el Centro Académico Deportivo, CAD).\n• '
                  'Inclusión de personas con discapacidad y protocolos contra el acoso, la discriminación y la '
                  'violencia de género.\n\nHorarios, requisitos y convocatorias varían por sede; pregunta en tu '
                  'sede o en ' + WEB + '.',
        'follow': ['¿Hay gratuidad?', '¿Cómo contacto a la universidad?'],
    },
    'acreditacion': {
        'keywords': ['acreditacion', 'acreditada', 'acreditado', 'alta calidad', 'cna', 'snies', 'calidad',
                     'registro calificado', 'reconocida', 'investigacion', 'grupos de investigacion', 'semilleros'],
        'answer': 'La UCundinamarca se identifica como "universidad de docencia que hace investigación". Su meta '
                  'es la acreditación institucional multicampus y el Plan Rectoral 2023–2027 contempla presentar '
                  '13 programas a acreditación de alta calidad; algunos, como Ingeniería Ambiental en Girardot, ya '
                  'han tenido visita del CNA. Cuenta con grupos y semilleros de investigación.\n\nNo puedo '
                  'asegurar que un programa específico tenga acreditación vigente; verifícalo en el SNIES o en ' +
                  WEB + '.',
        'follow': ['¿Qué carreras hay?', '¿Cuál es su misión y visión?'],
    },
    'directivos': {
        'keywords': ['rector', 'rectora', 'directivos', 'vicerrector', 'vicerrectora', 'quien dirige', 'gobernador',
                     'consejo superior', 'quien es el rector', 'secretaria general', 'gobierno universitario'],
        'answer': 'Según el Informe de Sostenibilidad 2024, el rector (periodo 2023–2027) es Adriano Muñoz '
                  'Barrera, la Secretaria General es Isabel Quintero Uribe y la Vicerrectora Académica es Vilma '
                  'Moreno Melo. El Consejo Superior Universitario, máxima autoridad de gobierno, lo preside el '
                  'Gobernador de Cundinamarca.' + VERIFY.replace('dato', 'cargo'),
        'follow': ['¿Qué sedes tiene?', '¿Cómo contacto a la universidad?'],
    },
    'contacto_udec': {
        'keywords': ['contactar la universidad', 'contacto de la universidad', 'telefono de la universidad',
                     'correo de la universidad', 'contacto udec', 'linea gratuita', 'info@', 'pqrf',
                     'yo denuncio', 'denunciar', 'queja de la universidad', 'whatsapp', 'redes de la universidad',
                     'contactar a la udec', 'como contacto a la universidad', 'comunicarme con la universidad',
                     'telefono udec', 'correo udec', 'atencion al ciudadano', 'tiktok'],
        'answer': 'Contacto de la UCundinamarca:\n• Teléfono: (+57 601) 828 1483.\n• Línea gratuita: 018000 '
                  '180414.\n• Correo general: info@ucundinamarca.edu.co (Secretaría General: '
                  'sgeneral@ucundinamarca.edu.co).\n• Posgrados (WhatsApp): 317 401 5845.\n• Web: ' + WEB + '\n• '
                  'Quejas o denuncias: canal "Yo Denuncio" y sistema PQRF en la web.\n\nEste es el contacto de la '
                  'universidad; para problemas de la app TutoUdec escribe a tutoudec.soporte@gmail.com.' + VERIFY,
        'follow': ['¿Qué sedes tiene?', '¿Cómo me inscribo?'],
    },
    'colegio_mayor': {
        'keywords': ['colegio mayor', 'universidad mayor', 'colegio mayor de cundinamarca'],
        'answer': 'Ojo: la Universidad Colegio Mayor de Cundinamarca es una institución distinta, ubicada en '
                  'Bogotá (universidadmayor.edu.co). TutoUdec está pensada para la Universidad de Cundinamarca '
                  '(UCundinamarca), con sede principal en Fusagasugá.',
        'follow': ['¿Qué es la UdeC?'],
    },
    'transparencia_ambiente': {
        'keywords': ['sostenibilidad', 'ambiental', 'huella de carbono', 'responsabilidad social', 'iso',
                     'certificaciones', 'reciclaje', 'transparencia', 'ods'],
        'answer': 'En su Informe de Sostenibilidad 2024 la UCundinamarca reporta certificaciones ISO 45001 '
                  '(seguridad y salud en el trabajo) y efr (conciliación laboral-familiar), procesos ISO 14001 en '
                  'gestión ambiental (Girardot y Facatativá), medición de huella de carbono, reforestación, '
                  'programas posconsumo y un sistema antisoborno con el canal "Yo Denuncio".',
        'follow': ['¿Qué es la UdeC?'],
    },
}
