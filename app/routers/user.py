#system import
from typing import Annotated

# Libs Imports
from fastapi import APIRouter, status, HTTPException
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

#Local imports
from db.database import SessionLocal
from internal.auth import decode_token
from crud import user as userCRUD
from internal.models import User
from models.user import User as userSchema, EditUser

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/users")
async def read_users(db: Session = Depends(get_db), auth: Annotated[User, Depends(decode_token)] = None ) -> list[userSchema]:
    if (auth["role"] != "MAINTAINER"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    users = userCRUD.get_users(db)
    if not users:
        raise HTTPException(status_code=404, detail="Users not found")
    return users
         
@router.post("/users")
async def create_user(EditUser: EditUser, db: Session = Depends(get_db), auth: Annotated[User, Depends(decode_token)] = None ) -> EditUser:
    if (auth["role"] != "MAINTAINER" and auth["role"] != "ADMIN"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    result = userCRUD.create_user(db, EditUser, auth['company_id'])
    if result == False:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Mail already exist")
    return result

@router.delete("/user/{userId}")
async def delete_user(userId: int, db: Session = Depends(get_db), auth: Annotated[User, Depends(decode_token)] = None) -> str:
    oldUser = userCRUD.get_user_by_id(db, userId)
    if not oldUser:
        raise HTTPException(status_code=404, detail="User not found")
    if (auth["role"] != "MAINTAINER" and auth["role"] != "ADMIN" or auth["company_id"] != oldUser.company_id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    delete_user = userCRUD.delete_user(db, User, userId)
    return delete_user

@router.patch("/user/{userId}")
async def update_user(userId: int, EditUser: EditUser, db: Session = Depends(get_db), auth: Annotated[User, Depends(decode_token)] = None) -> str:
    currentUser = userCRUD.get_user_by_id(db, userId)
    if not currentUser:
        raise HTTPException(status_code=404, detail="User not found")
    if (auth["role"] != "MAINTAINER" and auth["role"] != "ADMIN" or auth["company_id"] != currentUser.company_id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    response = userCRUD.update_user(db, EditUser, userId)
    return response