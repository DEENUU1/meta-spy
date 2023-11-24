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


def set_as_downloaded(image: InstagramImages) -> None:
    image.downloaded = True
    get_session().commit()
    return


def get_all():
    session = get_session()
    return session.query(InstagramImages).all()


def get_not_downloaded():
    session = get_session()
    return session.query(InstagramImages).filter_by(downloaded=False).all()
