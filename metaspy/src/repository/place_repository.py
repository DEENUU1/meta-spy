from typing import List

from ..database import get_session
from ..models import (
    Places,
)


def places_exists(name: str, data: str, person_id: int) -> bool:
    """Check if Place object exists
    Args:
        name (str): Name
        data (str): Date
        person_id (int): Person ID
    Returns:
        bool: True if exists, False otherwise.
    """
    session = get_session()
    places = (
        session.query(Places)
        .filter_by(name=name, date=data, person_id=person_id)
        .first()
    )
    return places is not None


def create_places(name: str, date: str, person_id: int) -> Places:
    """Create Places object

    Args:
        name (str): Name
        date (str): Date
        person_id (int): Person ID
    Returns:
        Places: Places object
    """
    session = get_session()
    places = Places(name=name, date=date, person_id=person_id)
    session.add(places)
    session.commit()
    return places


def get_places_list(person_id: int) -> List[Places]:
    """Return a list of Places objects

    Args:
        person_id (int): Person ID
    Returns:
        List[Places]: List of Places objects
    """
    session = get_session()
    return session.query(Places).filter_by(person_id=person_id).all()


def get_place(place_id: int) -> Places:
    """Return Place object
    Args:
        place_id (int): Place ID
    Returns:
        Places: Place object
    """
    session = get_session()
    return session.query(Places).filter_by(id=place_id).first()
