from ..models import (
    Reels,
)
from ..database import get_session
from typing import List, Optional


def reels_exists(url: str, person_id: int) -> bool:
    session = get_session()
    reels = session.query(Reels).filter_by(url=url, person_id=person_id).first()
    return reels is not None


def create_reels(url: str, person_id: int) -> Reels:
    session = get_session()
    reels = Reels(url=url, person_id=person_id)
    session.add(reels)
    session.commit()
    return reels


def get_reels(person_id: int) -> List[Reels]:
    session = get_session()
    return session.query(Reels).filter_by(person_id=person_id).all()


def get_new_reels(person_id: int) -> List[Reels]:
    """Return a list of Reels with bool field set to False"""
    session = get_session()
    return (
        session.query(Reels)
        .filter(person_id == person_id, Reels.downloaded == False)
        .all()
    )


def get_reel(reel_id: int) -> Reels:
    session = get_session()
    return session.query(Reels).filter_by(id=reel_id).first()
