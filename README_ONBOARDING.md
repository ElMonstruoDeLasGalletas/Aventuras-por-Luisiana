# Feature: Sistema de preferencias de usuario (Onboarding)
 
**Rama:** `gonzalo/onboarding-preferencias`  
**Fecha:** Enero 2026

---

## Resumen

Implementación del sistema de preferencias de usuario para el onboarding de la aplicación. Permite que los usuarios nuevos seleccionen sus intereses (tags) al crear cuenta. Los tags tienen IDs individuales y se almacenan en una relación muchos-a-muchos con los usuarios.

---

## Arquitectura

### Modelo de datos (Relación muchos a muchos)
```
User (1) ←→ (N) UserPreferredTag (N) ←→ (1) Tag

- Un usuario puede tener múltiples tags
- Un tag puede pertenecer a múltiples usuarios
- Tabla intermedia: user_preferred_tags
```

---

## Archivos nuevos creados

### 1. `app/routers/preferences.py`
**Propósito:** Router con endpoints para gestionar preferencias y catálogo de tags.

**Endpoints:**
- `GET /preferences/tags` - Listar todos los tags disponibles (público)
- `POST /preferences/tags` - Crear nuevo tag en el catálogo (requiere auth)
- `GET /preferences/` - Obtener preferencias del usuario autenticado
- `POST /preferences/tags` - Añadir tags a preferencias del usuario (por IDs)
- `DELETE /preferences/tags/{tag_id}` - Eliminar un tag específico por ID
- `DELETE /preferences/tags` - Eliminar múltiples tags (por IDs)

**Dependencias:** Todos los endpoints excepto `GET /preferences/tags` requieren autenticación JWT.

### Corrección de imports (Primera iteración)

**Problema inicial:** El router importaba desde módulos incorrectos:
```python
# Imports incorrectos originales
from ..db import get_db
from ..security import get_current_user
```

**Solución:** Corregir imports para usar `deps.py`:
```python
# Imports correctos
from ..deps import get_db, get_current_user
```

**Por qué:** Las funciones de dependencia están definidas en `app/deps.py`, igual que en otros routers del proyecto.

---

## Archivos modificados

### 1. `app/models.py`

**Cambios principales:** Refactorización completa del modelo de preferencias.

#### Nuevas tablas creadas:

**a) Tabla `tags` - Catálogo de tags disponibles**
```python
class Tag(Base):
    __tablename__ = "tags"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
```

**Por qué:**
- Catálogo centralizado de tags disponibles en la aplicación
- Cada tag tiene ID único para referencias en relaciones
- Índice en `name` para búsquedas rápidas
- Constraint UNIQUE en `name` evita duplicados

**b) Tabla `user_preferred_tags` - Relación Usuario ↔ Tags**
```python
class UserPreferredTag(Base):
    __tablename__ = "user_preferred_tags"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    tag_id: Mapped[int] = mapped_column(ForeignKey("tags.id"), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    
    __table_args__ = (
        UniqueConstraint("user_id", "tag_id", name="uq_user_tag"),
    )
```

**Por qué:**
- Implementa relación muchos-a-muchos entre User y Tag
- Un usuario puede tener múltiples tags
- Un tag puede pertenecer a múltiples usuarios
- Constraint UNIQUE evita duplicados (mismo tag dos veces para un usuario)
- Índices en foreign keys para consultas eficientes

**c) Tabla `user_preferences` - Mantenida para compatibilidad**
```python
class UserPreferences(Base):
    __tablename__ = "user_preferences"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, unique=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), on_update=lambda: datetime.now(timezone.utc), nullable=False)
```

**Por qué:**
- Mantiene compatibilidad durante migración
- Campo `preferred_tags` (JSONB) eliminado
- Se puede eliminar completamente en futuras versiones

---

### 2. `app/schemas.py`

**Cambios:** Schemas completamente rediseñados para trabajar con IDs.

#### Schemas Nuevos:
```python
# Tag individual (lectura)
class TagOut(BaseModel):
    id: int
    name: str

# Crear tag en catálogo
class TagCreate(BaseModel):
    name: str = Field(min_length=1, max_length=50)

# Añadir tags a preferencias
class UserPreferencesAdd(BaseModel):
    tag_ids: List[int] = Field(default=[])

# Eliminar tags de preferencias
class UserPreferencesRemove(BaseModel):
    tag_ids: List[int] = Field(default=[])

# Respuesta con preferencias del usuario
class UserPreferencesOut(BaseModel):
    tags: List[TagOut]
```

**Por qué:**
- Trabajo con IDs en lugar de strings
- Validación de tipos con Pydantic
- Operaciones granulares (añadir/eliminar por IDs)
- Respuesta rica con objetos Tag completos (ID + nombre)

#### Schemas eliminados:
```python
# Versión anterior (ya no se usa)
class UserPreferencesCreate(BaseModel):
    preferred_tags: List[str]  # Lista de strings sin IDs
```

---

### 3. `app/main.py`

**Cambios:** Registro de routers adicionales del equipo.
```python
# Imports añadidos por el equipo
from .routers.reviews import router as reviews_router
from .routers.routes import router as routes_router

# Registros añadidos
app.include_router(reviews_router)
app.include_router(routes_router)
```

**Por qué:** Fusión con cambios de `main` - el equipo añadió routers de reviews y routes.

---

### 4. `.gitignore`

**Cambios:** Ignorar archivos auxiliares.
```
# Archivos auxiliares de carga de datos
load_tags.py
*.csv
```

**Por qué:** Scripts de carga y CSVs de prueba no deben estar en control de versiones.

