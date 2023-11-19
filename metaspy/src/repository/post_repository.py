from typing import List, Dict

from ..database import get_session
from ..models import Posts, PostSource


def post_exists(url: str) -> bool:
    """Check if Post object already exists based on the URL"""
    session = get_session()
    posts = session.query(Posts).filter_by(url=url).first()
    return posts is not None


def get_posts(person_id: int) -> List[Posts]:
    """Return all posts for a person"""
    session = get_session()
    posts = session.query(Posts).filter_by(person_id=person_id).all()
    return posts


def get_post_by_url(url: str) -> Posts:
    """Return a post based on the URL"""
    session = get_session()
    post = session.query(Posts).filter_by(url=url).first()
    return post


def get_all_posts() -> List[Posts]:
    """Return all posts from database"""
    session = get_session()
    posts = session.query(Posts).all()
    return posts


def get_post(post_id: int) -> Posts:
    """Return a post based on the ID"""
    session = get_session()
    post = session.query(Posts).filter_by(id=post_id).first()
    return post


def create_post(
    url: str,
    person_id: int,
    content: str = None,
    number_of_likes: int = None,
    image_urls: Dict[int, str] = None,
    author: str = None,
    source: PostSource = None,
) -> Posts:
    """Create or update Post object"""
    session = get_session()

    existing_post = session.query(Posts).filter_by(url=url).first()

    if existing_post:
        if content is not None:
            existing_post.content = content
        if number_of_likes is not None:
            existing_post.number_of_likes = number_of_likes
        if source is not None:
            existing_post.source = source
        if image_urls is not None:
            existing_post.image_urls = image_urls
        if author is not None:
            existing_post.author = author
        session.commit()
        return existing_post
    else:
        post = Posts(
            url=url,
            person_id=person_id,
            content=content,
            number_of_likes=number_of_likes,
            image_urls=image_urls,
            source=source,
        )
        session.add(post)
        session.commit()
        return post


def mark_post_as_scraped(post_id: int) -> None:
    """Mark a post as scraped by updating the 'scraped' field to True"""
    session = get_session()
    post = session.query(Posts).filter_by(id=post_id).first()
    if post:
        post.scraped = True
        session.commit()


def get_posts_by_person(person_id: int) -> List[Posts]:
    """Return all posts for a person"""
    session = get_session()
    posts = session.query(Posts).filter_by(person_id=person_id).all()
    return posts
