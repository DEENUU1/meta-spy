from ..models import (
    Likes,
)
from ..database import get_session


def like_exists(name: str, person_id: int) -> bool:
    """
    Check if Likes object exists

    Args:
        person_id (int): Person ID

    Returns:
        bool: True if exists, False otherwise.
    """
    session = get_session()
    person = session.query(Likes).filter_by(name=name, person_id=person_id).first()
    return person is not None


def create_like(person_id: int, name: str) -> Likes:
    """Create Likes object
    Args:
        person_id (str): Person ID
        name (str): Nmae
    Returns:
        Likes: Likes object.
    """
    session = get_session()
    like = Likes(person_id=person_id, name=name)
    session.add(like)
    session.commit()
    return like
