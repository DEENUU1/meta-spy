from typing import List

from ..database import get_session
from ..models import (
    Image,
)


def image_exists(url: str, person_id: int) -> bool:
    """Check if Image object exists

    Args:
        url (str): Url
        person_id (int): Person ID

    Returns:
        bool: True if exists, False otherwise.
    """
    session = get_session()
    image = session.query(Image).filter_by(url=url, person_id=person_id).first()
    return image is not None


def create_image(url: str, person_id: int) -> Image:
    """Create Image object

    Args:
        person_id (int): Person ID
        url (str): Url

    Returns:
        Image: Image object
    """
    session = get_session()
    image = Image(url=url, person_id=person_id)
    session.add(image)
    session.commit()
    return image


def get_image_list(person_id: int) -> List[Image]:
    """Get list of Image objects

    Args:
        person_id (int): Person ID

    Returns:
        List[Image]: List of Image objects
    """
    session = get_session()
    return session.query(Image).filter_by(person_id=person_id).all()


def get_image(image_id: int) -> Image:
    """Get Image object

    Args:
        image_id (int): Image ID

    Returns:
        Image: Image object
    """
    session = get_session()
    return session.query(Image).filter_by(id=image_id).first()
