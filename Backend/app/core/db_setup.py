from .settings import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


engine = create_engine(f"{settings.DB_URL}", echo=True)


def init_db():
    from .base import Base

    try:
        Base.metadata.create_all(engine)
        print("Database tables created! 👽")
    except Exception as e:
        print(f"❌ An error occurred initializing the database: {e}")


def get_db():
    try:
        with Session(engine, expire_on_commit=False) as session:
            yield session
    except Exception as e:
        print(f"❌ Error getting database session: {e}")
        raise e


if __name__ == "__main__":
    init_db()
