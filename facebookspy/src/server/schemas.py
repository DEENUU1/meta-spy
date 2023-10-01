from typing import Optional
from pydantic import BaseModel


class PersonListSchema(BaseModel):
    id: int
    full_name: Optional[str] = None
    url: Optional[str] = None
    facebook_id: Optional[str] = None
