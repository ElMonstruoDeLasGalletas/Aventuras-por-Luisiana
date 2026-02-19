# Preparación del proyecto

Este documento explica cómo preparar el entorno de desarrollo para trabajar en el proyecto paso a paso.

---

## Requisitos previos

Antes de empezar, asegúrate de tener instalado:

* **Python** (versión 3.10 o superior recomendada)
* **Docker** y **Docker Compose**
* **Git**

---

## Preparación del entorno

### 1 Acceder a la carpeta del proyecto

Desde la terminal, navega hasta la carpeta del proyecto:

```bash
cd ruta/del/proyecto
```

---

### 2 Crear el entorno virtual

Crea un entorno virtual llamado `.venv` (el resto de comandos asumen este nombre):

```bash
python -m venv .venv
```

---

### 3 Activar el entorno virtual

En **Windows (PowerShell)**:

```bash
.venv\Scripts\Activate.ps1
```

> Si PowerShell bloquea la activación, puede que necesites ejecutar:
>
> ```bash
> Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
> ```

---

### 4 Levantar los servicios con Docker

Arranca los contenedores definidos en `docker-compose.yml`:

```bash
docker compose up
```

Esto levantará el servidor y los servicios necesarios usando la configuración del proyecto.

---

### 5 Lanzar el servidor de desarrollo

Con el entorno virtual activado, ejecuta:

```bash
uvicorn app.main:app --reload
```

#### Si el comando anterior no funciona

Usa esta alternativa para asegurarte de que se utiliza el `uvicorn` del entorno virtual:

```bash
python -m uvicorn app.main:app --reload
```

---

## Comprobación

Si todo ha ido bien, el servidor debería estar disponible en:

```
http://127.0.0.1:8000
```

Y la documentación automática de la API en:

```
http://127.0.0.1:8000/docs
```
El acceso a la base de datos está definido en el docker-compose.yml
```
http:localhost:8080
```
  
  
  
---
# FEATURES
---

# Feature: Sistema de Preferencias de Usuario (Onboarding)

**Rama:** `gonzalo/onboarding-preferencias`  
**Fecha:** Enero 2026

---

## Resumen

Implementación del sistema de preferencias de usuario para el onboarding de la aplicación. Permite que los usuarios nuevos seleccionen sus intereses (tags) al crear cuenta, y se almacenan en base de datos para personalizar su experiencia.

---

## Archivos nuevos creados

### 1. `app/routers/preferences.py`
**Propósito:** Router con endpoints para gestionar las preferencias de usuario.

**Endpoints:**
- `POST /preferences/` - Crear o actualizar preferencias del usuario autenticado
- `GET /preferences/` - Obtener preferencias del usuario autenticado

**Dependencias:** Requiere autenticación (JWT token)

### Corrección de imports

**Problema inicial:** El router `preferences.py` importaba desde módulos incorrectos:
```python
# Imports incorrectos originales
from ..db import get_db  # get_db no existe en db.py
from ..security import get_current_user  # get_current_user no existe en security.py
```

**Solución:** Corregir imports para usar el módulo correcto `deps.py`:
```python
# Imports correctos
from ..deps import get_db, get_current_user
```

**Por qué:** 
- `get_db` es una función dependencia que está definida en `app/deps.py`
- `get_current_user` también está en `app/deps.py` para verificar autenticación
- Otros routers (`auth.py`, `pois.py`) ya importan correctamente de `deps.py`

---

## Archivos modificados

### 1. `app/models.py`
**Líneas añadidas:** Final del archivo (después de la clase `Review`)

**Cambio:** Nueva clase `UserPreferences`
```python
class UserPreferences(Base):
    __tablename__ = "user_preferences"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, unique=True, index=True)
    preferred_tags: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), on_update=lambda: datetime.now(timezone.utc), nullable=False)
```

**Por qué:**
- Almacenar las preferencias de tags de cada usuario
- Relación 1:1 con `User` (un usuario = unas preferencias)
- Campo `preferred_tags` es JSONB para guardar array de strings tipo `["nature", "kayak", "photo"]`
- Índice en `user_id` para búsquedas rápidas

---

### 2. `app/schemas.py`
**Líneas añadidas:** Final del archivo

**Cambios:** Dos nuevos schemas Pydantic
```python
class UserPreferencesCreate(BaseModel):
    preferred_tags: List[str] = Field(default=[])

class UserPreferencesOut(BaseModel):
    id: int
    user_id: int
    preferred_tags: List[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
```

**Por qué:**
- `UserPreferencesCreate` - Validar datos que envía el frontend (solo lista de tags)
- `UserPreferencesOut` - Serializar respuesta que devuelve el backend (todos los campos)
- Validación automática de tipos por Pydantic

---

