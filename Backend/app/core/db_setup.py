from base import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from settings import settings


engine = create_engine(f"{settings.DB_URL}", echo=True)


def create_db_and_tables():
    try:
        Base.metadata.create_all(engine)
        print("Database tables created! 👽")
    except Exception as e:
        print(f"An error occurred initializing the database: {e}")


def get_db():
    with Session(engine, expire_on_commit=False) as session:
        try:
            yield session
        except Exception as e:
            print(f"Database error: {e}")
            session.rollback
            raise


if __name__ == "__main__":
    create_db_and_tables()
