import os
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import django
django.setup()

from django.contrib.auth.models import User

username = os.getenv('DJANGO_SUPERUSER_USERNAME')
email = os.getenv('DJANGO_SUPERUSER_EMAIL')
password = os.getenv('DJANGO_SUPERUSER_PASSWORD')
if not all((username, email, password)):
    sys.exit(
        'Configura DJANGO_SUPERUSER_USERNAME, DJANGO_SUPERUSER_EMAIL y '
        'DJANGO_SUPERUSER_PASSWORD en el entorno antes de ejecutar este script.'
    )

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f'Superusuario creado: {username}')
else:
    print(f'El superusuario {username} ya existe')