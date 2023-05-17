#system import

#Libs imports
from sqlalchemy.orm import Session
#Local imports
from internal.models import Company
from models.company import Company as CompanyShema, EditCompany

#Récupérer l'ntreprise avec un Id
def get_company_by_id(db: Session, company_id: int):
    return  db.query(Company).filter(Company.id == company_id).first()

def create_company(db: Session, EditCompany: EditCompany, ownerId: int):
    db_company = Company(
    name = EditCompany.name, 
    address = EditCompany.address,
    siret = EditCompany.siret,
    owner_id = ownerId, 
    )
    print(db_company)
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company.name

def update_company(db: Session, NewEditCompany: EditCompany, companyId: int):
    db_company = db.query(Company).filter_by(id=companyId).first()
    db_company.name = NewEditCompany.name if NewEditCompany.name != "string" else db_company.name
    db_company.address = NewEditCompany.address if NewEditCompany.address != "string" else db_company.address
    db_company.siret = NewEditCompany.siret if NewEditCompany.siret != 0 else db_company.siret
    print(db_company)
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company.name

def delete_company(db: Session, companyId: int):
    db_company = db.query(Company).filter_by(id=companyId).first()
    db.delete(db_company)
    db.commit()
    return db_company.name


    