---

## Tags Disponibles

Los 14 tags actuales cargados en la base de datos:

| ID | Nombre |
|----|--------|
| 1 | swamp |
| 2 | bayou |
| 3 | alligators |
| 4 | trail |
| 5 | nature |
| 6 | photo |
| 7 | canoe |
| 8 | kayak |
| 9 | cypress |
| 10 | water |
| 11 | family-friendly |
| 12 | viewpoint |
| 13 | sunset |
| 14 | wildlife |

---

## Base de datos

### Tabla: `tags`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INTEGER | Primary key |
| name | VARCHAR(50) | Nombre del tag (UNIQUE, INDEX) |
| created_at | TIMESTAMP | Fecha de creación |

### Tabla: `user_preferred_tags`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INTEGER | Primary key |
| user_id | INTEGER | Foreign key a `users.id` (INDEX) |
| tag_id | INTEGER | Foreign key a `tags.id` (INDEX) |
| created_at | TIMESTAMP | Fecha de creación |

**Constraint:** UNIQUE(user_id, tag_id) - Evita duplicados

### Tabla: `user_preferences` (legacy)

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INTEGER | Primary key |
| user_id | INTEGER | Foreign key a `users.id` (UNIQUE) |
| created_at | TIMESTAMP | Fecha de creación |
| updated_at | TIMESTAMP | Fecha de actualización |

**Nota:** Esta tabla se mantiene por compatibilidad pero ya no almacena tags.

---

## Flujos de uso

### 1. Usuario nuevo - Onboarding
```
1. Frontend llama GET /preferences/tags
   → Obtiene lista de 14 tags con IDs
   
2. Usuario selecciona: "nature" (ID=5), "kayak" (ID=8), "photo" (ID=6)

3. Frontend llama POST /preferences/tags
   Body: {"tag_ids": [5, 8, 6]}
   → Se crean 3 registros en user_preferred_tags
```

### 2. Usuario modifica preferencias
```
1. Frontend llama GET /preferences/
   → Obtiene tags actuales del usuario
   
2. Usuario quiere añadir "sunset" (ID=13)
   Frontend llama POST /preferences/tags
   Body: {"tag_ids": [13]}
   
3. Usuario quiere eliminar "photo" (ID=6)
   Frontend llama DELETE /preferences/tags/6
```

### 3. Administrador añade nuevo tag
```
1. Admin llama POST /preferences/tags
   Body: {"name": "adventure"}
   → Se crea tag con ID=15
   
2. Ahora disponible para todos los usuarios
```

---

## Testing manual (Swagger UI)

URL: `http://localhost:8000/docs`

### Flujo completo de prueba:

**1. Ver tags disponibles (sin auth)**
```
GET /preferences/tags
→ Devuelve 14 tags con IDs
```

**2. Registrar usuario**
```
POST /auth/register
Body: {"email": "test@test.com", "name": "Test", "password": "123456"}
```

**3. Login**
```
POST /auth/login
Body: {"email": "test@test.com", "password": "123456"}
→ Copiar el access_token
```

**4. Autorizar en Swagger**
```
Botón "Authorize" → Pegar token
```

**5. Añadir preferencias**
```
POST /preferences/tags
Body: {"tag_ids": [5, 8, 6]}  // nature, kayak, photo
```

**6. Ver preferencias**
```
GET /preferences/
→ Devuelve los 3 tags con IDs y nombres
```

**7. Eliminar un tag**
```
DELETE /preferences/tags/6  // Eliminar "photo"
```

**8. Verificar cambio**
```
GET /preferences/
→ Solo devuelve 2 tags (nature, kayak)
```

---

## Pendiente

### Backend:
- [x] Endpoint para obtener POIs/Rutas filtrados por preferencias
- [x] Lógica de recomendación (scoring por tags coincidentes)
- [x] Implementado en `GET /routes/recommended`

### Frontend (Android):
- [ ] Pantalla de onboarding con grid de tags
- [ ] Integración con API (GET tags, POST preferencias)
- [ ] Mostrar onboarding solo en primera instalación + registro
- [ ] Pantalla de edición de preferencias en configuración

### Base de datos:
- [ ] Eliminar tabla `user_preferences` legacy una vez confirmado que todo funciona
- [ ] Considerar añadir campo `description` a tabla `tags` para UI

---

## Ventajas del nuevo modelo

**vs. Modelo anterior (JSONB array)**

| Aspecto | Anterior | Nuevo |
|---------|----------|-------|
| Identificación | Por string | Por ID único |
| Eliminación | Reemplazar array completo | DELETE por ID específico |
| Validación | Client-side | DB constraint (Foreign Key) |
| Búsquedas | JSON scan | Índices relacionales |
| Integridad | Strings arbitrarios | Solo tags existentes |
| Modificación | Sobrescribir todo | Operaciones granulares |

**Operaciones más eficientes:**
- Añadir 1 tag: 1 INSERT (antes: leer + modificar + escribir array)
- Eliminar 1 tag: 1 DELETE (antes: leer + filtrar + escribir array)
- Buscar usuarios con tag X: JOIN directo (antes: JSON contains)

---

## Notas técnicas

- **Autenticación:** Todos los endpoints excepto `GET /preferences/tags` requieren JWT
- **Sin duplicados:** POST añade solo tags nuevos (no duplica)
- **Validación:** Foreign keys garantizan que tag_id exista en tabla tags
- **Performance:** Índices en user_id y tag_id para JOINs rápidos
- **Escalabilidad:** Modelo normalizado permite millones de relaciones user-tag