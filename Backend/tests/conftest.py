import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Backend.app.core.base import Base
from Backend.app.core.settings import settings


@pytest.fixture
def db():
    test_db_url = settings.DATABASE_URL_TEST
    engine = create_engine(test_db_url)

    Base.metadata.create_all(engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    yield session

    session.close()
    Base.metadata.drop_all(engine)
