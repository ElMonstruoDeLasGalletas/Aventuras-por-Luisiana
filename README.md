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

(El acceso a la base de datos está definido en el docker-compose.yml)

Y la documentación automática de la API en:

```
http://127.0.0.1:8000/docs
```

---

