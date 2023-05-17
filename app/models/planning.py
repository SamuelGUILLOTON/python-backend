#system import
from datetime import datetime
#Libs imports
from pydantic import BaseModel

class Planning(BaseModel):
    id: int
    planning: str
    company_id: int
    created_at: datetime
    updated_at: datetime
    start_date: datetime
    end_date: datetime

    class Config:
        orm_mode = True

class EditPlanning(BaseModel):
    planning: str
    start_date: datetime
    end_date: datetime

    class Config:
        orm_mode = True