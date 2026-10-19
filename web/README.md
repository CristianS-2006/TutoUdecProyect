# TutoUdec Web

Frontend web Vue 3 para el sistema de tutorías TutoUdec. Consume la misma API
Django y base de datos que la aplicación móvil.

## Inicio local

```powershell
npm ci
$env:VITE_API_URL = "http://127.0.0.1:8000/api"
npm run dev
```

Para producción, establece `VITE_API_URL` con el origen HTTPS de la API antes
de compilar:

```powershell
$env:VITE_API_URL = "https://tu-api.azurewebsites.net/api"
npm run build
```

El dashboard está disponible en `/dashboard` para cuentas administradoras y
refresca los indicadores cada 30 segundos.
