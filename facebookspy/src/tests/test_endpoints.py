from typing import List

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from ..server.backend.app import app
from ..database import get_session
from ..models import (
    Person,
    Videos,
    Reviews,
    Friends,
    Places,
    Image,
    FamilyMember,
    Notes,
)


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


def test_get_person_by_facebook_id_not_found(client):
    response = client.get("/person/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Person not found"}


def test_get_person_by_facebook_id(client, session):
    person = Person(
        full_name="John Doe", url="https://example.com/john-doe", facebook_id="abc"
    )
    session.add(person)
    session.commit()

    response = client.get("/person/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "full_name": "John Doe",
        "url": "https://example.com/john-doe",
        "facebook_id": "abc",
    }


def test_get_reviews_by_person_id_not_found(client):
    response = client.get("/person/review/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Reviews not found"}


def test_get_reviews_by_person_id(client, session):
    person = Person(
        full_name="John Doe", url="https://example.com/john-doe", facebook_id="abc"
    )
    review1 = Reviews(company="Company A", review="Review A", person=person)
    session.add(person)
    session.add(review1)
    session.commit()

    response = client.get("/person/review/1")
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "company": "Company A", "review": "Review A", "person_id": 1},
    ]


def test_get_videos_by_person_id_not_found(client):
    response = client.get("/person/video/1")
    assert response.status_code == 404
    assert response.json() == {"detail": "Videos not found"}


def test_get_videos_by_person_id(client, session):
    person = Person(
        full_name="John Doe", url="https://example.com/john-doe", facebook_id="abc"
    )
    video1 = Videos(url="https://www.youtube.com/watch?v=abc123", person=person)
    session.add(person)
    session.add(video1)
    session.commit()

    response = client.get("/person/video/1")
    assert response.status_code == 200
    assert response.json() == [
        {"id": 1, "url": "https://www.youtube.com/watch?v=abc123", "person_id": 1},
    ]


def test_get_places_by_person_id(client: TestClient, session: Session):
    person = Person(
        full_name="John Doe", url="https://example.com/john-doe", facebook_id="abc"
    )
    place = Places(
        name="Place A",
        date="Some date",
        person=person,
    )
    session.add(person)
    session.add(place)
    session.commit()

    response = client.get("/person/place/1")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "name": "Place A",
            "date": "Some date",
            "person_id": 1,
        }
    ]


def test_get_friends_by_person_id(client: TestClient, session: Session):
    person = Person(
        full_name="John Doe", url="https://example.com/john-doe", facebook_id="abc"
    )
    friend = Friends(
        full_name="John Toe", url="https://example.com/john-toe", person=person
    )
    session.add(person)
    session.add(friend)
    session.commit()

    response = client.get("/person/friend/1")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "full_name": "John Toe",
            "url": "https://example.com/john-toe",
            "person_id": 1,
        }
    ]


def test_get_images_by_person_id(client: TestClient, session: Session):
    person = Person(
        full_name="John Doe", url="https://example.com/john-doe", facebook_id="abc"
    )
    image = Image(path="src/images/johndoe/1.jpg", person=person)
    session.add(person)
    session.add(image)
    session.commit()

    response = client.get("/person/image/1")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "path": "src/images/johndoe/1.jpg",
            "person_id": 1,
        }
    ]


# def test_get_family_member_by_person_id(client: TestClient, session: Session):
#     person = Person(
#         full_name="John Doe", url="https://example.com/john-doe", facebook_id="abc"
#     )
#     family_member = FamilyMember(
#         full_name="John Toe",
#         role="Father",
#         url="https://example.com/john-toe",
#         person=person,
#     )
#     session.add(person)
#     session.add(family_member)
#     session.commit()
#
#     response = client.get("/person/family_member/1")
#     assert response.status_code == 200
#     assert response.json() == [
#         {
#             "id": 1,
#             "full_name": "John Toe",
#             "role": "Father",
#             "url": "https://example.com/john-toe",
#             "person_id": 1,
#         }
#     ]


def test_create_note_for_person(client: TestClient, session: Session):
    person = Person(
        full_name="John Doe", url="https://example.com/john-doe", facebook_id="abc"
    )
    session.add(person)
    session.commit()

    response = client.post(
        "/person/note/1",
        json={"content": "This is a note", "person_id": 1},
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "content": "This is a note",
        "person_id": 1,
    }


def test_update_note_for_person(client: TestClient, session: Session):
    person = Person(
        full_name="John Doe", url="https://example.com/john-doe", facebook_id="abc"
    )
    note = Notes(content="This is a note", person=person)
    session.add(person)
    session.add(note)
    session.commit()

    response = client.put(
        "/person/note/1",
        json={"content": "This is a note", "person_id": 1},
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "content": "This is a note",
        "person_id": 1,
    }
