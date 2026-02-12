from sqlalchemy.orm import Session
from ..models import UserRole
from ..core.seed_data import USER_ROLES

def seed_user_roles(db: Session):
    for role_name in USER_ROLES:
        existing_role = (
            db.query(UserRole)
            .filter(UserRole.name == role_name)
            .first()
        )

        if not existing_role:
            db.add(UserRole(name=role_name))

    db.commit()