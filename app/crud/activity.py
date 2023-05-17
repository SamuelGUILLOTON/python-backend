#system import
from datetime import datetime

#Libs imports
from sqlalchemy.orm import Session

#Local imports
from models.user import EditUser
from internal.crypto import decrypt
from internal.models import Activity, User, Notification
from models.activity import EditActivity

def get_activity_by_id(activityId: int, db: Session):
    return db.query(Activity).filter_by(id=activityId).first()

def get_user_activities(user_id: int, db: Session):
    return db.query(Activity).join(Activity.user).filter(User.id == user_id).all()

def get_activity_users(activity_id: int, db: Session, EditUser: EditUser):
    users = db.query(User).join(User.activity).filter(Activity.id == activity_id).all()
    decrypted_users = []
    for user in users:
        decrypted_user = EditUser(
            lastname_hash=decrypt(user.lastname_hash),
            firstname_hash=decrypt(user.firstname_hash),
            mail_hash=decrypt(user.mail_hash),
            company_id=user.company_id,
            role=user.role,
            password_hash=user.password_hash
        )
        decrypted_users.append(decrypted_user)
    return decrypted_users

def get_planning_activities(planning_id: id, db: Session):
     return db.query(Activity).filter(Activity.planning_id == planning_id).all()
    
def create_activity(planning_id: id, db: Session, EditActivity: EditActivity, ownerId: int):
    db_activity = Activity(
    activity = EditActivity.activity, 
    owner_id = ownerId,
    start_date = EditActivity.start_date,
    end_date = EditActivity.end_date,
    planning_id = planning_id, 
    )
    print(db_activity)
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity.activity

def update_activity(activity_id: int, db: Session, NewEditActivity: EditActivity):
    db_activity = db.query(Activity).filter_by(id=activity_id).first()
    db_activity.activity = NewEditActivity.activity if NewEditActivity.activity != "string" else db_activity.activity
    db_activity.start_date = NewEditActivity.start_date if NewEditActivity.start_date != datetime.now() else db_activity.start_date
    db_activity.end_date = NewEditActivity.end_date if NewEditActivity.end_date != datetime.now() else db_activity.end_date
    db_activity.planning_id = NewEditActivity.planning_id if NewEditActivity.planning_id != 0 else db_activity.planning_id
    db_activity.user = db_activity.user
    db.commit()
    db.refresh(db_activity)
    #create notif
    db_notification = Notification(
    created_at = datetime.now(), 
    activity_id = activity_id,
    message = "there is some change on your activity , {activity_name}".format(activity_name=db_activity.activity)
    )
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    #add user to notif
    usersActivity = db.query(User).join(User.activity).filter(Activity.id == activity_id).all()
    for user in usersActivity:
        db_notification.user.append(user) 
    db.commit()
    return db_activity.activity

def delete_activity(activity_id: int, db: Session):
    db_activity = db.query(Activity).filter_by(id=activity_id).first()
    #create notif
    db_notification = Notification(
    created_at = datetime.now(), 
    activity_id = activity_id,
    message = "your activity has been removed , {activity_name}".format(activity_name=db_activity.activity)
    )
    #add notification to user and remove user from activity
    usersActivity = db.query(User).join(User.activity).filter(Activity.id == activity_id).all()
    for user in usersActivity:
        db_notification.user.append(user)
        db_activity.user.remove(user) 
    db.commit()
    #delete activity
    db.delete(db_activity)
    db.commit()
    return db_activity.activity

def add_user_to_activity(user_id: int, activity_id: int, db: Session):
    db_user = db.query(User).filter_by(id=user_id).first()
    db_activity = db.query(Activity).filter_by(id=activity_id).first()
    print(db_activity)
    db_activity.user.append(db_user)
    db.commit()
    db.refresh(db_activity)
    #create notif
    db_notification = Notification(
    created_at = datetime.now(), 
    activity_id = activity_id,
    message = "you have been add to , {activity_name}".format(activity_name=db_activity.activity)
    )
    #add notification to user and 
    db_notification.user.append(db_user)
    db.commit()
    return "true"
    

def delete_user_from_activity(user_id: int, activity_id: int, db: Session):
    db_user = db.query(User).filter_by(id=user_id).first()
    db_activity = db.query(Activity).filter_by(id=activity_id).first()
    db_activity.user.remove(db_user)
    db.commit()
    #create notif
    db_notification = Notification(
    created_at = datetime.now(), 
    activity_id = activity_id,
    message = "You have been removed from , {activity_name}".format(activity_name=db_activity.activity)
    )
    #add notification to user and 
    db_notification.user.append(db_user)
    db.commit()
    return 'true'