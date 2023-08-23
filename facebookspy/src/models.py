from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, Enum as EnumColumn
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from enum import Enum

Base = declarative_base()


class FamilyMember(Base):
    __tablename__ = "family_members"

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String, nullable=False)
    role = Column(String, nullable=True)
    url = Column(String, nullable=True)
    person_id = Column(Integer, ForeignKey("persons.id"))

    # Relationship
    person = relationship("Person", back_populates="family_member")


class Friends(Base):
    __tablename__ = "friends"

    id = Column(Integer, primary_key=True, autoincrement=True)
    person_id = Column(Integer, ForeignKey("persons.id"))
    full_name = Column(String, nullable=False)
    url = Column(String, nullable=True)

    # Relationship
    person = relationship("Person", back_populates="friends")


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, autoincrement=True)
    path = Column(String, nullable=False)
    person_id = Column(Integer, ForeignKey("persons.id"))

    # Relationship
    person = relationship("Person", back_populates="images")


class Person(Base):
    __tablename__ = "persons"

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String, nullable=True)
    url = Column(String, nullable=True)
    facebook_id = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    email = Column(String, nullable=True)

    # Relationships (using backref for bidirectional relationship)
    friends = relationship("Friends", back_populates="person")
    images = relationship("Image", back_populates="person")
    places = relationship("Places", uselist=False, back_populates="person")
    work_and_education = relationship(
        "WorkAndEducation", uselist=False, back_populates="person"
    )
    family_member = relationship("FamilyMember", uselist=False, back_populates="person")
    recent_places = relationship("RecentPlaces", uselist=False, back_populates="person")
    reels = relationship("Reels", uselist=False, back_populates="person")
    videos = relationship("Videos", uselist=False, back_populates="person")
    reviews = relationship("Reviews", uselist=False, back_populates="person")
    note = relationship("Notes", uselist=False, back_populates="person")
    posts = relationship("Posts", uselist=False, back_populates="person")
    likes = relationship("Likes", uselist=False, back_populates="person")
    groups = relationship("Groups", uselist=False, back_populates="person")
    events = relationship("Events", uselist=False, back_populates="person")


class Places(Base):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    date = Column(String, nullable=True)
    person_id = Column(Integer, ForeignKey("persons.id"))

    # Relationship
    person = relationship("Person", back_populates="places")


class WorkAndEducation(Base):
    __tablename__ = "work_and_education"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    person_id = Column(Integer, ForeignKey("persons.id"))

    # Relationship
    person = relationship("Person", back_populates="work_and_education")


class RecentPlaces(Base):
    __tablename__ = "recent_places"

    id = Column(Integer, primary_key=True, autoincrement=True)
    localization = Column(String, nullable=False)
    date = Column(String, nullable=True)
    person_id = Column(Integer, ForeignKey("persons.id"))

    # Relationship
    person = relationship("Person", back_populates="recent_places")


class Reels(Base):
    __tablename__ = "reels"

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, nullable=False)
    person_id = Column(Integer, ForeignKey("persons.id"))
    downloaded = Column(Boolean, default=False)

    # Relationship
    person = relationship("Person", back_populates="reels")


class Videos(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, nullable=False)
    person_id = Column(Integer, ForeignKey("persons.id"))
    downloaded = Column(Boolean, default=False)

    # Relationship
    person = relationship("Person", back_populates="videos")


class Reviews(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company = Column(String, nullable=False)
    review = Column(String, nullable=False)
    person_id = Column(Integer, ForeignKey("persons.id"))

    # Relationship
    person = relationship("Person", back_populates="reviews")


class Notes(Base):
    __tablename__ = "notes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    content = Column(String, nullable=True)
    person_id = Column(Integer, ForeignKey("persons.id"))

    # Relationship
    person = relationship("Person", back_populates="note")


class PostSource(Enum):
    GROUP = "GROUP"
    ACCOUNT = "ACCOUNT"


class Posts(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String, nullable=False)
    person_id = Column(Integer, ForeignKey("persons.id"))
    content = Column(String, nullable=True)
    number_of_likes = Column(Integer, nullable=True)
    number_of_shares = Column(Integer, nullable=True)
    number_of_comments = Column(Integer, nullable=True)
    scraped = Column(Boolean, default=False)
    source = Column(EnumColumn(PostSource), default=PostSource.ACCOUNT)

    # Relationship
    person = relationship("Person", back_populates="posts")


class Likes(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    person_id = Column(Integer, ForeignKey("persons.id"))

    # Relationship
    person = relationship("Person", back_populates="likes")


class Groups(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    url = Column(String, nullable=True)
    person_id = Column(Integer, ForeignKey("persons.id"))

    # Relationship
    person = relationship("Person", back_populates="groups")


class Events(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    url = Column(String, nullable=True)
    person_id = Column(Integer, ForeignKey("persons.id"))

    # Relationships
    person = relationship("Person", back_populates="events")
