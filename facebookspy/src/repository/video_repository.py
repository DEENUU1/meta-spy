from typing import List

from ..database import get_session
from ..models import (
    Videos,
)


def video_exists(url: str, person_id: int) -> bool:
    """Check if Video object exists

    Args:
        url (str): Video URL
        person_id (int): Person ID

    Returns:
        bool: True if exists, False otherwise.
    """
    session = get_session()
    video = session.query(Videos).filter_by(url=url, person_id=person_id).first()
    return video is not None


def create_videos(url: str, person_id: int) -> Videos:
    """Create Videos object

    Args:
        url (str): Video URL
        person_id (int): Person ID

    Returns:
        Videos: Videos object
    """
    session = get_session()
    videos = Videos(url=url, person_id=person_id)
    session.add(videos)
    session.commit()
    return videos


def get_videos(person_id: int) -> List[Videos]:
    """Return all videos for specified person object"""
    session = get_session()
    return session.query(Videos).filter(Videos.person_id == person_id).all()


def update_videos_downloaded(video_id: int):
    """Update the 'downloaded' field for a single Videos object"""
    session = get_session()
    video = session.query(Videos).filter_by(id=video_id).first()
    if video:
        video.downloaded = True
        session.commit()


def get_new_videos(person_id: int) -> List[Videos]:
    """Return a list of videos with a bool field set to False"""
    session = get_session()
    return (
        session.query(Videos)
        .filter(Videos.person_id == person_id, Videos.downloaded == False)
        .all()
    )
