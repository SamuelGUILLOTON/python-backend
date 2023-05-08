#system import
from pydantic import BaseModel

class Activity(BaseModel):
    id: int
    activity: str
    owner: int