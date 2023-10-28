import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from metaspy.src.models import (
    Base,
)
from ..database import get_session
from metaspy.src.server.app import app

engine = create_engine("sqlite:///database_test.db")
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)


@pytest.fixture
def session():
    connection = engine.connect()
    transaction = connection.begin()
    session = Session(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture
def client(session: Session):
    def override_get_session():
        return session

    app.dependency_overrides[get_session] = override_get_session
    client = TestClient(app)
    yield client
    app.dependency_overrides.pop(get_session)
