
#system import
from typing import Annotated
# Libs Imports
from fastapi import APIRouter, status, HTTPException
from fastapi import Depends, HTTPException
#Local imports
from sqlalchemy.orm import Session
from db.database import SessionLocal
from internal.auth import decode_token
from crud import activity as activityCRUD, planning as planningCRUD
from internal.models import Activity
from internal.models import User
from models.activity import EditActivity, Activity as activitySchema
from models.user import User as userSchema

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/users/{user_id}/activities")
async def get_user_activities(user_id: int, db: Session = Depends(get_db), auth: Annotated[User, Depends(decode_token)] = None) -> list[activitySchema]:
    if (auth["id"] != user_id and auth["role"] == "USER"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Your only authorizes to see your activites")
    userActivities = activityCRUD.get_user_activities(user_id, db)
    if not userActivities:
        raise HTTPException(status_code=404, detail="no activity found")
    return userActivities

@router.get("/activities/{activity_id}")
async def get_activiy_users(activity_id: int, db: Session = Depends(get_db), auth: Annotated[User, Depends(decode_token)] = None) -> list[userSchema]:
    allActivityUsers = activityCRUD.get_activity_users(activity_id)
    inActivity = False
    for user in allActivityUsers:
        if user["id"] == auth["id"]:
            inActivity = True
    if (inActivity == False and auth["role"] != "ADMIN" and auth["role"] != "MAINTAINER"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Your only authorizes to see your activites")
    if not allActivityUsers:
        raise HTTPException(status_code=404, detail="no user found")
    return allActivityUsers

@router.post("/activities/{planning_id}")
async def create_activity(planning_id: int, EditActivity: EditActivity, db: Session = Depends(get_db), auth: Annotated[User, Depends(decode_token)] = None) -> str:
    currentPlanning = planningCRUD.get_planning_by_id(db, planning_id)
    if (auth["company_id"] != currentPlanning.company_id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Your only authorizes to see your activites")
    return activityCRUD.create_activity(planning_id, db, EditActivity, auth["id"])

@router.patch("/activities/{activity_id}")
async def update_activity(activityId: int, EditActivity: EditActivity, db: Session = Depends(get_db), auth: Annotated[User, Depends(decode_token)] = None) -> str:
    currentActivity = activityCRUD.get_activity_by_id(activityId, db)
    if not currentActivity:
        raise HTTPException(status_code=404, detail="no activity found")
    if (auth["role"] != "MAINTAINER" and auth["role"] != "ADMIN" and auth["id"] != currentActivity.owner_id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Your only authorizes to see your activites")
    return activityCRUD.update_activity(activityId, db, EditActivity)

@router.delete("/activities/{activity_id}")
async def delete_activity(activityId: int, db: Session = Depends(get_db), auth: Annotated[User, Depends(decode_token)] = None) -> str:
    currentActivity = activityCRUD.get_activity_by_id(activityId, db)
    if not currentActivity:
        raise HTTPException(status_code=404, detail="no activity found")
    if (auth["role"] != "MAINTAINER" and auth["role"] != "ADMIN" and auth["id"] != currentActivity.owner_id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Your only authorizes to see your activites")
    return activityCRUD.delete_activity(activityId, db, EditActivity)

###pour que le owner ou admin ajoute un user à une activité
@router.post("/activities/{activity_id}/users/{user_id}")
async def add_user_to_activity(activity_id: int, user_id: int, db: Session = Depends(get_db), auth: Annotated[User, Depends(decode_token)] = None) -> str:
    currentActivity = activityCRUD.get_activity_by_id(activity_id, db)
    currentPlanning = planningCRUD.get_planning_by_id(currentActivity.planning_id, db)
    if not currentActivity and not currentPlanning:
        raise HTTPException(status_code=404, detail="no activity or user found")
    if (auth["role"] != "MAINTAINER" and auth["role"] != "ADMIN" and auth["company_id"] != currentPlanning.company_id or auth["id"] != currentActivity.owner_id ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Your only authorizes to see your activites")
    #if not db_user:
    #    raise HTTPException(status_code=404, detail="User not found")
    activityCRUD.add_user_to_activity(user_id, activity_id, db)
    return 'true'

###pour que l'utilisateur s'ajoute à une activité, seulement si il fait partie de l'entreprise
@router.post("/activities/users/{activity_id}")
async def register_to_activity(activity_id: int, user_id: int, db: Session = Depends(get_db), auth: Annotated[User, Depends(decode_token)] = None) -> str:
    currentActivity = activityCRUD.get_activity_by_id(activity_id, db)
    currentPlanning = planningCRUD.get_planning_by_id(currentActivity.planning_id, db)
    if not currentActivity and not currentPlanning:
        raise HTTPException(status_code=404, detail="no activity or user found")
    if (auth["company_id"] != currentPlanning.company_id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Your only register to your company activity")
    #if not db_user:
    #    raise HTTPException(status_code=404, detail="User not found")
    activityCRUD.add_user_to_activity(auth["id"], activity_id, db)
    return 'true'


###pour que l'owner ou l'admin supprime un user d'une activité
@router.delete("/activities/{activity_id}/users/{user_id}")
async def delete_user_from_activity(activity_id: int, user_id: int, db: Session = Depends(get_db), auth: Annotated[User, Depends(decode_token)] = None) -> str:
    currentActivity = activityCRUD.get_activity_by_id(activity_id, db)
    currentPlanning = planningCRUD.get_planning_by_id(currentActivity.planning_id, db)
    if not currentActivity and not currentPlanning:
        raise HTTPException(status_code=404, detail="no activity or user found")
    if (auth["role"] != "MAINTAINER" and auth["role"] != "ADMIN" and auth["company_id"] != currentPlanning.company_id or auth["id"] != currentActivity.owner_id ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Your only authorizes to see your activites")
    #if not db_user:
    #    raise HTTPException(status_code=404, detail="User not found")
    activityCRUD.delete_user_from_activity(user_id, activity_id, db)
    return 'true'


###pour que lutilisateur se supprime d'une activité
@router.delete("/activities/users/{activity_id}")
async def unsubscribe_user_from_activity(activity_id: int, db: Session = Depends(get_db), auth: Annotated[User, Depends(decode_token)] = None) -> str:
    currentActivity = activityCRUD.get_activity_by_id(activity_id, db)
    currentPlanning = planningCRUD.get_planning_by_id(currentActivity.planning_id, db)
    if not currentActivity and not currentPlanning:
        raise HTTPException(status_code=404, detail="no activity or user found")
    if (auth["company_id"] != currentPlanning.company_id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Your only register to your company activity")
    #if not db_user:
    #    raise HTTPException(status_code=404, detail="User not found")
    activityCRUD.delete_user_from_activity(auth["id"], activity_id, db)
    return 'true'