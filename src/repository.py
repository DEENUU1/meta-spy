from models import Person, FamilyMember, Friends, Image, Places, WorkAndEducation
from database import session


def person_exists(facebook_id):
    return session.query(Person).filter_by(facebook_id=facebook_id).first() is not None


def get_person(facebook_id):
    return session.query(Person).filter_by(facebook_id=facebook_id).first()


def create_person(url, facebook_id, full_name=None):
    person = Person(full_name=full_name, url=url, facebook_id=facebook_id)
    session.add(person)
    session.commit()
    return person


def create_family_member(full_name, role, url, person_id):
    family_member = FamilyMember(
        full_name=full_name, role=role, url=url, person_id=person_id
    )
    session.add(family_member)
    session.commit()
    return family_member


def create_friends(full_name, url, person_id):
    friends = Friends(full_name=full_name, url=url, person_id=person_id)
    session.add(friends)
    session.commit()
    return friends


def create_image(path, person_id):
    image = Image(path=path, person_id=person_id)
    session.add(image)
    session.commit()
    return image


def create_places(name, date, person_id):
    places = Places(name=name, date=date, person_id=person_id)
    session.add(places)
    session.commit()
    return places


def create_work_and_education(name, person_id):
    work_and_education = WorkAndEducation(name=name, person_id=person_id)
    session.add(work_and_education)
    session.commit()
    return work_and_education
