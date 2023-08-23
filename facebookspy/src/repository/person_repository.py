from typing import Optional

from ..database import get_session
from ..models import (
    Person,
)


def person_exists(facebook_id: str) -> bool:
    """
    Check if Person object exists

    Args:
        facebook_id (str): Facebook ID

    Returns:
        bool: True if exists, False otherwise.
    """
    session = get_session()
    person = session.query(Person).filter_by(facebook_id=facebook_id).first()
    return person is not None


def get_person(facebook_id: str) -> Optional[Person]:
    """
    Get Person object

    Args:
        facebook_id (str): Facebook ID

    Returns:
        Person: Person object if exists, None otherwise.
    """
    session = get_session()
    person = session.query(Person).filter_by(facebook_id=facebook_id).first()
    return person


def create_person(
    facebook_id: str, full_name: str = None, phone_number: str = None, email: str = None
) -> Person:
    """Create Person object
    Args:
        facebook_id (str): Facebook ID
        full_name (str): Full name
        phone_number (str): Phone number
        email (str): Email address

    Returns:
        Person: Person object.
    """
    session = get_session()
    person = get_person(facebook_id)

    if person is None:
        url = f"https://www.facebook.com/{facebook_id}/"
        person = Person(full_name=full_name, url=url, facebook_id=facebook_id)
        session.add(person)
        session.commit()
    else:
        if full_name is not None and person.full_name is None:
            person.full_name = full_name
        if phone_number is not None and person.phone_number is None:
            person.phone_number = phone_number
        if email is not None and person.email is None:
            person.email = email
        session.commit()

    return person
