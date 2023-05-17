#system import
from typing import Annotated

# Libs Imports
from fastapi import APIRouter, status, HTTPException
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException

#Local imports
from crud import company as companyCRUD, user as userCRUD
from internal.models import Company
from models.company import Company as companySchema, EditCompany
from models.user import User as userSchema, EditUser
from db.database import SessionLocal
from internal.models import User
from internal.auth import decode_token

router = APIRouter()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/companies")
async def create_company(EditCompany: EditCompany, db: Session = Depends(get_db), auth: Annotated[User, Depends(decode_token)] = None) -> str:
    if (auth["role"] != "MAINTAINER"):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    company_name = companyCRUD.create_company(db, EditCompany, auth["id"])
    return company_name

@router.delete("/companies/{companyId}")
async def delete_company(companyId: int, db: Session = Depends(get_db), auth: Annotated[User, Depends(decode_token)] = None ) -> str:
    currentCompany = companyCRUD.get_company_by_id(db, companyId)
    if not currentCompany:
        raise HTTPException(status_code=404, detail="Company not found")
    if (auth["role"] != "MAINTAINER" or auth["id"] != currentCompany.owner_id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    delete_company = companyCRUD.delete_company(db, companyId)
    return delete_company

@router.patch("/companies/{companyId}")
async def update_company(companyId: int, EditCompany: EditCompany, db: Session = Depends(get_db), auth: Annotated[User, Depends(decode_token)] = None) -> str:
    currentCompany = companyCRUD.get_company_by_id(db, companyId)
    if not currentCompany:
        raise HTTPException(status_code=404, detail="Company not found")
    if (auth["role"] != "MAINTAINER" or auth["id"] != currentCompany.owner_id):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    response = companyCRUD.update_company(db, EditCompany, companyId)
    return response

@router.get("/users/company/{companyId}")
async def users_by_company(companyId: int, db: Session = Depends(get_db), auth: Annotated[User, Depends(decode_token)] = None ) -> list[userSchema]:
    if (auth["role"] != "MAINTAINER" and auth["role"] != "ADMIN" or auth["company_id"] != companyId):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")
    users = userCRUD.get_users_by_company(companyId, db)
    if not users:
        raise HTTPException(status_code=404, detail="no users found")
    return users