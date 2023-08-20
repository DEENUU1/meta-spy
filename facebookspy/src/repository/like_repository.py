from ..models import (
    Likes,
)
from ..database import get_session


def like_exists(name: str) -> bool:
    """
    Check if Likes object exists

    Args:
        person_id (int): Person ID

    Returns:
        bool: True if exists, False otherwise.
    """
    session = get_session()
    person = session.query(Likes).filter_by(name=name).first()
    return person is not None


def create_like(person_id: int, name: str, url: str = None) -> Likes:
    """Create Likes object
    Args:
        person_id (str): Person ID
        name (str): Nmae
        url (str): Url of a like object
    Returns:
        Person: Person object.
    """
    session = get_session()
    like = like_exists(name)

    if like:
        if url is not None:
            like.url = url
    else:
        like = Likes(person_id=person_id, name=name, url=url)
        session.add(like)

    session.commit()
    return like