### 3. `app/main.py`
**Líneas añadidas:** 
- Línea 6: Import del router
- Última línea: Registro del router

**Cambios:**
```python
# Import añadido
from .routers.preferences import router as preferences_router

# Registro añadido
app.include_router(preferences_router)
```

**Por qué:** Conectar el nuevo router de preferencias a la aplicación FastAPI para que los endpoints estén disponibles

---

## Tags disponibles

Los tags actuales en las rutas son:
- `nature`, `swamp`, `bayou`, `alligators`, `trail`
- `photo`, `viewpoint`, `sunset`
- `canoe`, `kayak`, `water`
- `family-friendly`, `wildlife`, `cypress`

---

## Base de datos

### Nueva Tabla: `user_preferences`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INTEGER | Primary key |
| user_id | INTEGER | Foreign key a `users.id` (UNIQUE) |
| preferred_tags | JSONB | Array de strings con tags seleccionados |
| created_at | TIMESTAMP | Fecha de creación |
| updated_at | TIMESTAMP | Fecha de última actualización |

**Tabla creada automáticamente** por SQLAlchemy al arrancar el servidor.

---

## Testing manual (Swagger UI)

URL: `http://localhost:8000/docs`

### Flujo de prueba:
1. `POST /auth/register` - Crear usuario
2. `POST /auth/login` - Obtener token
3. Botón "Authorize" - Introducir token
4. `POST /preferences/` - Guardar preferencias con body:
```json
{
  "preferred_tags": ["nature", "photo", "kayak"]
}
```
5. `GET /preferences/` - Verificar que se guardaron

---

## Pendiente

### Backend:
- [ ] Endpoint para obtener POIs filtrados por preferencias del usuario
- [ ] Lógica de recomendación basada en tags coincidentes

### Frontend (Android):
- [ ] Pantalla de onboarding con selector de categorías
- [ ] Integración con API `/preferences/`
- [ ] Mostrar onboarding solo en primera instalación + registro nuevo

---

## Notas Técnicas

- **Autenticación requerida:** Todos los endpoints de `/preferences/` requieren JWT token válido
- **Idempotencia:** `POST /preferences/` crea o actualiza (upsert) - no genera duplicados
- **Validación:** Pydantic valida que `preferred_tags` sea lista de strings
- **Performance:** Índice en `user_id` para consultas rápidas

# Feature: notificaciones geolocalizadas

**Rama:** `gonzalo/notificaciones-geolocalizadas`  
**Fecha:** Febrero 2026

---

## Resumen

Implementación del sistema de notificaciones geolocalizadas. El frontend Android envía las coordenadas del usuario al backend, que calcula si está dentro del radio de alguna geofence y envía una notificación push al dispositivo mediante Firebase Cloud Messaging (FCM).

---

## Archivos nuevos creados

### 1. `app/routers/notifications.py`

**Propósito:** Router con endpoints para gestionar tokens de dispositivo, comprobar ubicación y crear geofences.

**Endpoints:**
- `POST /notifications/device-token` — registra el token FCM del dispositivo Android del usuario autenticado
- `POST /notifications/check-location` — recibe coordenadas del usuario y devuelve las geofences que se han disparado, enviando la push correspondiente
- `POST /notifications/geofences` — crea una nueva geofence vinculada a un POI

**Dependencias:** requiere autenticación (JWT token)

### 2. `app/services/notification_service.py`

**Propósito:** Lógica de negocio para notificaciones.

**Funciones principales:**
- `haversine_distance` — calcula la distancia en metros entre dos coordenadas geográficas
- `register_device_token` — registra o actualiza el token FCM de un dispositivo
- `get_triggered_geofences` — detecta qué geofences están dentro del radio del usuario y envía las pushs
- `send_push_notification` — envía una notificación push real via FCM
- `log_notification` — registra en base de datos que se envió la notificación
- `create_geofence` — crea una nueva geofence en base de datos

### 3. `alembic/` (carpeta completa)

Alembic inicializado por primera vez en el proyecto para gestionar migraciones de base de datos.

---

## Archivos modificados

### 1. `app/models.py`

**Cambio:** tres nuevas clases al final del archivo.

- `DeviceToken` — almacena el token FCM de cada dispositivo del usuario. Campo `is_active` para desactivar tokens caducados sin borrarlos.
- `Geofence` — zona geográfica definida por coordenadas y radio en metros, vinculada obligatoriamente a un POI.
- `NotificationLog` — registro de notificaciones enviadas para evitar repetir la misma notificación más de una vez al día por usuario y geofence.

### 2. `app/schemas.py`

**Cambio:** nuevos schemas Pydantic al final del archivo.

- `DeviceTokenCreate` / `DeviceTokenOut` — para registrar y devolver tokens de dispositivo
- `LocationCheck` — coordenadas que envía el frontend
- `GeofenceCreate` / `GeofenceOut` — para crear y devolver geofences
- `TriggeredGeofencesOut` — lista de geofences disparadas que devuelve el endpoint de check-location

