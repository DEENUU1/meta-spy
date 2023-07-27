from sqlalchemy import Column, String, Integer, ForeignKey
from database import Base
from sqlalchemy.orm import relationship
from typing import Optional


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

    def add_friends(self, full_name: str, url: Optional[str] = None):
        friend = Friends(full_name=full_name, url=url)
        self.friends.append(friend)

    def add_image(self, path: str):
        image = Image(path=path)
        self.images.append(image)

    def add_places(self, name: str, date: Optional[str] = None):
        places = Places(name=name, date=date)
        self.places = places

    def add_work_and_education(self, name: str):
        work_and_education = WorkAndEducation(name=name)
        self.work_and_education = work_and_education

    def add_family_member(
        self, full_name: str, role: Optional[str] = None, url: Optional[str] = None
    ):
        family_member = FamilyMember(full_name=full_name, role=role, url=url)
        self.family_member = family_member


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


class FamilyMember(Base):
    __tablename__ = "family_members"

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String, nullable=False)
    role = Column(String, nullable=True)
    url = Column(String, nullable=True)
    person_id = Column(Integer, ForeignKey("persons.id"))

    # Relationship
    person = relationship("Person", back_populates="family_member")
