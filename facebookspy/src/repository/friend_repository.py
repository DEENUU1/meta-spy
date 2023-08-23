from typing import List

from ..database import get_session
from ..models import Friends, Person


def friend_exists(person_id: int, full_name: str, url: str) -> bool:
    """
    Check if Friend object exists

    Args:
        person_id (int): Person ID
        full_name (str): Full name
        url (str): URL

    Returns:
        bool: True if exists, False otherwise.
    """
    session = get_session()
    friend = (
        session.query(Friends)
        .filter_by(person_id=person_id, full_name=full_name, url=url)
        .first()
    )
    return friend is not None


def create_friends(full_name: str, url: str, person_id: int) -> Friends:
    """Create a Friend object
    Args:
        full_name (str): Full name
        url (str): URL
        person_id (int): Person ID
    Returns:
        Friends: Friend object
    """
    session = get_session()
    friends = Friends(full_name=full_name, url=url, person_id=person_id)
    session.add(friends)
    session.commit()
    return friends


def get_friends_list(person_id: int) -> List[Friends]:
    """Return a list of Friend objects

    Args:
        person_id (int): Person ID
    Returns:
        List[Friends]: List of Friend objects
    """
    session = get_session()
    friends = session.query(Friends).filter_by(person_id=person_id).all()
    return friends


def get_friend(friend_id: int) -> Friends:
    """Return a Friend object

    Args:
        friend_id (int): Friend ID
    Returns:
        Friends: Friend object
    """
    session = get_session()
    friend = session.query(Friends).filter_by(id=friend_id).first()
    return friend


def get_number_of_friends(person_id: int) -> int:
    """
    Get the number of Friends for a specific Person.

    Args:
        person_id (int): ID of the Person.

    Returns:
        int: Number of Friends associated with the Person.
    """
    session = get_session()
    person = session.query(Person).get(person_id)

    if person is None:
        return 0

    return len(person.friends)
