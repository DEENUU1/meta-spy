from ..models import Person, Posts, PostSource

from ..database import get_session
from typing import List, Optional


def post_exists(url: str) -> bool:
    """Check if Post object already exists based on the URL"""
    session = get_session()
    posts = session.query(Posts).filter_by(url=url).first()
    return posts is not None


def create_post(
    url: str,
    person_id: int,
    content: str,
    number_of_likes: int,
    number_of_shares: int,
    number_of_comments: int,
    source: PostSource,
) -> Posts:
    """Create Post object"""
    session = get_session()
    post = Posts(
        url=url,
        person_id=person_id,
        content=content,
        number_of_likes=number_of_likes,
        number_of_shares=number_of_shares,
        number_of_comments=number_of_comments,
        source=source,
    )
    session.add(post)
    session.commit()
    return post
