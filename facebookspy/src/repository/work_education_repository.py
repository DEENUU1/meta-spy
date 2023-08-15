from ..models import (
    WorkAndEducation,
)
from ..database import get_session
from typing import List, Optional


def work_and_education_exists(name: str, person_id: int) -> bool:
    session = get_session()
    work_and_education = (
        session.query(WorkAndEducation)
        .filter_by(name=name, person_id=person_id)
        .first()
    )
    return work_and_education is not None


def create_work_and_education(name: str, person_id: int) -> WorkAndEducation:
    session = get_session()
    work_and_education = WorkAndEducation(name=name, person_id=person_id)
    session.add(work_and_education)
    session.commit()
    return work_and_education


def get_work_and_education_list(person_id: int) -> List[WorkAndEducation]:
    session = get_session()
    return session.query(WorkAndEducation).filter_by(person_id=person_id).all()


def get_work_and_education(work_and_education_id: int) -> WorkAndEducation:
    session = get_session()
    return session.query(WorkAndEducation).filter_by(id=work_and_education_id).first()
