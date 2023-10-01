from typing import Optional
from pydantic import BaseModel
from ..models import PostSource


class PersonListSchema(BaseModel):
    id: int
    full_name: Optional[str] = None
    url: Optional[str] = None
    facebook_id: Optional[str] = None


class PersonDetailSchema(BaseModel):
    id: int
    full_name: Optional[str] = None
    url: Optional[str] = None
    facebook_id: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    number_of_friends: Optional[int] = None
    ai_summary: Optional[str] = None


class FamilyMemberSchema(BaseModel):
    id: int
    full_name: str
    role: Optional[str]
    url: Optional[str]
    person_id: int


class FriendsSchema(BaseModel):
    id: int
    person_id: int
    full_name: str
    url: Optional[str]


class ImageSchema(BaseModel):
    id: int
    path: str
    person_id: int


class PlacesSchema(BaseModel):
    id: int
    name: str
    date: Optional[str]
    person_id: int


class WorkAndEducationSchema(BaseModel):
    id: int
    name: str
    person_id: int


class RecentPlacesSchema(BaseModel):
    id: int
    localization: str
    date: Optional[str]
    person_id: int


class ReelsSchema(BaseModel):
    id: int
    url: str
    person_id: int
    downloaded: bool


class VideosSchema(BaseModel):
    id: int
    url: str
    person_id: int
    downloaded: bool


class ReviewsSchema(BaseModel):
    id: int
    company: str
    review: str
    person_id: int


class PostsSchema(BaseModel):
    id: int
    url: str
    person_id: int
    content: Optional[str]
    number_of_likes: Optional[int]
    number_of_shares: Optional[int]
    number_of_comments: Optional[int]
    scraped: bool
    source: PostSource
    classification: bool
    score: Optional[float]


class LikesSchema(BaseModel):
    id: int
    name: str
    person_id: int


class GroupsSchema(BaseModel):
    id: int
    name: str
    url: Optional[str]
    person_id: int


class EventsSchema(BaseModel):
    id: int
    name: str
    url: Optional[str]
    person_id: int


class CrawlerQueueSchema(BaseModel):
    id: int
    url: str
    status: bool = False
