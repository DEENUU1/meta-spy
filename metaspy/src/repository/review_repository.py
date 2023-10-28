from ..database import get_session
from ..models import (
    Reviews,
)
from typing import List


def review_exists(company: str, review: str, person_id: int) -> bool:
    """Check if Review object exists

    Args:
        company (str): Company name
        review (str): Review
        person_id (int): Person ID

    Returns:
        bool: True if exists, False otherwise.
    """
    session = get_session()
    review = (
        session.query(Reviews)
        .filter_by(company=company, review=review, person_id=person_id)
        .first()
    )
    return review is not None


def create_reviews(company: str, review: str, person_id: int) -> Reviews:
    """Create a Reviews object

    Args:
        company (str): Company name
        review (str): Review
        person_id (int): Person ID

    Returns:
        Reviews: Reviews object
    """
    session = get_session()
    reviews = Reviews(company=company, review=review, person_id=person_id)
    session.add(reviews)
    session.commit()
    return reviews


def get_review(review_id: int) -> Reviews:
    """Return Reviews object

    Args:
        review_id (int): Review ID

    Returns:
        Reviews: Reviews object
    """
    session = get_session()
    return session.query(Reviews).filter_by(id=review_id).first()


def get_reviews_by_person(person_id: int) -> List[Reviews]:
    """Return Reviews object

    Args:
        person_id (int): Person ID

    Returns:
        List[Reviews]: Reviews object
    """
    session = get_session()
    return session.query(Reviews).filter_by(person_id=person_id).all()
