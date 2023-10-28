from metaspy.src.models import (
    Person,
    FamilyMember,
    Friends,
    Image,
    Places,
    WorkAndEducation,
    RecentPlaces,
    Reels,
    Videos,
    Reviews,
    Notes,
    Posts,
    PostSource,
    Likes,
    Groups,
    Events,
)
from .conftest import session


def test_create_person_model_successfully_create_object(session):
    person = Person(
        full_name="John Doe",
        url="https://example.com/john_doe",
        facebook_id="johndoe123",
    )
    session.add(person)
    session.commit()

    assert person.id is not None
    assert person.full_name == "John Doe"
    assert person.url == "https://example.com/john_doe"
    assert person.facebook_id == "johndoe123"


def test_create_family_member_model_successfully_create_object(session):
    person = Person(full_name="Jane Doe", url="https://example.com/jane_doe")
    family_member = FamilyMember(full_name="Father", person=person)
    session.add(family_member)
    session.commit()

    assert family_member.id is not None
    assert family_member.full_name == "Father"
    assert family_member.person == person


def test_create_friend_model_successfully_create_object(session):
    person = Person(full_name="Alice Smith", url="https://example.com/alice_smith")
    friend = Friends(full_name="Bob Johnson", person=person)
    session.add(friend)
    session.commit()

    assert friend.id is not None
    assert friend.full_name == "Bob Johnson"
    assert friend.person == person


def test_create_image_model_successfully_create_object(session):
    person = Person(full_name="John Smith", url="https://example.com/john_smith")
    image = Image(path="/path/to/image.jpg", person=person)
    session.add(image)
    session.commit()

    assert image.id is not None
    assert image.path == "/path/to/image.jpg"
    assert image.person == person


def test_create_place_model_successfully_create_object(session):
    person = Person(full_name="Alice Johnson", url="https://example.com/alice_johnson")
    place = Places(name="Home", date="2023-07-27", person=person)
    session.add(place)
    session.commit()

    assert place.id is not None
    assert place.name == "Home"
    assert place.date == "2023-07-27"
    assert place.person == person


def test_create_work_and_education_model_successfully_create_object(session):
    person = Person(full_name="Bob Brown", url="https://example.com/bob_brown")
    work_education = WorkAndEducation(name="Software Engineer", person=person)
    session.add(work_education)
    session.commit()

    assert work_education.id is not None
    assert work_education.name == "Software Engineer"
    assert work_education.person == person


def test_person_relationships_model_successfully_create_object(session):
    person = Person(full_name="Test Person", url="https://example.com/test_person")

    family_member = FamilyMember(full_name="Mother", person=person)
    friend = Friends(full_name="Friend 1", person=person)
    image = Image(path="/path/to/image.jpg", person=person)
    place = Places(name="Workplace", date="2023-07-27", person=person)
    work_education = WorkAndEducation(name="Teacher", person=person)

    session.add_all([family_member, friend, image, place, work_education])
    session.commit()

    assert person.friends == [friend]
    assert person.images == [image]


def test_relationship_backrefs_model_successfully_create_object(session):
    person = Person(
        full_name="Backref Person", url="https://example.com/backref_person"
    )
    friend1 = Friends(full_name="Backref Friend 1", person=person)
    friend2 = Friends(full_name="Backref Friend 2", person=person)

    session.add_all([friend1, friend2])
    session.commit()

    assert friend1.person == person
    assert friend2.person == person
    assert person.friends == [friend1, friend2]


def test_recent_places_model_successfully_create_object(session):
    person = Person(
        full_name="Recent Place Person", url="https://example.com/recent_place_person"
    )
    recent_place = RecentPlaces(localization="Home", date="2023-07-27", person=person)
    session.add(recent_place)
    session.commit()

    assert recent_place.id is not None
    assert recent_place.localization == "Home"
    assert recent_place.date == "2023-07-27"
    assert recent_place.person == person


def test_reels_model_successfully_create_object(session):
    person = Person(full_name="Reels Person", url="https://example.com/reels_person")
    reels = Reels(url="https://example.com/reels/1", person=person)
    session.add(reels)
    session.commit()

    assert reels.id is not None
    assert reels.url == "https://example.com/reels/1"
    assert reels.person == person


def test_videos_model_successfully_create_object(session):
    person = Person(full_name="Videos Person", url="https://example.com/videos_person")
    videos = Videos(url="https://example.com/videos/1", person=person)
    session.add(videos)
    session.commit()

    assert videos.id is not None
    assert videos.url == "https://example.com/videos/1"
    assert videos.person == person


def test_reviews_model_successfully_create_object(session):
    person = Person(
        full_name="Reviews Person", url="https://example.com/reviews_person"
    )
    reviews = Reviews(
        company="Test",
        person=person,
        review="Test review",
    )
    session.add(reviews)
    session.commit()

    assert reviews.id is not None
    assert reviews.company == "Test"
    assert reviews.person == person
    assert reviews.review == "Test review"


def test_note_model_successfully_create_object(session):
    person = Person(full_name="Note Person", url="https://example.com/note_person")
    note = Notes(content="Test note", person=person)
    session.add(note)
    session.commit()

    assert note.id is not None
    assert note.content == "Test note"
    assert note.person == person


def test_post_model_successfully_create_object(session):
    person = Person(full_name="Note Person", url="https://example.com/note_person")
    post = Posts(
        url="https://example.com/post/1",
        content="Test post",
        person=person,
        number_of_likes=2,
    )
    session.add(post)
    session.commit()

    assert post.id is not None
    assert post.url == "https://example.com/post/1"
    assert post.content == "Test post"
    assert post.person == person
    assert post.number_of_likes == 2
    assert post.source == PostSource.ACCOUNT


def test_likes_model_successfully_create_object(session):
    person_object = Person(full_name="XYZ", url="https://example.com/xyz")
    like = Likes(
        name="Like 1",
        person=person_object,
    )
    session.add(like)
    session.commit()

    assert like.id is not None
    assert like.name == "Like 1"
    assert like.person == person_object


def test_groups_model_successfully_create_object(session):
    person_object = Person(full_name="XYZ", url="https://example.com/xyz")
    group = Groups(
        name="Group 1", person=person_object, url="https://example.com/group/1"
    )
    session.add(group)
    session.commit()

    assert group.id is not None
    assert group.name == "Group 1"
    assert group.url == "https://example.com/group/1"
    assert group.person == person_object


def test_events_model_successfully_create_object(session):
    person_object = Person(full_name="XYZ", url="https://example.com/xyz")
    event = Events(
        name="Event 1", person=person_object, url="https://example.com/event/1"
    )
    session.add(event)
    session.commit()

    assert event.id is not None
    assert event.name == "Event 1"
    assert event.person == person_object
