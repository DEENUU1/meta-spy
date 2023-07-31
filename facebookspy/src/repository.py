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
from typing import Any, Type, List


def person_exists(facebook_id: str) -> Any:
    return session.query(Person).filter_by(facebook_id=facebook_id).first() is not None


def get_person(facebook_id: str) -> Type[Person] | None:
    return session.query(Person).filter_by(facebook_id=facebook_id).first()


def create_person(facebook_id: str, full_name=None) -> Person:
    url = f"https://www.facebook.com/{facebook_id}/"
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


def get_family_member_list(person_id: int) -> List[FamilyMember]:
    return session.query(FamilyMember).filter_by(person_id=person_id).all()


def get_family_member(family_member_id: int) -> FamilyMember:
    return session.query(FamilyMember).filter_by(id=family_member_id).first()


def create_friends(full_name: str, url: str, person_id: int) -> Friends:
    friends = Friends(full_name=full_name, url=url, person_id=person_id)
    session.add(friends)
    session.commit()
    return friends


def get_friends_list(person_id: int) -> List[Friends]:
    return session.query(Friends).filter_by(person_id=person_id).all()


def get_friend(friend_id: int) -> Friends:
    return session.query(Friends).filter_by(id=friend_id).first()


def create_image(path: str, person_id: int) -> Image:
    image = Image(path=path, person_id=person_id)
    session.add(image)
    session.commit()
    return image


def get_image_list(person_id: int) -> List[Image]:
    return session.query(Image).filter_by(person_id=person_id).all()


def get_image(image_id: int) -> Image:
    return session.query(Image).filter_by(id=image_id).first()


def create_places(name: str, date: str, person_id: int) -> Places:
    places = Places(name=name, date=date, person_id=person_id)
    session.add(places)
    session.commit()
    return places


def get_places_list() -> List[Places]:
    pass


def get_place() -> Places:
    pass


def create_work_and_education(name: str, person_id: int) -> WorkAndEducation:
    work_and_education = WorkAndEducation(name=name, person_id=person_id)
    session.add(work_and_education)
    session.commit()
    return work_and_education


def get_work_and_education_list() -> List[WorkAndEducation]:
    pass


def get_work_and_education() -> WorkAndEducation:
    pass


def create_recent_places(localization: str, date: str, person_id: int) -> RecentPlaces:
    recent_places = RecentPlaces(
        localization=localization, date=date, person_id=person_id
    )
    session.add(recent_places)
    session.commit()
    return recent_places


def get_recent_places_list() -> List[RecentPlaces]:
    pass


def get_recent_place() -> RecentPlaces:
    pass


def create_reels(url: str, person_id: int) -> Reels:
    reels = Reels(url=url, person_id=person_id)
    session.add(reels)
    session.commit()
    return reels


def get_reels_list() -> List[Reels]:
    pass


def get_reel() -> Reels:
    pass


def create_videos(url: str, person_id: int) -> Videos:
    videos = Videos(url=url, person_id=person_id)
    session.add(videos)
    session.commit()
    return videos


def get_videos_list() -> List[Videos]:
    pass


def get_video() -> Videos:
    pass


def create_reviews(company: str, review: str, person_id: int) -> Reviews:
    reviews = Reviews(company=company, review=review, person_id=person_id)
    session.add(reviews)
    session.commit()
    return reviews


def get_reviews_list() -> List[Reviews]:
    pass


def get_review() -> Reviews:
    pass
