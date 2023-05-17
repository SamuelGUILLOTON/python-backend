#System imports
from datetime import datetime
#Libs imports
from pydantic import BaseModel
#Local imports
from models.user import User

class Activity(BaseModel):
    id: int
    activity: str
    owner_id: int
    start_date: datetime
    end_date: datetime
    planning_id: int
    created_at: datetime
    user: list[User] = []
    
    class Config:
        orm_mode = True

class EditActivity(BaseModel):
    activity: str
    start_date: datetime
    end_date: datetime
    planning_id: int
    user: list[User] = []
    
    class Config:
        orm_mode = True