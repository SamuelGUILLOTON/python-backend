#System imports
from typing import Annotated


#Libs imports
from fastapi import Depends, APIRouter, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from sqlalchemy.orm import Session

#Local imports
from internal.models import User
from crud import user as userCRUD
from db.database import SessionLocal
from internal.hash_pwd import hash_password

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

JWT_KEY = "apzoapzoeziueipuzeredsdf"

async def decode_token(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        decoded_data = jwt.decode(token, JWT_KEY, algorithms=['HS256'])
        user = userCRUD.get_user_by_id(db, decoded_data["id"]).__dict__
        if user == None:
            raise credentials_exception
    except JWTError:
        return credentials_exception
    return user


@router.post("/login")
async def login(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    users = [user.__dict__ for user in userCRUD.get_users(db)]
    print(users)
    for user in users:
        print(user)
        print(form_data.password)
        print(hash_password(form_data.password))
        if user["mail_hash"] == form_data.username and user["password_hash"] == hash_password(form_data.password):
            data = dict()
            data["id"] = user["id"]
            jwt_token = jwt.encode(data, JWT_KEY, algorithm="HS256")
            return {"access_token": jwt_token, "token_type": "bearer"}
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username or password")