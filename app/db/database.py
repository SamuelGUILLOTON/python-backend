#Libs imports
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "mysql://guilloton_10:Ferrari59139@mysql-guilloton.alwaysdata.net/guilloton_python"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#Base = declarative_base()

session = SessionLocal()

