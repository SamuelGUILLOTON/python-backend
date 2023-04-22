#system import
from enum import Enum
from pydantic import BaseModel

class RoleEnum(Enum):
    ADMIN = "ADMIN"
    MAINTAINER = "MAINTAINER"
    USER = "USER"

class User(BaseModel):
    id: int
    lastname_hash: str
    firstname_hash: str
    mail_hash: str
    company_id: int
    role: RoleEnum
    password_hash: str
