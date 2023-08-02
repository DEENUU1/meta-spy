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
from .database import get_session
from typing import List, Optional


def person_exists(facebook_id: str) -> bool:
    session = get_session()
    person = session.query(Person).filter_by(facebook_id=facebook_id).first()
    return person is not None


def get_person(facebook_id: str) -> Optional[Person]:
    session = get_session()
    person = session.query(Person).filter_by(facebook_id=facebook_id).first()
    return person


def create_person(facebook_id: str, full_name=None) -> Person:
    session = get_session()
    url = f"https://www.facebook.com/{facebook_id}/"
    person = Person(full_name=full_name, url=url, facebook_id=facebook_id)
    session.add(person)
    session.commit()
    return person


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


def create_friends(full_name: str, url: str, person_id: int) -> Friends:
    session = get_session()
    friends = Friends(full_name=full_name, url=url, person_id=person_id)
    session.add(friends)
    session.commit()
    return friends


def get_friends_list(person_id: int) -> List[Friends]:
    session = get_session()
    friends = session.query(Friends).filter_by(person_id=person_id).all()
    return friends


def get_friend(friend_id: int) -> Friends:
    session = get_session()
    friend = session.query(Friends).filter_by(id=friend_id).first()
    return friend


def create_image(path: str, person_id: int) -> Image:
    session = get_session()
    image = Image(path=path, person_id=person_id)
    session.add(image)
    session.commit()
    return image


def get_image_list(person_id: int) -> List[Image]:
    session = get_session()
    return session.query(Image).filter_by(person_id=person_id).all()


def get_image(image_id: int) -> Image:
    session = get_session()
    return session.query(Image).filter_by(id=image_id).first()


def create_places(name: str, date: str, person_id: int) -> Places:
    session = get_session()
    places = Places(name=name, date=date, person_id=person_id)
    session.add(places)
    session.commit()
    return places


def get_places_list(person_id: int) -> List[Places]:
    session = get_session()
    return session.query(Places).filter_by(person_id=person_id).all()


def get_place(place_id: int) -> Places:
    session = get_session()
    return session.query(Places).filter_by(id=place_id).first()


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


def create_recent_places(localization: str, date: str, person_id: int) -> RecentPlaces:
    session = get_session()
    recent_places = RecentPlaces(
        localization=localization, date=date, person_id=person_id
    )
    session.add(recent_places)
    session.commit()
    return recent_places


def get_recent_places_list(person_id: int) -> List[RecentPlaces]:
    session = get_session()
    return session.query(RecentPlaces).filter_by(person_id=person_id).all()


def get_recent_place(recent_place_id: int) -> RecentPlaces:
    session = get_session()
    return session.query(RecentPlaces).filter_by(id=recent_place_id).first()


def create_reels(url: str, person_id: int) -> Reels:
    session = get_session()
    reels = Reels(url=url, person_id=person_id)
    session.add(reels)
    session.commit()
    return reels


def get_reels_list(person_id: int) -> List[Reels]:
    session = get_session()
    return session.query(Reels).filter_by(person_id=person_id).all()


def get_reel(reel_id: int) -> Reels:
    session = get_session()
    return session.query(Reels).filter_by(id=reel_id).first()


def create_videos(url: str, person_id: int) -> Videos:
    session = get_session()
    videos = Videos(url=url, person_id=person_id)
    session.add(videos)
    session.commit()
    return videos


def create_reviews(company: str, review: str, person_id: int) -> Reviews:
    session = get_session()
    reviews = Reviews(company=company, review=review, person_id=person_id)
    session.add(reviews)
    session.commit()
    return reviews


def get_review(review_id: int) -> Reviews:
    session = get_session()
    return session.query(Reviews).filter_by(id=review_id).first()
