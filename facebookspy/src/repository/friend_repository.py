from ..models import (
    Friends,
)
from ..database import get_session
from typing import List, Optional


def friend_exists(person_id: int, full_name: str, url: str) -> bool:
    session = get_session()
    friend = (
        session.query(Friends)
        .filter_by(person_id=person_id, full_name=full_name, url=url)
        .first()
    )
    return friend is not None


def create_friends(full_name: str, url: str, person_id: int) -> Friends:
    session = get_session()
    friends = Friends(full_name=full_name, url=url, person_id=person_id)
    session.add(friends)
    session.commit()
    return friends


def get_friends_list(person_id: int) -> List[Friends]:
    session = get_session()
    friends = session.query(Friends).filter_by(person_id=person_id).all()
    return friends


def get_friend(friend_id: int) -> Friends:
    session = get_session()
    friend = session.query(Friends).filter_by(id=friend_id).first()
    return friend
