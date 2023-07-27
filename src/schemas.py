from pydantic import BaseModel
from typing import List


class ImageSchema(BaseModel):
    path: str
    person_id: int


class PlacesSchema(BaseModel):
    name: str
    date: str
    person_id: int


class WorkAndEducationSchema(BaseModel):
    name: str
    person_id: int


class FamilyMemberSchema(BaseModel):
    full_name: str
    role: str
    url: str
    person_id: int


class FriendsSchema(BaseModel):
    fullname: str
    url: str


class PersonSchema(BaseModel):
    full_name: str
    url: str
    facebook_id: str
    family_member: FamilyMemberSchema
    places: List[PlacesSchema]
    work_and_education: List[WorkAndEducationSchema]
    image: ImageSchema
    friends: List[FriendsSchema]

    class Config:
        orm_mode = True
