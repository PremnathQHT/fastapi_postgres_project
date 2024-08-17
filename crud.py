import schemas
import models
import datetime
from sqlalchemy.orm import Session
from logs.qtoolslogger import logger


#User Creation on DB
def create_users(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username, email=user.email,
        hash_password=user.hash_password,
        created_at=datetime.datetime.utcnow(),
        modified_at=datetime.datetime.utcnow())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f"user details added in Database,{db_user}")
    return {
        "username": db_user.username,
        "email": db_user.email
    }

#Roles Creation on DB
def roles_definition(db: Session, role_def: schemas.CreateRoles):
    def_role = models.Role(
    role_id=role_def.role_id,
    role_name=role_def.role_name,)
    db.add(def_role)
    db.commit()
    db.refresh(def_role)
    logger.info(f"New roles defined and added in Database,{def_role}")
    return def_role


#Assigning Roles on DB
def assigning_roles(db:Session,role_assign:schemas.AssignRoles):
    assign_role = models.UserRole(
    user_id=role_assign.user_id,
    role_id=role_assign.role_id,)
    db.add(assign_role)
    db.commit()
    db.refresh(assign_role)
    logger.info(f"Roles assigned to users added in Database,{assign_role}")
    return assign_role