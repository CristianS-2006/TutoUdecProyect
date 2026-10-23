"""Visor de la base de datos en tiempo real (solo lectura).

Uso:  python backend/db_live.py            # se refresca cada 3 s
      python backend/db_live.py --once     # una sola lectura
Usa la misma base que el backend (SQLite local o PostgreSQL via DATABASE_URL).
"""
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

import django  # noqa: E402

django.setup()

from django.apps import apps  # noqa: E402
from django.db import connection  # noqa: E402


def snapshot():
    engine = connection.settings_dict['ENGINE'].rsplit('.', 1)[-1]
    lines = [f"Base de datos: {engine} | {time.strftime('%Y-%m-%d %H:%M:%S')}", '']
    lines.append(f"{'Tabla':40} {'Registros':>10}")
    lines.append('-' * 51)
    for model in sorted(apps.get_models(), key=lambda m: m._meta.db_table):
        lines.append(f"{model._meta.db_table:40} {model.objects.count():>10}")
    lines.append('')
    lines.append('Últimos registros de tablas del proyecto:')
    for model in apps.get_app_config('api').get_models():
        last = model.objects.order_by('-pk')[:3]
        lines.append(f"  [{model._meta.db_table}]")
        for obj in last:
            lines.append(f"    #{obj.pk} {str(obj)[:70]}")
    return '\n'.join(lines)


if __name__ == '__main__':
    once = '--once' in sys.argv
    while True:
        out = snapshot()
        if not once:
            os.system('cls' if os.name == 'nt' else 'clear')
        print(out)
        if once:
            break
        time.sleep(3)
