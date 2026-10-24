"""Cálculo de disponibilidad mensual de un tutor y validación de reservas."""
from datetime import date, datetime, time, timedelta

from django.utils import timezone

from .models import Disponibilidad, Tutoria

ESTADOS_ACTIVOS = ('pendiente', 'confirmada', 'en_progreso')
# Si el tutor aún no configuró horarios se asume lunes a viernes, 8:00 a 18:00.
VENTANA_POR_DEFECTO = [(d, time(8, 0), time(18, 0)) for d in range(5)]
DURACIONES_VALIDAS = (30, 45, 60, 90, 120)


def _aware(dt):
    return timezone.make_aware(dt, timezone.get_current_timezone())


def ventanas_del_tutor(tutor):
    franjas = list(
        Disponibilidad.objects.filter(tutor=tutor, activo=True)
        .values_list('dia_semana', 'hora_inicio', 'hora_fin')
    )
    return franjas or VENTANA_POR_DEFECTO


def _ocupados(tutor, desde, hasta):
    qs = Tutoria.objects.filter(
        tutor=tutor, estado__in=ESTADOS_ACTIVOS,
        fecha_inicio__lt=hasta, fecha_inicio__gte=desde - timedelta(hours=6),
    )
    return [(t.fecha_inicio, t.fecha_inicio + timedelta(minutes=t.duracion_minutos)) for t in qs]


def _choca(inicio, fin, ocupados):
    return any(inicio < o_fin and fin > o_ini for o_ini, o_fin in ocupados)


def horarios_libres(tutor, dia, duracion, ventanas=None, ocupados=None, ahora=None):
    """Lista de inicios (datetime con zona) libres para un día y una duración."""
    ventanas = ventanas if ventanas is not None else ventanas_del_tutor(tutor)
    ahora = ahora or timezone.now()
    if ocupados is None:
        ocupados = _ocupados(tutor, _aware(datetime.combine(dia, time.min)), _aware(datetime.combine(dia, time.max)))
    libres = []
    for dia_semana, h_ini, h_fin in ventanas:
        if dia_semana != dia.weekday():
            continue
        cursor = _aware(datetime.combine(dia, h_ini))
        limite = _aware(datetime.combine(dia, h_fin))
        paso = timedelta(minutes=duracion)
        while cursor + paso <= limite:
            if cursor > ahora and not _choca(cursor, cursor + paso, ocupados):
                libres.append(cursor)
            cursor += paso
    return sorted(set(libres))


def disponibilidad_mensual(tutor, anio, mes, duracion):
    primero = date(anio, mes, 1)
    siguiente = date(anio + (mes == 12), mes % 12 + 1, 1)
    ventanas = ventanas_del_tutor(tutor)
    ocupados = _ocupados(tutor, _aware(datetime.combine(primero, time.min)), _aware(datetime.combine(siguiente, time.min)))
    ahora = timezone.now()
    dias = []
    dia = primero
    while dia < siguiente:
        libres = horarios_libres(tutor, dia, duracion, ventanas, ocupados, ahora)
        if libres:
            dias.append({
                'fecha': dia.isoformat(),
                'horarios': [h.astimezone(timezone.get_current_timezone()).strftime('%H:%M') for h in libres],
            })
        dia += timedelta(days=1)
    return {'mes': f'{anio:04d}-{mes:02d}', 'duracion_minutos': duracion, 'dias': dias}


def validar_reserva(tutor, estudiante, inicio, duracion, ignorar_id=None):
    """Devuelve un mensaje de error o None si la tutoría se puede registrar."""
    if tutor.usuario_id == estudiante.id:
        return 'No puedes agendar una tutoría contigo mismo.'
    if not tutor.disponible:
        return 'El tutor no está disponible por ahora.'
    if inicio <= timezone.now():
        return 'La fecha y hora deben ser futuras.'
    local = inicio.astimezone(timezone.get_current_timezone())
    fin = inicio + timedelta(minutes=duracion)
    dentro = any(
        d == local.date().weekday()
        and _aware(datetime.combine(local.date(), h_ini)) <= inicio
        and fin <= _aware(datetime.combine(local.date(), h_fin))
        for d, h_ini, h_fin in ventanas_del_tutor(tutor)
    )
    if not dentro:
        return 'Ese horario está fuera de la disponibilidad del tutor. Elige otro de la agenda.'
    ocupados = _ocupados(tutor, inicio - timedelta(hours=6), fin)
    if _choca(inicio, fin, ocupados):
        return 'El tutor ya tiene una tutoría en ese horario. Elige otro.'
    return None
