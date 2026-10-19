# Mobile - TutoUdec

Aplicación móvil del sistema de tutorías construida con React Native y Expo.

## Requisitos

- Node.js 18+
- Expo CLI
- Expo Go (en el dispositivo móvil)
- Python 3.12-3.14 (para el backend)

## Dependencias Principales

```json
{
  "expo": "~54.0.0",
  "react": "19.0.0",
  "react-native": "0.81.0",
  "@react-navigation/native": "^7.0.0",
  "@react-navigation/stack": "^7.0.0",
  "@react-navigation/bottom-tabs": "^7.0.0",
  "react-native-safe-area-context": "4.12.0",
  "react-native-screens": "~4.4.0",
  "react-native-gesture-handler": "~2.20.0",
  "axios": "^1.6.0"
}
```

---

## Estructura de Archivos

```
mobile/
├── src/
│   ├── assets/              # Imágenes y recursos estáticos
│   ├── components/          # Componentes reutilizables
│   │   └── AppHeader.js     # Barra de navegación superior
│   ├── context/
│   │   └── AuthContext.js   # Manejo de autenticación
│   ├── navigation/
│   │   └── AppNavigator.js  # Configuración de navegación
│   ├── screens/
│   │   ├── auth/            # Pantallas de autenticación
│   │   │   ├── LoginScreen.js
│   │   │   └── RegisterScreen.js
│   │   ├── admin/           # Pantallas de administración
│   │   │   ├── UsuariosAdminScreen.js
│   │   │   └── MateriasAdminScreen.js
│   │   └── main/            # Pantallas principales
│   │       ├── HomeScreen.js
│   │       ├── TutoresScreen.js
│   │       ├── TutoriasScreen.js
│   │       └── DetalleTutorScreen.js
│   ├── services/
│   │   └── api.js           # Cliente Axios configurado
│   ├── theme/
│   │   └── colors.js        # Paleta de colores institucional
│   └── utils/
│       └── helpers.js       # Funciones auxiliares
├── App.js                   # Punto de entrada
├── app.json                 # Configuración de Expo
├── package.json
└── babel.config.js
```

---

## Pantallas Principales

### Autenticación
- **LoginScreen**: Inicio de sesión con usuario/email y contraseña
- **RegisterScreen**: Registro de nuevos usuarios

### Principal
- **HomeScreen**: Vista principal con materias y tutores destacados
- **TutoresScreen**: Lista de tutores con filtros avanzados
- **DetalleTutorScreen**: Perfil completo de un tutor
- **TutoriasScreen**: Agenda personal y gestión de disponibilidad
- **ProfileScreen**: Perfil del usuario

### Administración
- **UsuariosAdminScreen**: Gestión de usuarios (solo admin)
- **MateriasAdminScreen**: Gestión de materias (solo admin)

---

## Configuración de la API

La dirección del servidor backend se configura en:

```
src/config.js
```

Por defecto usa `DEFAULT_LAN_HOST = '192.168.1.7'`. Cambiar por la IP de tu PC.

El proyecto EAS `@cristian.123/tutoudec` ya está creado y vinculado en
`app.config.js`. Para crear un APK de prueba, inicia sesión en la CLI (`npx
eas-cli@25.2.0 login`), configura la URL pública de la API y configura las
credenciales Android de EAS una vez.
Para generarlo localmente desde PowerShell:

```powershell
$env:EXPO_PUBLIC_API_URL = "https://tu-api.azurewebsites.net/api"
npx eas-cli build --platform android --profile preview
```

La descarga del APK requiere una cuenta EAS y una API ya desplegada.

---

## Inicio Rápido

```powershell
# Instalar dependencias
npm install --legacy-peer-deps

# Iniciar en modo desarrollo
npx expo start

# Iniciar con LAN (para conectar desde celular)
npx expo start --lan

# Limpiar caché si hay problemas
npx expo start -c
```

---

## Colores Institucionales

```javascript
export const C = {
  primary: '#006D32',           // Verde institucional
  onPrimary: '#FFFFFF',
  primaryContainer: '#E8F5E9',
  secondary: '#FACC15',        // Amarillo
  onSecondary: '#000000',
  secondaryContainer: '#FEF9C3',
  surface: '#FBFCFA',
  onSurface: '#191C19',
  onSurfaceVariant: '#404943',
  outline: '#707971',
  outlineVariant: '#BFC9C1',
};
```

---

## Navegación

La aplicación usa:
- **Bottom Tabs**: Barra inferior con 4 pestañas (Home, Tutores, Agenda, Perfil)
- **Stack Navigator**: Para pantallas secundarias y modales
- **SafeAreaInsets**: Para respet ar los botones del sistema operativo

---

## Autenticación

El estado de autenticación se maneja con `AuthContext`:
- Token JWT almacenado en AsyncStorage
- Refresh token para renovar sesiones
- Roles: `estudiante`, `tutor`, `admin`

---

## Roles de Usuario

| Rol | Permisos |
|-----|----------|
| **Estudiante** | Buscar tutores, agendar tutorías, dejar reseñas |
| **Tutor** | Lo anterior + gestionar disponibilidad |
| **Admin** | Acceso total, gestión de usuarios y materias |
