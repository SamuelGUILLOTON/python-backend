#system import
from pydantic import BaseModel
from datetime import datetime

class Activity(BaseModel):
    id: int
    date: datetime
    start: datetime
    end: datetime
    address: str
    owner: int