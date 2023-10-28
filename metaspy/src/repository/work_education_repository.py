from typing import List

from ..database import get_session
from ..models import (
    WorkAndEducation,
)


def work_and_education_exists(name: str, person_id: int) -> bool:
    """Check if WorkAndEducation object exists

    Args:
        name (str): Name
        person_id (int): Person ID

    Returns:
        bool: True if exists, False otherwise.
    """
    session = get_session()
    work_and_education = (
        session.query(WorkAndEducation)
        .filter_by(name=name, person_id=person_id)
        .first()
    )
    return work_and_education is not None


def create_work_and_education(name: str, person_id: int) -> WorkAndEducation:
    """Create WorkAndEducation object

    Args:
        name (str): Name
        person_id (int): Person ID

    Returns:
        WorkAndEducation: WorkAndEducation object
    """
    session = get_session()
    work_and_education = WorkAndEducation(name=name, person_id=person_id)
    session.add(work_and_education)
    session.commit()
    return work_and_education


def get_work_and_education_list(person_id: int) -> List[WorkAndEducation]:
    """Return a list of WorkAndEducation objects

    Args:
        person_id (int): Person ID

    Returns:
        List[WorkAndEducation]: List of WorkAndEducation objects
    """
    session = get_session()
    return session.query(WorkAndEducation).filter_by(person_id=person_id).all()


def get_work_and_education(work_and_education_id: int) -> WorkAndEducation:
    """Return WorkAndEducation object

    Args:
        work_and_education_id (int): WorkAndEducation ID

    Returns:
        WorkAndEducation: WorkAndEducation object
    """
    session = get_session()
    return session.query(WorkAndEducation).filter_by(id=work_and_education_id).first()
