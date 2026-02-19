import csv
from datetime import datetime
from app.db import SessionLocal, engine, Base
from app.models import User, POI, Review
from app.security import hash_password

# Crear las tablas si no existen
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# Limpiar datos existentes (opcional, cuidado en producción)
print("Limpiando datos existentes...")
db.query(Review).delete()
db.query(POI).delete()
db.query(User).delete()
db.commit()

# Cargar usuarios
print("Cargando usuarios...")
with open('users 1.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    for row in reader:
        user = User(
            id=int(row[0]),
            email=row[1],
            name=row[2],
            password_hash=row[3],
            created_at=datetime.fromisoformat(row[4].replace('+00', '+00:00'))
        )
        db.add(user)
db.commit()
print("Usuarios cargados")

# Cargar POIs
print("Cargando POIs...")
with open('pois 1.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    for row in reader:
        import json
        poi = POI(
            id=int(row[0]),
            name=row[1],
            lat=float(row[2]),
            lng=float(row[3]),
            description=row[4] if row[4] else None,
            tags=json.loads(row[5]),
            media=json.loads(row[6]),
            type=row[7] if row[7] else None,
            is_deleted=False,
            created_at=datetime.fromisoformat(row[9].replace('+00', '+00:00')),
            updated_at=datetime.fromisoformat(row[10].replace('+00', '+00:00'))
        )
        db.add(poi)
db.commit()
print("POIs cargados")

# Cargar reviews
print("Cargando reviews...")
with open('reviews.csv', 'r', encoding='utf-8-sig') as f:
    reader = csv.reader(f)
    for row in reader:
        review = Review(
            id=int(row[0]),
            user_id=int(row[1]),
            poi_id=int(row[2]),
            rating=int(row[3]),
            content=row[4] if row[4] else None,
            is_deleted=False,
            created_at=datetime.fromisoformat(row[6].replace('+00', '+00:00')),
            updated_at=datetime.fromisoformat(row[7].replace('+00', '+00:00'))
        )
        db.add(review)
db.commit()
print("Reviews cargadas")

db.close()
print("\nTodos los datos cargados correctamente!")