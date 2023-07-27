from sqlalchemy import Column, String, Integer, ForeignKey
from .database import Base
from sqlalchemy.orm import relationship


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
    full_name = Column(String, nullable=False)
    url = Column(String, nullable=True)
    facebook_id = Column(String, nullable=True)

    # Relationships (using backref for bidirectional relationship)
    friends = relationship("Friends", back_populates="person")
    images = relationship("Image", back_populates="person")
    places = relationship("Places", uselist=False, back_populates="person")
    work_and_education = relationship(
        "WorkAndEducation", uselist=False, back_populates="person"
    )
    family_member = relationship("FamilyMember", uselist=False, back_populates="person")


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
