#Libs imports
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Définition de l'URL de la base de données MySQL
SQLALCHEMY_DATABASE_URL = "mysql://guilloton_10:Ferrari59139@mysql-guilloton.alwaysdata.net/guilloton_python"

# Création d'un moteur SQLAlchemy pour se connecter à la base de données
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    echo=True
)

# Création d'une session de base de données pour effectuer des opérations
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()

