
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
from crud import user as userCRUD
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

#Route pour récupérer les activités d'un user 
@router.get("/users/{user_id}/activities")
async def get_user_activities(user_id: int, db: Session = Depends(get_db), auth: Annotated[User, Depends(decode_token)] = None) -> list[activitySchema]:
    user = userCRUD.get_user_by_id(db, user_id)
    #Si le user recherché n'est pas trouvé 
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    #Un user peux voir ses a ctivité, si son id est égale à l'id user recherché il est authorisé, autrement si l'admin ou le maintainer de l'entreprise c'est autorisé
    if (auth["id"] != user_id or auth["role"] != "ADMIN" and auth["role"] != "MAINTAINER" and auth["company_id"] != user.company_id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    userActivities = activityCRUD.get_user_activities(user_id, db)
    #gére le cas si le user n'a pas d'activité
    if not userActivities:
        raise HTTPException(status_code=404, detail="no activity found")
    return userActivities

#Route pour avoir tout les users d'une activité
@router.get("/activities/{activity_id}")
async def get_activiy_users(activity_id: int, db: Session = Depends(get_db), auth: Annotated[User, Depends(decode_token)] = None) -> list[userSchema]:
    allActivityUsers = activityCRUD.get_activity_users(activity_id)
    currentPlanning = planningCRUD.get_planning_by_id(activity_id, db)
    inActivity = False
    #je regarde si le user qui fait la recherche est dans l'activité recherché
    for user in allActivityUsers:
        if user["id"] == auth["id"]:
            inActivity = True
    #si le user n'est pas dans l'activité ou que c'est ce n'est pas un admin et un maintainer et qu'il ne fait partie de la méme company il n'est pas authorisé
    if (inActivity == False or auth["role"] != "ADMIN" and auth["role"] != "MAINTAINER" and auth["company_id"] != currentPlanning.company_id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    #si aucun user n'est rattaché à une activité cela renvoi une erreur
    if not allActivityUsers:
        raise HTTPException(status_code=404, detail="no user found")
    return allActivityUsers

#Route pour créer une activité, on rentre le planning parent à l'activité 
@router.post("/activities/{planning_id}")
async def create_activity(planning_id: int, EditActivity: EditActivity, db: Session = Depends(get_db), auth: Annotated[User, Depends(decode_token)] = None) -> str:
    currentPlanning = planningCRUD.get_planning_by_id(planning_id, db)
    #Si le user connecté ne fait pas partie de l'entreprise et que c'est un user: rejeté
    if (auth["company_id"] != currentPlanning.company_id and auth["role"] == "USER"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return activityCRUD.create_activity(planning_id, db, EditActivity, auth["id"])

#Route pour modifier une activité
@router.patch("/activities/{activity_id}")
async def update_activity(activityId: int, EditActivity: EditActivity, db: Session = Depends(get_db), auth: Annotated[User, Depends(decode_token)] = None) -> str:
    currentActivity = activityCRUD.get_activity_by_id(activityId, db)
    currentPlanning = planningCRUD.get_planning_by_id(currentActivity.planning_id, db)
    if not currentActivity or not currentPlanning:
        raise HTTPException(status_code=404, detail="no activity found")
    #Si le user connecté est un user et qu'il ne fait pas partie de la company ou que ce n'est pas le propriétaire de l'activité: rejeté
    if (auth["role"] != "MAINTAINER" and auth["role"] != "ADMIN" and auth["company_id"] != currentPlanning.company_id or auth["id"] != currentActivity.owner_id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return activityCRUD.update_activity(activityId, db, EditActivity)

#route pour supprimer une activité
@router.delete("/activities/{activity_id}")
async def delete_activity(activityId: int, db: Session = Depends(get_db), auth: Annotated[User, Depends(decode_token)] = None) -> str:
    currentActivity = activityCRUD.get_activity_by_id(activityId, db)
    currentPlanning = planningCRUD.get_planning_by_id(currentActivity.planning_id, db)
    if not currentActivity:
        raise HTTPException(status_code=404, detail="no activity found")
    #Si le user connecté est un user et qu'il ne fait pas partie de la company ou que ce n'est pas le propriétaire de l'activité: rejeté
    if (auth["role"] != "MAINTAINER" and auth["role"] != "ADMIN" and auth["company_id"] != currentPlanning.company_id or auth["id"] != currentActivity.owner_id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return activityCRUD.delete_activity(activityId, db, EditActivity)

#Route pour que le owner ou admin ajoute un user à une activité
@router.post("/activities/{activity_id}/users/{user_id}")
async def add_user_to_activity(activity_id: int, user_id: int, db: Session = Depends(get_db), auth: Annotated[User, Depends(decode_token)] = None) -> str:
    currentActivity = activityCRUD.get_activity_by_id(activity_id, db)
    currentPlanning = planningCRUD.get_planning_by_id(currentActivity.planning_id, db)
    currentUser = userCRUD.get_user_by_id(db, user_id)
    if not currentActivity or not currentPlanning or not currentUser:
        raise HTTPException(status_code=404, detail="no activity or user found")
    #si c'est un user ou si l'entreprise du planning ou de l'utilisateur à ajouter n'est pas la méme que le current user
    if (auth["role"] != "MAINTAINER" and auth["role"] != "ADMIN" or auth["company_id"] != currentPlanning.company_id or auth["company_id"] != currentUser.company_id ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    activityCRUD.add_user_to_activity(user_id, activity_id, db)
    return 'true'

#Route pour que l'utilisateur s'ajoute à une activité, seulement si il fait partie de l'entreprise
@router.post("/activities/users/{activity_id}")
async def register_to_activity(activity_id: int, user_id: int, db: Session = Depends(get_db), auth: Annotated[User, Depends(decode_token)] = None) -> str:
    currentActivity = activityCRUD.get_activity_by_id(activity_id, db)
    currentPlanning = planningCRUD.get_planning_by_id(currentActivity.planning_id, db)
    if not currentActivity and not currentPlanning:
        raise HTTPException(status_code=404, detail="no activity or user found")
    if (auth["company_id"] != currentPlanning.company_id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    activityCRUD.add_user_to_activity(auth["id"], activity_id, db)
    return 'true'


#Route pour que l'owner ou l'admin supprime un user d'une activité
@router.delete("/activities/{activity_id}/users/{user_id}")
async def delete_user_from_activity(activity_id: int, user_id: int, db: Session = Depends(get_db), auth: Annotated[User, Depends(decode_token)] = None) -> str:
    currentActivity = activityCRUD.get_activity_by_id(activity_id, db)
    currentPlanning = planningCRUD.get_planning_by_id(currentActivity.planning_id, db)
    if not currentActivity and not currentPlanning:
        raise HTTPException(status_code=404, detail="no activity or user found")
    if (auth["role"] != "MAINTAINER" and auth["role"] != "ADMIN" and auth["company_id"] != currentPlanning.company_id or auth["id"] != currentActivity.owner_id ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
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
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    activityCRUD.delete_user_from_activity(auth["id"], activity_id, db)
    return 'true'