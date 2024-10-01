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
__desc__ = "DBmodel Program of toolsmgt applications"


#Import
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import datetime

################################################################
# Define the User model

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    org_id = Column(Integer, ForeignKey('organizations.org_id', ondelete="CASCADE"), index=True)
    user_name = Column(String, index=True,default=None)
    password = Column(String)
    email = Column(String, unique=True, nullable=False)
    account_type = Column(String, index=True, default="viewer")
    verified = Column(Boolean, default=False)
    is_active= Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # Automatically set in UTC
    modified_at = Column(DateTime(timezone=True),default=func.now(),onupdate=func.now())

    # Define the relationship back to Organization
    organization = relationship("Organization", back_populates="users")

       # Define relationship to user_roles with cascade options
    roles = relationship("user_roles", back_populates="user", cascade="all, delete-orphan")

    projects = relationship("Project_users", back_populates="user", cascade="all, delete-orphan")


################################################################
# Define the organization

class Organization(Base):
    __tablename__ = "organizations"

    org_id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    org_name = Column(String, unique=True, index=True)
    org_description = Column(String, index=True)
    location = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    modified_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())


    # Define the one-to-many relationship with User
    users = relationship("User", back_populates="organization", cascade="all, delete-orphan")

    # users = relationship("User", back_populates="org")
    # projects = relationship("Project", back_populates="org")
    # services = relationship("Service", back_populates="org")

################################################################
# Define role and permissions

class role_permissions(Base):
    __tablename__ = "role_permissions"
    role_id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    role_name = Column(String, index=True)
    role_description=Column(String, index=True)
                                 
################################################################
# Define User_roles

class user_roles(Base):
    __tablename__ = "user_roles"
    
    # Add a primary key column
    id = Column(Integer, primary_key=True, index=True,autoincrement=True)

    role_id = Column(Integer, ForeignKey("role_permissions.role_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    # Define the relationship back to User
    user = relationship("User", back_populates="roles")


################################################################


# Define Projects

class Project(Base):
    __tablename__ = "projects"

    project_id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    org_id = Column(Integer, ForeignKey("organizations.org_id", ondelete="CASCADE"), nullable=False)
    project_name = Column(String, index=True)
    project_description = Column(String, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # Automatically set in UTC
    modified_at = Column(DateTime(timezone=True), onupdate=func.now()) 

################################################################

# Define Project_users

class Project_users(Base):
    __tablename__ = "project_users"
    # Add a primary key column
    id = Column(Integer, primary_key=True, index=True,autoincrement=True)
    project_id = Column(Integer, ForeignKey("projects.project_id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

     # Define the relationship back to User
    user = relationship("User", back_populates="projects")