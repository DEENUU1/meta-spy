from ..models import Person, Posts

from ..database import get_session
from typing import List, Optional


def post_exists(url: str) -> bool:
    """Check if Post object already exists based on the URL"""
    session = get_session()
    posts = session.query(Posts).filter_by(url=url).first()
    return posts is not None
