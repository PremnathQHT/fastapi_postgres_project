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
from datetime import datetime
from typing import List
from sqlalchemy.orm import Session 
import app.toolsmgtlogger as qtslogger
from app.models import Project,Project_users
from app.database import get_db
from app.schemas import ListProjects,CreateProjects
from app.oauth2 import get_current_user


# Initialize logger
logger = qtslogger.logger()




router=APIRouter(
                #  prefix="/projects-details",
                 tags=["Projects"])

# @router.get('/list-projects')
# def list_projects():
#     """
#     List all projects API Endpoint
#     """
#     return {"message": "List of projects"}



@router.get("/list-projects", response_model=List[ListProjects], status_code=status.HTTP_200_OK)
def list_all_users(db: Session = Depends(get_db),id:int=Depends(get_current_user)):
    # Query all users from the database
    result = db.query(Project).all()
    # Return the query result
    return result

@router.get("/projects/{org_id}")
def get_project(org_id:int,db:Session=Depends(get_db),id:int=Depends(get_current_user)):
    """
    Get a project by ID API Endpoint
    """
    project = db.query(Project).filter(Project.org_id == org_id).all()
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project

@router.post("/project/{org_id}", response_model=ListProjects, status_code=status.HTTP_201_CREATED)
def create_project(org_id:int,project: CreateProjects, db: Session = Depends(get_db),id:int=Depends(get_current_user)):
    """
    Create a new project API Endpoint
    """
    new_project = Project(org_id=org_id,project_name=project.project_name,
                    project_description=project.project_description)
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    logger.info(f"User created successfully {new_project.project_name}")
    return new_project

@router.put("/project/{org_id}/{project_id}", response_model=ListProjects, status_code=status.HTTP_200_OK)
def update_project(org_id:int, project_id:int, project: CreateProjects, db: Session = Depends(get_db),id:int=Depends(get_current_user)):
    """
    Update an existing project API Endpoint
    """
    project_to_update = db.query(Project).filter(Project.org_id == org_id, Project.project_id == project_id).first()
    if not project_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    
    project_to_update.project_name = project.project_name
    project_to_update.project_description = project.project_description
    project_to_update.modified_at = datetime.utcnow()
    db.commit()
    db.refresh(project_to_update)
    logger.info(f"Project updated successfully: {project_to_update.project_name}")
    return project_to_update

@router.delete("/project/{org_id}/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(org_id:int, project_id:int, db: Session = Depends(get_db),id:int=Depends(get_current_user)):
    """
    Delete a project API Endpoint
    """
    project_to_delete = db.query(Project).filter(Project.org_id == org_id, Project.project_id == project_id).first()
    if not project_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    
    db.delete(project_to_delete)
    db.commit()
    logger.info(f"Project deleted successfully: {project_to_delete.project_name}")
    return {"message": "Project deleted successfully."}


@router.get("/project/{org_id}/{project_id}")
def assign_project_to_user(org_id:int, project_id:int,user_id:int,db:Session= Depends(get_db),id:int=Depends(get_current_user)):
    """
    Assign project to a user API Endpoint
    """
    project_user = Project_users(project_id=project_id, user_id=user_id)
    db.add(project_user)
    db.commit()
    db.refresh(project_user)
    logger.info(f"Project assigned to user successfully: {project_user.project_id}")
    return project_user