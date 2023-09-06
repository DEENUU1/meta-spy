from ..database import get_session
from ..models import (
    Groups,
)
from typing import List


def group_exists(name: str, person_id: int) -> bool:
    """
    Check if Groups object exists

    Args:
        name (str): Group name
        person_id (int): Person ID

    Returns:
        bool: True if exists, False otherwise.
    """
    session = get_session()
    person = session.query(Groups).filter_by(name=name, person_id=person_id).first()
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

    existing_group = group_exists(name, person_id)

    if existing_group:
        if url is not None:
            existing_group.url = url
        session.commit()
        return existing_group
    else:
        group = Groups(person_id=person_id, name=name, url=url)
        session.add(group)
        session.commit()
        return group


def get_groups_by_person(person_id: int) -> List[Groups]:
    """
    Get Groups object by person ID

    Args:
        person_id (int): Person ID

    Returns:
        Groups: Groups object
    """
    session = get_session()
    return session.query(Groups).filter_by(person_id=person_id).all()
