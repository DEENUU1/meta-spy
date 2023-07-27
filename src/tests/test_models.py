# import pytest
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# from src.models import (
#     Person,
#     FamilyMember,
#     Friends,
#     Image,
#     Places,
#     WorkAndEducation,
#     Base,
# )
#
# engine = create_engine("sqlite:///:memory:")
# Session = sessionmaker(bind=engine)
# Base.metadata.create_all(bind=engine)
#
#
# @pytest.fixture
# def session():
#     """Create a new SQLAlchemy session for each test."""
#     session = Session()
#     yield session
#     session.close()
#
#
# def test_create_person_model_successfully_create_object(session):
#     person = Person(
#         full_name="John Doe",
#         url="https://example.com/john_doe",
#         facebook_id="johndoe123",
#     )
#     session.add(person)
#     session.commit()
#
#     assert person.id is not None
#     assert person.full_name == "John Doe"
#     assert person.url == "https://example.com/john_doe"
#     assert person.facebook_id == "johndoe123"
#
#
# def test_create_family_member_model_successfully_create_object(session):
#     person = Person(full_name="Jane Doe", url="https://example.com/jane_doe")
#     family_member = FamilyMember(full_name="Father", person=person)
#     session.add(family_member)
#     session.commit()
#
#     assert family_member.id is not None
#     assert family_member.full_name == "Father"
#     assert family_member.person == person
#
#
# def test_create_friend_model_successfully_create_object(session):
#     person = Person(full_name="Alice Smith", url="https://example.com/alice_smith")
#     friend = Friends(full_name="Bob Johnson", person=person)
#     session.add(friend)
#     session.commit()
#
#     assert friend.id is not None
#     assert friend.full_name == "Bob Johnson"
#     assert friend.person == person
#
#
# def test_create_image_model_successfully_create_object(session):
#     person = Person(full_name="John Smith", url="https://example.com/john_smith")
#     image = Image(path="/path/to/image.jpg", person=person)
#     session.add(image)
#     session.commit()
#
#     assert image.id is not None
#     assert image.path == "/path/to/image.jpg"
#     assert image.person == person
#
#
# def test_create_place_model_successfully_create_object(session):
#     person = Person(full_name="Alice Johnson", url="https://example.com/alice_johnson")
#     place = Places(name="Home", date="2023-07-27", person=person)
#     session.add(place)
#     session.commit()
#
#     assert place.id is not None
#     assert place.name == "Home"
#     assert place.date == "2023-07-27"
#     assert place.person == person
#
#
# def test_create_work_and_education_model_successfully_create_object(session):
#     person = Person(full_name="Bob Brown", url="https://example.com/bob_brown")
#     work_education = WorkAndEducation(name="Software Engineer", person=person)
#     session.add(work_education)
#     session.commit()
#
#     assert work_education.id is not None
#     assert work_education.name == "Software Engineer"
#     assert work_education.person == person
#
#
# def test_person_relationships_model_successfully_create_object(session):
#     person = Person(full_name="Test Person", url="https://example.com/test_person")
#
#     family_member = FamilyMember(full_name="Mother", person=person)
#     friend = Friends(full_name="Friend 1", person=person)
#     image = Image(path="/path/to/image.jpg", person=person)
#     place = Places(name="Workplace", date="2023-07-27", person=person)
#     work_education = WorkAndEducation(name="Teacher", person=person)
#
#     session.add_all([family_member, friend, image, place, work_education])
#     session.commit()
#
#     assert person.family_member == family_member
#     assert person.friends == [friend]
#     assert person.images == [image]
#     assert person.places == place
#     assert person.work_and_education == work_education
#
#
# def test_relationship_backrefs_model_successfully_create_object(session):
#     person = Person(
#         full_name="Backref Person", url="https://example.com/backref_person"
#     )
#     friend1 = Friends(full_name="Backref Friend 1", person=person)
#     friend2 = Friends(full_name="Backref Friend 2", person=person)
#
#     session.add_all([friend1, friend2])
#     session.commit()
#
#     assert friend1.person == person
#     assert friend2.person == person
#     assert person.friends == [friend1, friend2]
