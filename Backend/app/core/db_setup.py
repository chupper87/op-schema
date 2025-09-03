from .settings import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from .logger import logger

import Backend.app.models.auth
import Backend.app.models.absence
import Backend.app.models.care_visit
import Backend.app.models.customer
import Backend.app.models.employee
import Backend.app.models.measure
import Backend.app.models.schedule


engine = create_engine(f"{settings.DB_URL}", echo=settings.DEBUG)


def init_db():
    from .base import Base

    try:
        Base.metadata.create_all(engine)
        logger.info("Database tables created! 👽")
    except Exception as e:
        print(f"❌ An error occurred initializing the database: {e}")


def get_db():
    try:
        with Session(engine, expire_on_commit=False) as session:
            yield session
    except Exception as e:
        logger.error(f"❌ Error getting database session: {e}")
        raise e


if __name__ == "__main__":
    init_db()
