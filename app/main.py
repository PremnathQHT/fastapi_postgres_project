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
__desc__ = "Main Program of toolsmgt applications"


#Import

from fastapi import FastAPI,Response,HTTPException,status
from fastapi.middleware.cors import CORSMiddleware
#import all routers
from app.routers import email_verification, users,organization,projects,services,roles_and_permissions,administrator
from app.auth import authentication
import app.models as models
from app.database import engine
# import uvicorn
import app.toolsmgtlogger as qtslogger

# Create logger object
logger = qtslogger.logger()



app = FastAPI(
    title="toolsmgt",
    description="An application to manage organizations, users, projects, and service allocation.",
    version="1.0.0",
    swagger_ui_parameters={"syntaxHighlight": True}
)

origins=["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# This line will create all tables and columns in Postgres
#This won't need anymore after the alembic
models.Base.metadata.create_all(bind=engine)

#include Routers
app.include_router(authentication.router)
app.include_router(email_verification.router)
app.include_router(organization.router)
app.include_router(users.router)
app.include_router(projects.router)
app.include_router(administrator.router)
# app.include_router(services.router)
# app.include_router(roles_and_permissions.router)