import schemas
import models
import datetime
from sqlalchemy.exc import IntegrityError
from core.password_hashing import encrypt_data
from sqlalchemy.orm import Session
from program_logs.qtoolslogger import logger


#User Creation on DB
def create_users(db: Session, user: schemas.UserCreate):

    password=(user.password)
    db_user = models.User(username=user.username, email=user.email,               
        hash_password=encrypt_data(password),
        created_at=datetime.datetime.utcnow(),
        modified_at=datetime.datetime.utcnow())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f"user details added in Database,{db_user}")
    # logger.info(decrypt_data(db_user.hash_password))
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



def createtemp_user(email: str, db: Session):
    # Create a new user instance
    new_user = models.User(
        username="",  # Assuming username is empty for this creation
        email=email,
        hash_password="",  # Assuming password is empty for this creation
        verified=True,  # Set the verified status to True
    )
    
    try:
        # Add the new user to the session and commit
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        logger.info(f"User with email {email} created successfully: {new_user}")
    
    except IntegrityError:
        # Handle unique constraint violations (e.g., if email already exists)
        db.rollback()
        logger.warning(f"User with email {email} already exists.")
    
    except Exception as e:
        # Handle other exceptions
        db.rollback()
        logger.error(f"An error occurred: {e}")





def update_user_by_email(db: Session,user_update: schemas.UserUpdate):
    # Get the user from the database by email
    db_user = db.query(models.User).filter(models.User.email == user_update.email).first()

    if not db_user:
        return {"detail":"User not found"}

    # Update the user details
    if user_update.username:
        db_user.username = user_update.username
    if user_update.password:
        db_user.hash_password = encrypt_data(user_update.password)

    # Update the modified_at timestamp
    db_user.modified_at = datetime.datetime.utcnow()

    # Commit the changes
    db.commit()
    db.refresh(db_user)

    logger.info(f"User details updated in the Database for email {db_user.email}, {db_user}")

    return {
        "username": db_user.username,
        "email": db_user.email
    }        