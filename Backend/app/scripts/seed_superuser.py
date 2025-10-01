import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from Backend.app.core.db_setup import SessionLocal  # noqa: E402
from Backend.app.models.auth import User  # noqa: E402
from Backend.app.core.security import get_password_hash  # noqa: E402


def create_initial_superuser():
    db = SessionLocal()

    # Check if superuser already exists
    existing = db.query(User).filter(User.is_superuser).first()
    if existing:
        print(f"Superuser already exists: {existing.username}")
        db.close()
        return

    user = User(
        email="admin@example.com",
        username="admin",
        hashed_password=get_password_hash("admin"),
        is_active=True,
        is_superuser=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    print(f"Superuser created: {user.username}")
    print("Password: admin")
    db.close()
    return user


if __name__ == "__main__":
    create_initial_superuser()
