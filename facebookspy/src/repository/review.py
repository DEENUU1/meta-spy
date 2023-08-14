from ..models import (
    Reviews,
)
from ..database import get_session
from typing import List, Optional


def review_exists(company: str, review: str, person_id: int) -> bool:
    session = get_session()
    review = (
        session.query(Reviews)
        .filter_by(company=company, review=review, person_id=person_id)
        .first()
    )
    return review is not None


def create_reviews(company: str, review: str, person_id: int) -> Reviews:
    session = get_session()
    reviews = Reviews(company=company, review=review, person_id=person_id)
    session.add(reviews)
    session.commit()
    return reviews


def get_review(review_id: int) -> Reviews:
    session = get_session()
    return session.query(Reviews).filter_by(id=review_id).first()
