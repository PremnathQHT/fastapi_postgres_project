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
__desc__ = "Administrator API routes Program of toolsmgt applications"


#Imports
#Imports
from fastapi import APIRouter,Depends
from app.database import get_db
from app.models import role_permissions
from sqlalchemy.orm import Session
import app.toolsmgtlogger as qtslogger
from app.schemas import Define_role

# Initialize logger
logger = qtslogger.logger()




router=APIRouter(
                 prefix="/Administrator/create_roles",
                 tags=["create_roles"])



@router.post('')
async def role_creation(roles_data:Define_role,db: Session = Depends(get_db)):
    # Create new roles instance 
    new_role = role_permissions(**roles_data.dict())
    db.add(new_role)
    db.commit()
    logger.info(f"New roles created with this role_data{roles_data}")
    return roles_data

