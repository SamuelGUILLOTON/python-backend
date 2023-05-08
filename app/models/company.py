#system import
from pydantic import BaseModel

class Company(BaseModel):
    id: int
    company_name: str
    siret: int
    address: str