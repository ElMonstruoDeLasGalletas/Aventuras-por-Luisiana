from app.db import SessionLocal
from app.models import Tag

# Tags extraídos del CSV de POIs
tags_to_load = [
    "swamp", "bayou", "alligators", "trail", "nature", 
    "photo", "canoe", "kayak", "cypress", "water", 
    "family-friendly", "viewpoint", "sunset", "wildlife"
]

db = SessionLocal()

print("Cargando tags...")
for tag_name in tags_to_load:
    # Verificar si ya existe
    existing = db.query(Tag).filter(Tag.name == tag_name).first()
    if not existing:
        new_tag = Tag(name=tag_name)
        db.add(new_tag)
        print(f"  + {tag_name}")
    else:
        print(f"  - {tag_name} (ya existe)")

db.commit()
db.close()
print("\nTags cargados correctamente!")