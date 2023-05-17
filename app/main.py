#System imports
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
#Libs imports
from fastapi import FastAPI

#Local imports
from routers import user, company, activity, planning
from internal import auth

app = FastAPI()

app.include_router(user.router, tags=["User"])
app.include_router(company.router, tags=["Company"])
app.include_router(activity.router, tags=["Activity"])
app.include_router(planning.router, tags=["Planning"])
app.include_router(auth.router, tags=["Authentification"])
