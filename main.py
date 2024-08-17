from fastapi import FastAPI, HTTPException, Depends,status
import schemas
import models
from database import engine,get_db
from sqlalchemy.orm import Session
import datetime
import uvicorn
import crud
from logs.qtoolslogger import logger


app = FastAPI()

# This line will create all tables and columns in Postgres
models.Base.metadata.create_all(bind=engine)


#Create user API
@app.post("/create-user",status_code=status.HTTP_200_OK)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    creation=crud.create_users(user=user,db=db)
    logger.info(f"user created{creation}")
    return f"user created successfully,{creation}"

#Create NEW Roles API
@app.post("/define-roles",status_code=status.HTTP_200_OK)
async def roledefinition(role_definition: schemas.CreateRoles, db: Session = Depends(get_db)):
  return crud.roles_definition(role_def=role_definition,db=db)

#Assign roles to users API
@app.put("/assign-roles",status_code=status.HTTP_200_OK)
async def roledefinition(roles_assign: schemas.AssignRoles, db: Session = Depends(get_db)):
   return crud.assigning_roles(role_assign=roles_assign,db=db)
 

if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, log_level="info")