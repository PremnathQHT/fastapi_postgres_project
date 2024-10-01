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
__desc__ = "Organizaition API routes Program of toolsmgt applications"


#Imports
from fastapi import APIRouter,status,HTTPException,Depends,Query,BackgroundTasks
from fastapi.responses import JSONResponse
from typing import List,Optional
from app.schemas import create_Org,Update_Org,Org_list
from app.database import get_db
from app.models import User,role_permissions,user_roles,Organization
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import app.toolsmgtlogger as qtslogger
from app.email_settings.email_sender import mail_engine
from app.utils import encrypt_password
from datetime import datetime


# Initialize logger
logger = qtslogger.logger()


router=APIRouter(prefix="/organization",tags=["Organization"])

@router.get("",response_model=List[Org_list],status_code=status.HTTP_200_OK)
def list_all_organizations(db: Session = Depends(get_db)):
    result=db.query(Organization).all()
    return result

@router.get("/{org_id}")
def get_organization_by_id(org_id:int,db:Session = Depends(get_db)):
    result=db.query(Organization).filter(Organization.org_id==org_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Organization not found")
    return result


@router.post("")
    #New Organization Creation
async def create_organization_user(org_data: create_Org,background_tasks: BackgroundTasks,db: Session = Depends(get_db)):
    """ Organization Account Creation

    Args:
        org_data (create_Org): schemas for create organization
        background_tasks (BackgroundTasks): Background tasks for sending email after organization
        db (Session, optional): _description_. Defaults to Depends(get_db).

    Returns:
        _dict_: Return a dict after organization account creation
    """
    Data_from_user = (
        db.query(
            User.user_name,
            User.org_id,
            User.account_type,
            User.email,
            User.verified,
            User.is_active
        )
        .filter(User.email == org_data.email)  # Filtering by the email
    ).first()
    logger.info(Data_from_user)
    
    #query 2
    existing_org=db.query(Organization).filter(Organization.org_name == org_data.org_name).first()
    #query 3
    manager_role=db.query(role_permissions).filter(role_permissions.role_name == "manager").first()

    # print(Data_from_user.user_name, Data_from_user.org_id,Data_from_user.id,Data_from_user.email,Data_from_user.verified)


    if Data_from_user is None:
        return JSONResponse(status_code=400, content={"detail": "You can't create Organization, valid user doesn't exist"})
    elif Data_from_user.email==org_data.email and Data_from_user.verified==True and Data_from_user.is_active==True:
        return JSONResponse(status_code=400, content={"detail": "User already exists"})
    elif existing_org:
        return JSONResponse(status_code=400, content={"detail": "Organization already exists"})
    elif manager_role is None:
        return JSONResponse(status_code=404, content={"detail": "Manager role not found"})
    else:
        # Create a new organization
        new_org = Organization(
            org_name=org_data.org_name,
            org_description=org_data.org_description,
            location=org_data.location
        )
        db.add(new_org)
        db.flush()

        # Fetch the organization to update
        org_db = db.query(Organization).filter(Organization.org_name == org_data.org_name).first()

        user_result = db.query(User).filter(User.email == org_data.email).first()
        
        # If organization not found, raise 404
        if not org_db:
            raise HTTPException(status_code=404, detail="Organization not found")

        # Update the organization fields
       
        user_result.org_id=org_db.org_id,
        user_result.user_name=org_data.user_name,
        user_result.email=org_data.email,
        user_result.account_type="Account_Manager",
        user_result.password=encrypt_password(org_data.password)  # Ensure the password is hashed
        
        try:
            # Attempt to commit the changes
            db.commit()
        except IntegrityError:
            # Rollback in case of an IntegrityError
            db.rollback()
            # Raise HTTP 409 Conflict error with a custom message
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Organization with the name '{org_data.org_name}' already exists."
            )
        except Exception:
            # Catch any other exceptions and raise HTTP 500 Internal Server Error
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred while updating the organization."
            )   
        result = db.query(User).filter(User.email ==Data_from_user.email).first()
        # Assign the manager role to the user
        new_user_role = user_roles(
            user_id=result.user_id,
            role_id=manager_role.role_id
        )

        db.add(new_user_role)
        result.is_active = True
        db.add(result)
        db.commit()


        # Send email notification to the user about organization creation
        background_tasks.add_task(
        mail_engine.send_org_creation_success_mail,
        receiver_email=org_data.email,
        org_name=org_data.org_name,
        user_name=org_data.user_name
    )

        return {"message":"organization created successfully",
                "Organization":f"{org_data.org_name}",
                "Org_account":f"{org_data.email}",
                "Role":"Manager_role",
            }


@router.put("/{org_id}", response_model=Update_Org, status_code=status.HTTP_200_OK)
async def update_organization_by_id(org_id: int, org_data: Update_Org, db: Session = Depends(get_db)):
    # Fetch the organization to update
    result = db.query(Organization).filter(Organization.org_id == org_id).first()
    
    # If organization not found, raise 404
    if not result:
        raise HTTPException(status_code=404, detail="Organization not found")

    # Update the organization fields
    result.org_name = org_data.org_name
    result.org_description = org_data.org_description
    result.location = org_data.location
    result.modified_at = datetime.utcnow()
    
    try:
        # Attempt to commit the changes
        db.commit()
    except IntegrityError:
        # Rollback in case of an IntegrityError
        db.rollback()
        # Raise HTTP 409 Conflict error with a custom message
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Organization with the name '{org_data.org_name}' already exists."
        )
    except Exception:
        # Catch any other exceptions and raise HTTP 500 Internal Server Error
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while updating the organization."
        )   
    return org_data


@router.delete("/{org_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_organization_by_id(org_id:int, db: Session = Depends(get_db)):
    result=db.query(Organization).filter(Organization.org_id==org_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Organization not found")
    db.delete(result)
    db.commit()
    logger.info(f"Organization {result.org_name} has been deleted successfully")
