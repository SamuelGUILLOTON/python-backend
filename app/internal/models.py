#system import
from enum import Enum
#Libs imports
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# Declare Classes / Tables
userActivity = Table('userActivity', Base.metadata,
    Column('activity_id', ForeignKey('activity.id'), primary_key=True),
    Column('user_id', ForeignKey('user.id'), primary_key=True)
)

userNotification = Table('userNotification', Base.metadata,
    Column('notification_id', ForeignKey('notification.id'), primary_key=True),
    Column('user_id', ForeignKey('user.id'), primary_key=True)
)

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
    company_id = Column(Integer, ForeignKey("company.id"), nullable=True)
    role = Column(String)
    password_hash = Column(String)
    activity = relationship("Activity", secondary="userActivity", back_populates="user")
    notification = relationship("Notification", secondary="userNotification", back_populates="user")
    
class Company(Base):
    __tablename__ = "company"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    siret = Column(String)
    owner_id = Column(Integer, ForeignKey("user.id"))

class Planning(Base):
    __tablename__ = "planning"

    id = Column(Integer, primary_key=True, index=True)
    planning = Column(String)
    company_id = Column(Integer, ForeignKey("company.id"))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    start_date = Column(DateTime)
    end_date = Column(DateTime)

class Activity(Base):
    __tablename__ = "activity"

    id = Column(Integer, primary_key=True)
    activity = Column(String)
    owner_id = Column(Integer, ForeignKey("user.id"))
    start_date = Column(DateTime)
    end_date = Column(DateTime)
    planning_id = Column(Integer, ForeignKey("planning.id"))
    created_at = Column(DateTime)
    user = relationship("User", secondary="userActivity", back_populates="activity")


class Notification(Base):
    __tablename__ = "notification"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime)
    activity_id = Column(Integer, ForeignKey("activity.id"))
    message = Column(String)
    user = relationship("User", secondary="userNotification", back_populates="notification")

    class Config:
        orm_mode = True