1️⃣ Define los roles

Primero hay que definir qué puede hacer cada tipo de usuario:

Rol	Qué puede hacer
Usuario normal	Consultar rutas, ver POIs, marcar favoritos, comentar quizás. Nada más.
Maquetador	Todo lo del usuario normal + crear o editar rutas y POIs (pero no borrar usuarios, ni tocar roles).
Admin	Todo. Crear, editar, borrar rutas, POIs, usuarios, roles… lo que le dé la gana.

💡 Consejo: empieza simple y ve ampliando permisos por “capas”.

2️⃣ Modela los roles en la base de datos

Lo más común:

class Role(Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)  # 'user', 'maquetador', 'admin'

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    hashed_password = Column(String)
    role_id = Column(Integer, ForeignKey("roles.id"))
    role = relationship("Role")


Así cada usuario tiene un rol asignado y puedes consultar sus permisos.

3️⃣ Protege rutas en FastAPI

Aquí entra el control de acceso. Por ejemplo:

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def get_current_user(token: str = Depends(oauth2_scheme)):
    # decodificar JWT y sacar user
    return user

def require_role(*roles: str):
    def role_checker(user = Depends(get_current_user)):
        if user.role.name not in roles:
            raise HTTPException(status_code=403, detail="No tienes permisos")
        return user
    return role_checker


Y luego en tus endpoints:

@app.post("/routes")
def create_route(route_data: RouteSchema, user = Depends(require_role("maquetador", "admin"))):
    # Solo maquetadores y admins pueden crear rutas
    ...


💡 Ventaja: muy flexible, puedes añadir nuevos roles y permisos sin reescribir todo.

4️⃣ Bonus: usar enums o bitmasks

Si quieres más precisión, en lugar de “roles rígidos”, cada permiso puede ser un flag:

class Permissions(enum.Flag):
    VIEW = 1
    EDIT = 2
    DELETE = 4


Así un admin tendría todos los flags, un usuario normal solo VIEW, etc.