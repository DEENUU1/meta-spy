from ..models import (
    Places,
)
from ..database import get_session
from typing import List, Optional


def places_exists(name: str, data: str, person_id: int) -> bool:
    session = get_session()
    places = (
        session.query(Places)
        .filter_by(name=name, date=data, person_id=person_id)
        .first()
    )
    return places is not None


def create_places(name: str, date: str, person_id: int) -> Places:
    session = get_session()
    places = Places(name=name, date=date, person_id=person_id)
    session.add(places)
    session.commit()
    return places


def get_places_list(person_id: int) -> List[Places]:
    session = get_session()
    return session.query(Places).filter_by(person_id=person_id).all()


def get_place(place_id: int) -> Places:
    session = get_session()
    return session.query(Places).filter_by(id=place_id).first()
