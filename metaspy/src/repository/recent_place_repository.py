from typing import List

from ..database import get_session
from ..models import (
    RecentPlaces,
)


def recent_places_exists(localization: str, date: str, person_id: int) -> bool:
    """
    Check if RecentPlaces object exists

    Args:
        localization (str): Localization
        date (str): Date
        person_id (int): Person ID

    Returns:
        bool: True if exists, False otherwise.
    """
    session = get_session()
    recent_places = (
        session.query(RecentPlaces)
        .filter_by(localization=localization, date=date, person_id=person_id)
        .first()
    )
    return recent_places is not None


def create_recent_places(localization: str, date: str, person_id: int) -> RecentPlaces:
    """Create RecentPlaces object

    Args:
        localization (str): Localization
        date (str): Date
        person_id (int): Person ID

    Returns:
        RecentPlaces: RecentPlaces object
    """
    session = get_session()
    recent_places = RecentPlaces(
        localization=localization, date=date, person_id=person_id
    )
    session.add(recent_places)
    session.commit()
    return recent_places


def get_recent_places_list(person_id: int) -> List[RecentPlaces]:
    """Return a list of RecentPlaces objects

    Args:
        person_id (int): Person ID

    Returns:
        List[RecentPlaces]: List of RecentPlaces objects
    """
    session = get_session()
    return session.query(RecentPlaces).filter_by(person_id=person_id).all()


def get_recent_place(recent_place_id: int) -> RecentPlaces:
    """Return RecentPlaces object

    Args:
        recent_place_id (int): RecentPlace ID

    Returns:
        RecentPlaces: RecentPlaces object
    """
    session = get_session()
    return session.query(RecentPlaces).filter_by(id=recent_place_id).first()
