#System imports
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
#Libs imports
from fastapi import FastAPI, Response, status

#Local imports
from models.user import User


app = FastAPI()

url = URL.create(
    drivername="mysql",
    username="guilloton_10",
    password="Ferrari59139",
    host="mysql-guilloton.alwaysdata.net",
    database="guilloton_python",
    port=3306
)

engine = create_engine(url)
Session = sessionmaker(bind=engine)
session = Session()

@app.get("/")
async def get_all_users():
    users_query = session.query(User)
    return users_query.all()

