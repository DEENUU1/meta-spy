from ..models import (
    FamilyMember,
)
from ..database import get_session
from typing import List, Optional


def family_member_exists(person_id: int, full_name: str) -> bool:
    session = get_session()
    family_member = (
        session.query(FamilyMember)
        .filter_by(person_id=person_id, full_name=full_name)
        .first()
    )
    return family_member is not None


def create_family_member(
    full_name: str, role: str, url: str, person_id: int
) -> FamilyMember:
    session = get_session()
    family_member = FamilyMember(
        full_name=full_name, role=role, url=url, person_id=person_id
    )
    session.add(family_member)
    session.commit()
    return family_member


def get_family_member_list(person_id: int) -> List[FamilyMember]:
    session = get_session()
    family_members = session.query(FamilyMember).filter_by(person_id=person_id).all()
    return family_members


def get_family_member(family_member_id: int) -> FamilyMember:
    session = get_session()
    family_member = session.query(FamilyMember).filter_by(id=family_member_id).first()
    return family_member
