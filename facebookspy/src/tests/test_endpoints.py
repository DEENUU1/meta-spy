import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from ..server.backend.app import app
from ..database import get_session
from ..models import Person


@pytest.fixture
def client(session: Session):
    def override_get_session():
        return session

    app.dependency_overrides[get_session] = override_get_session
    client = TestClient(app)
    yield client
    app.dependency_overrides.pop(get_session)


def test_get_people_list_empty(client):
    response = client.get("/person/")
    assert response.status_code == 404
    assert response.json() == {"detail": "People not found"}


def test_get_people_list(client, session):
    person1 = Person(
        full_name="John Doe", url="https://example.com/john-doe", facebook_id="abc"
    )
    person2 = Person(
        full_name="Jane Smith", url="https://example.com/jane-smith", facebook_id="abc1"
    )
    session.add(person1)
    session.add(person2)
    session.commit()

    response = client.get("/person/")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "full_name": "John Doe",
            "url": "https://example.com/john-doe",
            "facebook_id": "abc",
        },
        {
            "id": 2,
            "full_name": "Jane Smith",
            "url": "https://example.com/jane-smith",
            "facebook_id": "abc1",
        },
    ]
