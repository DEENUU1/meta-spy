from ..database import get_session
from ..models import InstagramComments


def create_comment(
    content: str,
    image_id: int,
) -> InstagramComments:
    session = get_session()
    comment = InstagramComments(
        content=content,
        image_id=image_id,
    )
    session.add(comment)
    session.commit()
    return comment