### 3. `app/main.py`

**Cambio:** import y registro del nuevo router.

```python
from .routers.notifications import router as notifications_router
app.include_router(notifications_router)
```

### 4. `.gitignore`

**Cambio:** añadida línea para excluir las credenciales de Firebase.

```
# Firebase
firebase-credentials.json
```

### 5. `requirements.txt`

**Cambio:** añadida dependencia `firebase-admin` para la integración con FCM.

---

## Base de datos

### nueva tabla: `device_tokens`

| campo | tipo | descripción |
|-------|------|-------------|
| id | integer | primary key |
| user_id | integer | foreign key a `users.id` |
| token | varchar(255) | token FCM del dispositivo (único) |
| is_active | boolean | indica si el token sigue activo |
| created_at | timestamp | fecha de creación |
| updated_at | timestamp | fecha de última actualización |

### nueva tabla: `geofences`

| campo | tipo | descripción |
|-------|------|-------------|
| id | integer | primary key |
| name | varchar(200) | nombre descriptivo de la zona |
| message | varchar(500) | mensaje que recibirá el usuario |
| lat | float | latitud del centro de la zona |
| lng | float | longitud del centro de la zona |
| radius_meters | float | radio en metros (por defecto 200) |
| poi_id | integer | foreign key a `pois.id` (obligatorio) |
| route_id | integer | foreign key a `routes.id` (opcional) |
| is_deleted | boolean | borrado suave |
| created_at | timestamp | fecha de creación |
| updated_at | timestamp | fecha de última actualización |

### nueva tabla: `notification_logs`

| campo | tipo | descripción |
|-------|------|-------------|
| id | integer | primary key |
| user_id | integer | foreign key a `users.id` |
| geofence_id | integer | foreign key a `geofences.id` |
| sent_at | timestamp | momento en que se envió la notificación |

**Migraciones generadas:**
- `05d15f3f402b_add_geofences_notification_tables.py`
- `a9af52b1ae97_geofence_poi_required.py`

---

## Firebase

El proyecto usa Firebase Cloud Messaging (FCM) para el envío de notificaciones push a Android.

**Configuración necesaria:**
- archivo `firebase-credentials.json` en la raíz del proyecto (no incluido en el repositorio)
- variable de entorno opcional `FIREBASE_CREDENTIALS_PATH` para indicar una ruta alternativa al archivo

El archivo de credenciales se obtiene desde la consola de Firebase en configuración del proyecto → cuentas de servicio → generar nueva clave privada. Debe compartirse con el equipo por un canal privado, nunca subirlo a GitHub.

---

## Lógica de proximidad

La detección de proximidad usa la **fórmula de Haversine**, que calcula la distancia real en metros entre dos puntos geográficos teniendo en cuenta la curvatura de la Tierra. Es más precisa que una simple diferencia de coordenadas.

**Anti-spam:** un usuario no recibe la misma notificación de la misma geofence más de una vez al día. El sistema comprueba el `notification_log` antes de enviar.

---

## Testing manual (Swagger UI)

URL: `http://localhost:8000/docs`

### Flujo de prueba:

1. `POST /auth/register` — crear usuario
2. `POST /auth/login` — obtener token
3. botón "Authorize" — introducir token
4. `POST /notifications/geofences` — crear geofence con body:
```json
{
  "name": "Entrada al Barrio Francés",
  "message": "¡Bienvenido al Barrio Francés!",
  "lat": 29.9584,
  "lng": -90.0644,
  "radius_meters": 200,
  "poi_id": 1
}
```
5. `POST /notifications/check-location` — comprobar ubicación con body:
```json
{
  "lat": 29.9584,
  "lng": -90.0644
}
```
6. verificar que la geofence aparece en `triggered`

---

## Pendiente

### backend:
- [ ] endpoint para listar geofences existentes
- [ ] endpoint para editar o desactivar una geofence
- [ ] restringir creación de geofences solo a usuarios con rol admin

### frontend (Android):
- [ ] integrar Firebase SDK en la app Android
- [ ] registrar el token FCM al iniciar sesión via `POST /notifications/device-token`
- [ ] enviar coordenadas periódicamente via `POST /notifications/check-location`

---

## notas técnicas

- **autenticación requerida:** todos los endpoints de `/notifications/` requieren JWT token válido
- **un poi por geofence:** cada geofence debe estar vinculada a un POI existente
- **tokens inactivos:** los tokens FCM caducados se marcan como `is_active=false` en lugar de borrarse, para mantener el historial
- **firebase inicialización:** Firebase se inicializa una sola vez al arrancar el servidor comprobando `firebase_admin._apps`