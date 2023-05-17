#system import
from datetime import datetime
#Libs imports
from pydantic import BaseModel

class Notification(BaseModel):
    id: int
    created_at: datetime
    activity_id: int
    message: str

    class Config:
        orm_mode = True

class NewNotification(BaseModel):
    created_at: datetime
    activity_id: int
    message: str

    class Config:
        orm_mode = True
