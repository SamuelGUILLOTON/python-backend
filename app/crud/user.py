#system import

#Libs imports
from sqlalchemy.orm import Session
#Local imports
from internal.models import User
from models.user import EditUser
from internal.crypto import decrypt, encrypt
from internal.hash_pwd import hash_password

def get_users(db: Session):
    users = db.query(User).all()
    decrypted_users = []
    for user in users:
        decrypted_user = User(
            id=user.id,
            lastname_hash=decrypt(user.lastname_hash),
            firstname_hash=decrypt(user.firstname_hash),
            mail_hash=decrypt(user.mail_hash),
            company_id=user.company_id,
            role=user.role,
            password_hash=user.password_hash
        )
        decrypted_users.append(decrypted_user)
    return decrypted_users

def get_user_by_id(db: Session, userId: int):
    user = db.query(User).filter_by(id=userId).first()
    user = User(
        id=user.id,  
        lastname_hash=decrypt(user.lastname_hash),
        firstname_hash=decrypt(user.firstname_hash),
        mail_hash=decrypt(user.mail_hash),
        company_id=user.company_id,
        role=user.role,
        password_hash=user.password_hash
    )
    return user

def get_user_by_mail(db: Session, mail: str):
    user = db.query(User).filter_by(mail_hash=mail).first()
    user = dict(  
        lastname_hash= decrypt(user.firstname_hash),
        firstname_hash= decrypt(user.firstname_hash),
        mail_hash= decrypt(user.mail_hash),
        company_id=user.company_id,
        role=user.role,
        password_hash=user.password_hash
    )
    return user

#création d'un utilisateur, check si le mail exist. L'id de la company est celle du user qui ajoute le nouveau user
def create_user(db: Session, EditUser: EditUser, company_id: int):
    users = db.query(User).all()
    for user in users:
        if EditUser.mail_hash == decrypt(user.mail_hash):
            return False
    print(EditUser)
    db_user = User(
    lastname_hash = encrypt(EditUser.lastname_hash),
    firstname_hash =  encrypt(EditUser.firstname_hash), 
    mail_hash =  encrypt(EditUser.mail_hash),
    company_id = company_id,
    role = EditUser.role, 
    password_hash = hash_password(EditUser.password_hash), 
    )
    print(db_user)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_user(db: Session, user: User, userId: int):
    db_user = db.query(User).filter_by(id=userId).first()
    db.delete(db_user)
    db.commit()
    return db_user.mail_hash

def update_user(db: Session, NewEditUser: EditUser, userId: int):
    db_user = db.query(User).filter_by(id=userId).first()
    db_user.lastname_hash = encrypt(NewEditUser.lastname_hash) if NewEditUser.lastname_hash != "string" else db_user.lastname_hash
    db_user.firstname_hash = encrypt(NewEditUser.firstname_hash) if NewEditUser.firstname_hash != "string" else db_user.firstname_hash
    db_user.mail_hash = encrypt(NewEditUser.mail_hash) if NewEditUser.mail_hash != "string" else db_user.mail_hash
    db_user.role = NewEditUser.role if NewEditUser.role != "string" else db_user.role
    db_user.password_hash = hash_password(NewEditUser.password_hash) if NewEditUser.password_hash != "string" else db_user.password_hash
    db.commit()
    db.refresh(db_user)
    return db_user.firstname_hash

def get_users_by_company(companyId: int, db: Session):
    users = db.query(User).filter_by(company_id=companyId).all()
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