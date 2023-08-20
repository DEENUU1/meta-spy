from ..models import (
    Groups,
)
from ..database import get_session


def group_exists(name: str) -> bool:
    """
    Check if Groups object exists

    Args:
        person_id (int): Person ID

    Returns:
        bool: True if exists, False otherwise.
    """
    session = get_session()
    person = session.query(Groups).filter_by(name=name).first()
    return person is not None


def create_like(person_id: int, name: str, url: str = None) -> Groups:
    """Create Groups object
    Args:
        person_id (str): Person ID
        name (str): Name
        url (str): URL
    Returns:
        Groups: Groups object.
    """
    session = get_session()

    like_exist = like_exist(name)
    if like_exist:
        if url is not None:
            like_exist.url = url

        session.commit()
        return like_exist
    else:
        like = Groups(person_id=person_id, name=name, url=url)
        session.add(like)
        session.commit()
        return like
