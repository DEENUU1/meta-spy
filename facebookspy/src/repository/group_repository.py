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


def create_group(person_id: int, name: str, url: str = None) -> Groups:
    """
    Create or update a Groups object.

    Args:
        person_id (int): Person ID
        name (str): Name
        url (str): URL

    Returns:
        Groups: Created or updated Groups object.
    """
    session = get_session()

    existing_like = group_exists(name)

    if existing_like:
        if url is not None:
            existing_like.url = url
        session.commit()
        return existing_like
    else:
        like = Groups(person_id=person_id, name=name, url=url)
        session.add(like)
        session.commit()
        return like
