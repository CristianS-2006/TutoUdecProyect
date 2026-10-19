# TutoUdec - Sistema de Tutorías

Sistema de gestión de tutorías académicas que conecta tutores y estudiantes. Incluye un backend en Django REST Framework, una aplicación móvil en React Native (Expo) y una versión web en Vue.js.

## Estructura del Proyecto

```
├── backend/          # API REST en Django
├── mobile/           # Aplicación móvil en React Native (Expo)
├── web/              # Aplicación web en Vue.js
├── API_DOCUMENTATION.md
└── README.md
```

## Requisitos Previos

- Python 3.12-3.14
- Node.js 18+
- PostgreSQL 14+ (para el backend)
- Git

---

## 🚀 Inicio Rápido

### Backend

```powershell
# 1. Entrar a la carpeta
cd backend

# 2. Crear entorno virtual
python -m venv venv

# 3. Activar entorno virtual
# En Windows:
.\venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate

# 4. Instalar dependencias
pip install -r requirements.txt

# 5. Para desarrollo local se usa SQLite automáticamente.
#    Para PostgreSQL, configura las variables indicadas abajo.

# 6. Aplicar las migraciones incluidas
python manage.py migrate

# 7. Crear superusuario (opcional)
python manage.py createsuperuser

# 8. Iniciar servidor
python manage.py runserver 0.0.0.0:8000
```

El backend estará disponible en: http://localhost:8000

---

### Aplicación Móvil

```powershell
# 1. Entrar a la carpeta
cd mobile

# 2. Instalar dependencias del lockfile
npm ci --legacy-peer-deps

# 3. Limpiar caché (si hay errores)
npx expo start -c

# 4. Iniciar con LAN (para conectar desde celular en la misma red)
npx expo start --lan
```

> **Nota:** Para conectar desde un dispositivo físico, asegúrate de que tu PC y celular estén en la misma red Wi-Fi.

---

### Aplicación Web

```powershell
# 1. Entrar a la carpeta
cd web

# 2. Instalar dependencias del lockfile
npm ci

# 3. Iniciar servidor de desarrollo
npm run dev
```

---

## 📁 Documentación por Carpeta

- **[backend/README.md](backend/README.md)** - Documentación completa del backend (modelos, vistas, configuración)
- **[backend/API_DOCUMENTATION.md](backend/API_DOCUMENTATION.md)** - Referencia completa de endpoints de la API
- **[mobile/README.md](mobile/README.md)** - Documentación de la aplicación móvil (futuro)
- **[web/README.md](web/README.md)** - Documentación de la aplicación web Vue.js

---

## 🔧 Configuración Importante

### Variables de Entorno (Backend)

Crea un archivo `.env` en la carpeta `backend/` para configurar PostgreSQL y
el entorno. Sin `DATABASE_HOST`, el proyecto usa SQLite localmente:

```env
SECRET_KEY=una-clave-aleatoria-larga
DEBUG=False
ALLOWED_HOSTS=tu-api.azurewebsites.net
DATABASE_NAME=tutoudec_db
DATABASE_USER=usuario_postgres
DATABASE_PASSWORD=contraseña_segura
DATABASE_HOST=servidor-postgres
DATABASE_PORT=5432
CORS_ALLOWED_ORIGINS=https://tu-web.azurestaticapps.net
CSRF_TRUSTED_ORIGINS=https://tu-api.azurewebsites.net
```

No subas el archivo `.env` al repositorio. Para un despliegue, configura estas
variables en el servicio de nube, incluida la URL pública del frontend en
`CORS_ALLOWED_ORIGINS` y `VITE_API_URL` para la web y `EXPO_PUBLIC_API_URL`
para Android. Web y móvil consultan la misma API y, por tanto, la misma base
de datos.

Para cargar datos ficticios locales y ver el dashboard con información de
ejemplo, ejecuta `python manage.py seed_data` desde `backend/`. Las cuentas de
tutoría generadas por ese comando quedan desactivadas y sin contraseña.

### Dashboard

El dashboard de análisis está en `/dashboard`, requiere una cuenta
administradora y actualiza sus agregados cada 30 segundos. La API
`/api/dashboard/resumen/` devuelve conteos, distribución de estados, materias
más solicitadas y tendencia de tutorías de los últimos seis meses, sin exponer
datos personales.

### Funcionalidades del prototipo

1. Registro e inicio de sesión con JWT.
2. Recuperación y cambio de contraseña.
3. Búsqueda y consulta del catálogo de tutores.
4. Visualización del perfil y detalles del tutor.
5. Consulta del catálogo de materias.
6. Creación de tutorías desde la aplicación móvil.
7. Consulta y gestión de tutorías por estado.
8. Inicio y perfil adaptados al rol de estudiante o tutor.
9. Asistente conversacional desde la aplicación móvil.
10. Dashboard web de indicadores agregados para administradores.

El workflow de Azure despliega el backend cuando están configurados sus
secretos OIDC y la base de datos PostgreSQL. Los workflows manuales
`Deploy TutoUdec web` y `Build TutoUdec Android APK` despliegan la web a Azure
Static Web Apps y generan el APK de prueba en EAS, respectivamente.

Antes de ejecutarlos, crea Azure Static Web Apps y configura en GitHub el
secreto `AZURE_STATIC_WEB_APPS_API_TOKEN` y la variable `VITE_API_URL` con la
URL HTTPS de la API. Inicia sesión en Expo con
`npx eas-cli@25.2.0 login`, configura las credenciales Android de EAS una vez
y agrega el secreto `EXPO_TOKEN` y la variable `EXPO_PUBLIC_API_URL` al
repositorio. El proyecto EAS `@cristian.123/tutoudec` ya está creado y su ID
está incluido en la configuración móvil. El perfil `preview` produce un APK
compartible.

Hasta tener esos recursos y ajustes no se puede emitir un enlace web o de
descarga de APK verificado.

Para compilar la web y el APK, configura `VITE_API_URL` y
`EXPO_PUBLIC_API_URL` con la misma URL HTTPS de la API, por ejemplo
`https://tu-api.azurewebsites.net/api`.

### IP del Servidor (Móvil)

Si necesitas cambiar la IP del backend en la app móvil, edita:
```
mobile/src/config.js
```
Cambia el valor de `DEFAULT_LAN_HOST` por tu IP local.

---

## 📡 Endpoints Principales de la API

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/auth/login/` | Iniciar sesión |
| POST | `/api/auth/register/` | Registrarse |
| GET | `/api/tutores/` | Listar tutores |
| GET | `/api/materias/` | Listar materias |
| POST | `/api/tutorias/` | Crear tutoría |
| GET | `/api/tutorias/mis_tutorias/` | Mis tutorías |

Documentación interactiva disponible en: http://localhost:8000/api/schema/swagger-ui/

---

## 👥 Roles de Usuario

- **Estudiante**: Puede buscar tutores, agendar tutorías y dejar reseñas
- **Tutor**: Además de lo anterior, puede gestionar su disponibilidad
- **Administrador**: Acceso total a todas las funcionalidades

---

## 📝 Notas de Desarrollo

- El proyecto usa **JWT** para autenticación
- El backend corre en `0.0.0.0:8000` para permitir conexiones desde otros dispositivos
- La app móvil requiere **Expo SDK 54** y **React 19.1.0**
- Para producción, cambiar `DEBUG=False` y usar HTTPS
