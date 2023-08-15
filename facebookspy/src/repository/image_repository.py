from ..models import (
    Image,
)
from ..database import get_session
from typing import List, Optional


def image_exists(path: str, person_id: int) -> bool:
    session = get_session()
    image = session.query(Image).filter_by(path=path, person_id=person_id).first()
    return image is not None


def create_image(path: str, person_id: int) -> Image:
    session = get_session()
    image = Image(path=path, person_id=person_id)
    session.add(image)
    session.commit()
    return image


def get_image_list(person_id: int) -> List[Image]:
    session = get_session()
    return session.query(Image).filter_by(person_id=person_id).all()


def get_image(image_id: int) -> Image:
    session = get_session()
    return session.query(Image).filter_by(id=image_id).first()
