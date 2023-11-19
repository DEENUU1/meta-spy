from ..database import get_session
from ..models import InstagramImages


def image_exists(url: str) -> bool:
    session = get_session()
    image = session.query(InstagramImages).filter_by(url=url).first()
    return image is not None


def create_image(url: str) -> InstagramImages:
    session = get_session()
    image = InstagramImages(url=url)
    session.add(image)
    session.commit()
    return image
