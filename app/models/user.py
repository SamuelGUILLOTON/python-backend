#system import
from enum import Enum
from pydantic import BaseModel

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import mapped_column


Base = declarative_base()

class RoleEnum(Enum):
    ADMIN = "ADMIN"
    MAINTAINER = "MAINTAINER"
    USER = "USER"

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    lastname_hash = Column(String)
    firstname_hash = Column(String)
    mail_hash = Column(String)
    company_id = Column(Integer)
    role = Column(String)
    password_hash = Column(String)

    def save(self, session):
        session.add(self)
        session.commit()
