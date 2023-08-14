from ..models import (
    RecentPlaces,
)
from ..database import get_session
from typing import List, Optional


def recent_places_exists(localization: str, date: str, person_id: int) -> bool:
    session = get_session()
    recent_places = (
        session.query(RecentPlaces)
        .filter_by(localization=localization, date=date, person_id=person_id)
        .first()
    )
    return recent_places is not None


def create_recent_places(localization: str, date: str, person_id: int) -> RecentPlaces:
    session = get_session()
    recent_places = RecentPlaces(
        localization=localization, date=date, person_id=person_id
    )
    session.add(recent_places)
    session.commit()
    return recent_places


def get_recent_places_list(person_id: int) -> List[RecentPlaces]:
    session = get_session()
    return session.query(RecentPlaces).filter_by(person_id=person_id).all()


def get_recent_place(recent_place_id: int) -> RecentPlaces:
    session = get_session()
    return session.query(RecentPlaces).filter_by(id=recent_place_id).first()
