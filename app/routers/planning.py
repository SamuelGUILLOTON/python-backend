#system import
from typing import Annotated

# Libs Imports
from fastapi import APIRouter, status, HTTPException
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException

#Local imports
from db.database import SessionLocal
from internal.models import User
from internal.auth import decode_token
from crud import planning as planningCRUD
from models.planning import Planning as planningSchema, EditPlanning

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/planning")
async def plannings_by_company(db: Session = Depends(get_db), auth: Annotated[User, Depends(decode_token)] = None ) -> list[planningSchema]:
    if (auth["role"] != "MAINTAINER" and auth["role"] != "ADMIN"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    planning = planningCRUD.plannings_by_company(auth["id"], auth["company_id"], db)
    if not planning:
        raise HTTPException(status_code=404, detail="Planning not found")
    return planning

@router.post("/planning")
async def create_planning(EditPlanning: EditPlanning, db: Session = Depends(get_db), auth: Annotated[User, Depends(decode_token)] = None) -> str:
    if (auth["role"] != "MAINTAINER" and auth["role"] != "ADMIN"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return planningCRUD.create_planning(auth["company_id"], EditPlanning, db)


@router.patch("/planning/{planningId}")
async def update_planning(planningId: int, EditPlanning: EditPlanning, db: Session = Depends(get_db), auth: Annotated[User, Depends(decode_token)] = None) -> str:
    currentPlanning = planningCRUD.get_planning_by_id(planningId, db)
    if not currentPlanning:
        raise HTTPException(status_code=404, detail="Planning not found")
    if (auth["role"] != "MAINTAINER" and auth["role"] != "ADMIN" and auth["company_id"] != currentPlanning.company_id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return planningCRUD.update_planning(db, EditPlanning, auth["company_id"])

#delete planning si le admin est dans lentrpeise
#ajouter ou supprimer des usrs d'une activity
@router.delete("/planning/{planning_id}")
async def delete_planning(planningId: int, db: Session = Depends(get_db), auth: Annotated[User, Depends(decode_token)] = None) -> str:
    currentPlanning = planningCRUD.get_planning_by_id(planningId, db)
    if not currentPlanning:
        raise HTTPException(status_code=404, detail="Planning not found")
    if (auth["role"] != "MAINTAINER" and auth["role"] != "ADMIN" and auth["company_id"] != currentPlanning.company_id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    return planningCRUD.delete_planning(db, planningId)

