from ..models import (
    Person,
)
from ..database import get_session
from typing import List, Optional


def person_exists(facebook_id: str) -> bool:
    session = get_session()
    person = session.query(Person).filter_by(facebook_id=facebook_id).first()
    return person is not None


def get_person(facebook_id: str) -> Optional[Person]:
    session = get_session()
    person = session.query(Person).filter_by(facebook_id=facebook_id).first()
    return person


def create_person(facebook_id: str, full_name=None) -> Person:
    session = get_session()
    person = get_person(facebook_id)

    if person is None:
        url = f"https://www.facebook.com/{facebook_id}/"
        person = Person(full_name=full_name, url=url, facebook_id=facebook_id)
        session.add(person)
        session.commit()
    elif full_name is not None and person.full_name is None:
        person.full_name = full_name
        session.commit()

    return person
