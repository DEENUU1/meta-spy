from ..database import get_session
from ..models import (
    Events,
)
from typing import List


def event_exists(name: str, person_id: int) -> bool:
    """
    Check if Events object exists

    Args:
        person_id (int): Person ID

    Returns:
        bool: True if exists, False otherwise.
    """
    session = get_session()
    person = session.query(Events).filter_by(name=name, person_id=person_id).first()
    return person is not None


def create_event(person_id: int, name: str, url: str = None) -> bool | Events:
    """
    Create or update a Events object.

    Args:
        person_id (int): Person ID
        name (str): Name
        url (str): URL

    Returns:
        Events: Created or updated Events object.
    """
    session = get_session()

    existing_event = event_exists(name, person_id)

    if existing_event:
        if url is not None:
            existing_event.url = url
        session.commit()
        return existing_event
    else:
        like = Events(person_id=person_id, name=name, url=url)
        session.add(like)
        session.commit()
        return like


def get_events_by_person(person_id: int) -> List[Events]:
    """
    Get Events object by person ID

    Args:
        person_id (int): Person ID

    Returns:
        Events: Events object
    """
    session = get_session()
    return session.query(Events).filter_by(person_id=person_id).all()
