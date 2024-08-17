from fastapi import FastAPI, HTTPException, Depends
import schemas
from typing import List, Annotated
import models 
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import datetime
import uvicorn


app = FastAPI()

# This line will create all tables and columns in Postgres
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




@app.post("/create-user")
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(
        username=user.username,
        email=user.email,
        hash_password=user.hash_password,
        created_at=datetime.datetime.utcnow(),
        modified_at=datetime.datetime.utcnow()
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return{
        "username": db_user.username,
        "email": db_user.email
    }

@app.post("/define-roles")
async def roledefinition(role_definition: schemas.CreateRoles, db: Session = Depends(get_db)):
    def_role = models.Role(
        role_id=role_definition.role_id,
        role_name=role_definition.role_name,)
    db.add(def_role)
    db.commit()
    db.refresh(def_role)
    return def_role

@app.put("/assign-roles")
async def roledefinition(roles_assign: schemas.AssignRoles, db: Session = Depends(get_db)):
    assign_role = models.UserRole(
        user_id=roles_assign.user_id,
        role_id=roles_assign.role_id,)
    db.add(assign_role)
    db.commit()
    db.refresh(assign_role)
    return assign_role


if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8000, log_level="info")