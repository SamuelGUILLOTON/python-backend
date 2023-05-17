#system import
from datetime import datetime

#Libs imports
from sqlalchemy.orm import Session

#Local imports
from internal.models import Planning
from models.planning import EditPlanning
from crud import activity as activityCRUD

def get_planning_by_id(planningId: int, db: Session):
    return db.query(Planning).filter_by(id=planningId).first()

def plannings_by_company(companyId, db: Session):
    return db.query(Planning).filter_by(company_id=companyId).first()

def create_planning(companyId: int, EditPlanning: EditPlanning, db: Session):
    db_planning = Planning(
    planning = EditPlanning.planning,
    company_id = companyId, 
    created_at = datetime.now(),
    start_date = EditPlanning.start_date,
    end_date = EditPlanning.end_date 
    )
    print(db_planning)
    db.add(db_planning)
    db.commit()
    db.refresh(db_planning)
    return db_planning.planning

def update_planning(db: Session, NewEditPlanning: EditPlanning, planningId: int):
    db_planning = db.query(Planning).filter_by(id=planningId).first()
    #Je vérifie si les valeurs ajouter ne sont pas celle par défaut dans le swagger
    db_planning.planning = NewEditPlanning.planning if NewEditPlanning.planning != "string" else db_planning.planning
    db_planning.start_date = NewEditPlanning.start_date if NewEditPlanning.start_date != datetime.now else db_planning.start_date
    db_planning.updated_at = datetime.now()
    db.commit()
    db.refresh(db_planning)
    return db_planning.planning

def delete_planning(db: Session, planningId: int):
    planningActivities = activityCRUD.get_planning_activities(planningId, db)
    #Je supprime toute les activités d'un planning
    for planningActivity in planningActivities:
        db.delete(planningActivity)
        db.commit()
    #puis je supprime le planning
    db_planning = db.query(Planning).filter_by(id=planningId).first()
    db.delete(db_planning)
    db.commit()
    return True