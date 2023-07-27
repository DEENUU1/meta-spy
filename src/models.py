from sqlalchemy import Column, String, Integer, ForeignKey
from database import Base
from sqlalchemy.orm import relationship


class Person(Base):
    __tablename__ = "persons"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    url = Column(String, index=True)
    facebook_id = Column(String, index=True)
    family_member = relationship("FamilyMember", back_populates="person", uselist=False)
    places = relationship("Places", back_populates="person")
    work_and_education = relationship("WorkAndEducation", back_populates="person")
    image = relationship("Image", back_populates="person", uselist=False)
    friends = relationship("Friends", back_populates="person")


class Friends(Base):
    __tablename__ = "friends"
    id = Column(Integer, primary_key=True, index=True)
    person_id = Column(Integer, ForeignKey("persons.id"))
    fullname = Column(String)
    url = Column(String)
    person = relationship("Person", back_populates="friends")


class Image(Base):
    __tablename__ = "images"
    id = Column(Integer, primary_key=True, index=True)
    path = Column(String)
    person_id = Column(Integer, ForeignKey("persons.id"))
    person = relationship("Person", back_populates="image")


class Places(Base):
    __tablename__ = "places"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    date = Column(String)
    person_id = Column(Integer, ForeignKey("persons.id"))
    person = relationship("Person", back_populates="places")


class WorkAndEducation(Base):
    __tablename__ = "work_and_education"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    person_id = Column(Integer, ForeignKey("persons.id"))
    person = relationship("Person", back_populates="work_and_education")


class FamilyMember(Base):
    __tablename__ = "family_members"
    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String)
    role = Column(String)
    url = Column(String)
    person_id = Column(Integer, ForeignKey("persons.id"))
    person = relationship("Person", back_populates="family_member")
