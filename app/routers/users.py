"""
Private License (toolsmgt)

This script is privately licensed and confidential. It is not intended for
public distribution or use without explicit permission from the owner.

All rights reserved (c) 2024.
"""

__author__ = "Premnath Palanichamy"
__copyright__ = "Copyright 2024, toolsmgt"
__license__ = "Refer Terms and Conditions"
__version__ = "1.0"
__maintainer__ = "Premnath"
__email__ = "premnath@quehive.com"
__status__ = "Development"
__desc__ = "User API routes Program of toolsmgt applications"


#Imports
from fastapi import APIRouter,status,Depends,HTTPException
from typing import List,Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import app.toolsmgtlogger as qtslogger
from app.models import User
from app.database import get_db
from app.schemas import UserCreate,ListUsers,Res_user
from app.utils import encrypt_password
from app.oauth2 import get_current_user
from datetime import datetime
from app.role_based_access import check_access

# Initialize logger
logger = qtslogger.logger()




router=APIRouter(
                #  prefix="/user-details",
                 tags=["Users"])



@router.get("/list-users", response_model=List[ListUsers], status_code=status.HTTP_200_OK)
def list_all_users(db: Session = Depends(get_db),current_user: dict = Depends(get_current_user)):
    print(current_user)
    data=None
    check_access(current_user,data)

    # Query all users from the database
    result = db.query(User).all()
    # Return the query result
    return result

@router.get("/users/{org_id}",response_model=List[ListUsers])
def list_users_based_on_org(org_id:int, db: Session = Depends(get_db),id:int=Depends(get_current_user)):
    # Query users based on organization id from the database
    result = db.query(User).filter(User.org_id == org_id).all()
    # Return the query result
    return result

@router.post("/user/{org_id}", response_model=Res_user, status_code=status.HTTP_201_CREATED)
def create_user_based_on_org(org_id: int, user_data: UserCreate, db: Session = Depends(get_db),id:int=Depends(get_current_user)):
    # Create a new user in the specified organization from the database
    new_user = User(
        org_id=org_id,
        user_name=user_data.user_name,
        password=encrypt_password(user_data.password),
        email=user_data.email
    )
    
    try:
        # Add the new user to the session
        db.add(new_user)
        # Attempt to commit the changes
        db.commit()
        # Refresh the instance to get the updated state from the database
        db.refresh(new_user)
        logger.info(f"User created successfully: {new_user}")
        return new_user
    except IntegrityError:
        # Rollback in case of an IntegrityError
        db.rollback()
        # Raise HTTP 409 Conflict error with a custom message
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with the email '{user_data.email}' already exists."
        )
    except Exception:
        # Rollback and raise HTTP 500 Internal Server Error for any other exceptions
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while creating the user."
        )


@router.put("/user/{org_id}/{user_id}", response_model=Res_user, status_code=status.HTTP_200_OK)
def update_user(org_id: int, user_id: int, user_data: UserCreate, db: Session = Depends(get_db),id:int=Depends(get_current_user)):
    """
    Update a user's information in the specified organization from the database.
    """
    # Query the user from the database
    user = db.query(User).filter(User.org_id == org_id, User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")

    # Update the user's information
    user.user_name = user_data.user_name
    user.email = user_data.email
    user.password = encrypt_password(user_data.password)
    user.modified_at = datetime.utcnow()

    # Commit the changes
    db.commit()
    db.refresh(user)
    logger.info(f"User updated successfully: {user}")

    # Return the updated user with correct fields
    return user



@router.delete("/user/{org_id}/{user_id}",status_code=status.HTTP_204_NO_CONTENT)

def delete_user(org_id: int, user_id: int, db: Session = Depends(get_db),id:int=Depends(get_current_user)):
    """
    Delete a user from the specified organization from the database.
    """
    # Query the user from the database
    user = db.query(User).filter(User.org_id == org_id, User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    
    # Delete the user
    db.delete(user)
    db.commit()
    logger.info(f"User deleted successfully: {user}")
    return {"message": "User deleted successfully."}