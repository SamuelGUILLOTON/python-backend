#Libs imports
from pydantic import BaseModel

class Company(BaseModel):
    id: int
    name: str
    address: str
    siret: int
    owner_id: int

    class Config:
        orm_mode = True

class EditCompany(BaseModel):
    name: str
    address: str
    siret: int

    class Config:
        orm_mode = True
