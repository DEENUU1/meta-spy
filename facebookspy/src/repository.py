from .models import (
    Person,
    FamilyMember,
    Friends,
    Image,
    Places,
    WorkAndEducation,
    RecentPlaces,
    Videos,
    Reels,
    Reviews,
)
from .database import session
from typing import Any, Type


def person_exists(facebook_id: str) -> Any:
    return session.query(Person).filter_by(facebook_id=facebook_id).first() is not None


def get_person(facebook_id: str) -> Type[Person] | None:
    return session.query(Person).filter_by(facebook_id=facebook_id).first()


def create_person(url: str, facebook_id: str, full_name=None) -> Person:
    person = Person(full_name=full_name, url=url, facebook_id=facebook_id)
    session.add(person)
    session.commit()
    return person


def create_family_member(
    full_name: str, role: str, url: str, person_id: int
) -> FamilyMember:
    family_member = FamilyMember(
        full_name=full_name, role=role, url=url, person_id=person_id
    )
    session.add(family_member)
    session.commit()
    return family_member


def create_friends(full_name: str, url: str, person_id: int) -> Friends:
    friends = Friends(full_name=full_name, url=url, person_id=person_id)
    session.add(friends)
    session.commit()
    return friends


def create_image(path: str, person_id: int) -> Image:
    image = Image(path=path, person_id=person_id)
    session.add(image)
    session.commit()
    return image


def create_places(name: str, date: str, person_id: int) -> Places:
    places = Places(name=name, date=date, person_id=person_id)
    session.add(places)
    session.commit()
    return places


def create_work_and_education(name: str, person_id: int) -> WorkAndEducation:
    work_and_education = WorkAndEducation(name=name, person_id=person_id)
    session.add(work_and_education)
    session.commit()
    return work_and_education


def create_recent_places(localization: str, date: str, person_id: int) -> RecentPlaces:
    recent_places = RecentPlaces(
        localization=localization, date=date, person_id=person_id
    )
    session.add(recent_places)
    session.commit()
    return recent_places


def create_reels(url: str, person_id: int) -> Reels:
    reels = Reels(url=url, person_id=person_id)
    session.add(reels)
    session.commit()
    return reels


def create_videos(url: str, person_id: int) -> Videos:
    videos = Videos(url=url, person_id=person_id)
    session.add(videos)
    session.commit()
    return videos


def create_reviews(company: str, review: str, person_id: int) -> Reviews:
    reviews = Reviews(company=company, review=review, person_id=person_id)
    session.add(reviews)
    session.commit()
    return reviews
