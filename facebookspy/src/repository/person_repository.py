from typing import Optional, List

from ..database import get_session
from ..models import (
    Person,
)
from sqlalchemy.orm import joinedload


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
    facebook_id: str,
) -> Person:
    """Create Person object
    Args:
        facebook_id (str): Facebook ID
        full_name (str): Full name

    Returns:
        Person: Person object.
    """
    session = get_session()
    person = get_person(facebook_id)

    if person is None:
        url = f"https://www.facebook.com/{facebook_id}/"
        person = Person(url=url, facebook_id=facebook_id)
        session.add(person)
        session.commit()

    return person


def update_number_of_friends(person_id: int, new_number_of_friends: int) -> bool:
    """
    Update the number_of_friends field of a Person object.

    Args:
        person_id (int): Person ID.
        new_number_of_friends (int): New value for number_of_friends.

    Returns:
        bool: True if the update was successful, False if the person does not exist.
    """
    session = get_session()
    person = session.query(Person).filter_by(id=person_id).first()

    if person is None:
        return False

    person.number_of_friends = new_number_of_friends
    session.commit()
    return True


def update_full_name(person_id: int, full_name: str) -> bool:
    session = get_session()
    person = session.query(Person).filter_by(id=person_id).first()

    if person is None:
        return False

    person.full_name = full_name
    session.commit()
    return True


def update_phone_number(person_id: int, phone_number: str) -> bool:
    session = get_session()
    person = session.query(Person).filter_by(id=person_id).first()

    if person is None:
        return False

    person.phone_number = phone_number
    session.commit()
    return True


def update_email(person_id: int, email: str) -> bool:
    session = get_session()
    person = session.query(Person).filter_by(id=person_id).first()

    if person is None:
        return False

    person.email = email
    session.commit()
    return True


def get_persons() -> List[Person]:
    """
    Return a list of Person objects
    """
    session = get_session()
    persons = (
        session.query(Person)
        .options(
            joinedload(Person.friends),
        )
        .all()
    )
    return persons
