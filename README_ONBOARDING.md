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