from ..models import Ai
from ..database import get_session


def ai_exists(person_id: int) -> bool:
    """Check if ai object exists in database

    Args:
        person_id (int): PersonId

    Returns:
        bool: True if ai exists, False otherwise
    """
    session = get_session()
    return session.query(Ai).filter_by(person_id=person_id).first() is not None


def get_ai(person_id: int) -> Ai:
    """Get ai object from database

    Args:
        person_id (int): PersonId

    Returns:
        Ai: Ai object
    """
    session = get_session()
    return session.query(Ai).filter_by(person_id=person_id).first()


def create_or_update_ai(person_id: int, person_summary=None, person_opinion=None) -> Ai:
    """Create or update Ai object for specified Person object

    Args:
        person_id (int): PersonId
        person_summary (str): PersonSummary
        person_opinion (str): PersonOpinion
    """
    session = get_session()
    ai = session.query(Ai).filter_by(person_id=person_id).first()

    if ai:
        if person_summary is not None:
            ai.person_summary = person_summary
        if person_opinion is not None:
            ai.person_opinion = person_opinion
    else:
        ai = Ai(
            person_summary=person_summary,
            person_opinion=person_opinion,
            person_id=person_id,
        )

    session.add(ai)
    session.commit()
