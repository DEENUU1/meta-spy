from ..database import get_session
from ..models import InstagramImages
from typing import List, Optional


def image_exists(url: str) -> bool:
    session = get_session()
    image = session.query(InstagramImages).filter_by(url=url).first()
    return image is not None


def create_image(url: str, account_id: int) -> InstagramImages:
    session = get_session()
    image = InstagramImages(url=url, account_id=account_id)
    session.add(image)
    session.commit()
    return image


def get_all() -> Optional[List[InstagramImages]]:
    session = get_session()
    return session.query(InstagramImages).all()
