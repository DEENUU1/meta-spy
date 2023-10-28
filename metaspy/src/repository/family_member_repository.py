from typing import List

from ..database import get_session
from ..models import (
    FamilyMember,
)


def family_member_exists(person_id: int, full_name: str) -> bool:
    """Check if FamilyMember object exists in database.

    Args:
        person_id (int): Person ID
        full_name (str): FamilyMember full name

    Returns:
        bool: True if FamilyMember object exists, False otherwise
    """
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
    """Create FamilyMember object in database.

    Args:
        full_name (str): FamilyMember full name
        role (str): FamilyMember role
        url (str): FamilyMember URL
        person_id (int): Person ID

    Returns:
        FamilyMember: FamilyMember object
    """
    session = get_session()
    family_member = FamilyMember(
        full_name=full_name, role=role, url=url, person_id=person_id
    )
    session.add(family_member)
    session.commit()
    return family_member


def get_family_member_list(person_id: int) -> List[FamilyMember]:
    """
    Return a list of FamilyMember objects

    Args:
        person_id (int): Person ID

    Returns:
        List[FamilyMember]: List of FamilyMember objects
    """
    session = get_session()
    family_members = session.query(FamilyMember).filter_by(person_id=person_id).all()
    return family_members


def get_family_member(family_member_id: int) -> FamilyMember:
    """Return a single FamilyMember object

    Args:
        family_member_id (int): FamilyMember ID

    Returns:
        FamilyMember: FamilyMember object
    """
    session = get_session()
    family_member = session.query(FamilyMember).filter_by(id=family_member_id).first()
    return family_member
