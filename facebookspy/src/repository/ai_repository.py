from ..models import Ai


def ai_exists(person_id: int) -> bool:
    """Check if ai object exists in database

    Args:
        person_id (int): PersonId

    Returns:
        bool: True if ai exists, False otherwise
    """
    return Ai.query.filter_by(person_id=person_id).first() is not None
