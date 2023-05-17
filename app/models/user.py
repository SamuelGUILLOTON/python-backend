#system import
from enum import Enum
#Libs imports
from pydantic import BaseModel

class UserRole(str, Enum):
    user = "USER"
    admin = "ADMIN"
    maintainer = "MAINTAINER"

class User(BaseModel):
    id: int
    lastname_hash: str
    firstname_hash: str
    mail_hash: str
    company_id: str
    role: UserRole
    password_hash: str

    class Config:
        orm_mode = True

class EditUser(BaseModel):
    lastname_hash: str
    firstname_hash: str
    mail_hash: str
    role: str
    password_hash: str

    class Config:
        orm_mode = True
