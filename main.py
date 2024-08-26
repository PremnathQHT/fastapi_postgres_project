from fastapi import FastAPI, HTTPException, Depends,status
import schemas
import jwt
from fastapi.encoders import jsonable_encoder
import models
from core.otp_mechanism import generate_otp,verify_otp
from core.email_sender import send_otp_email,send_welcome_email
from database import engine,get_db
from sqlalchemy.orm import Session
from sqlalchemy import select
import datetime
import uvicorn
import crud
from program_logs.qtoolslogger import logger


app = FastAPI()


SECRET_KEY="prem@123456"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=800

# This line will create all tables and columns in Postgres
models.Base.metadata.create_all(bind=engine)


@app.get("/validate-mail/{email_id}",status_code=status.HTTP_200_OK)
async def validate_user_mail(email_id,db:Session=Depends(get_db)):
   #is already mailID exist in DB ?
    existing_user_mail = db.query(models.User).filter(models.User.email == email_id).first()
    print(existing_user_mail)
    if existing_user_mail:
        # Username already exists
        return {"error": "Username already exists"}
    else:
        otp=generate_otp(email=email_id)
        send_otp_email(receiver_email=email_id,otp=otp)
        return {"message":"OTP has been send to User Mail ID","otp":otp}

        
@app.post('/verify_OTP',status_code=status.HTTP_200_OK)
async def verify_update(email_id:str,otp:int,db:Session=Depends(get_db)):
    verification=verify_otp(email=email_id,otp=otp)
    if verification=="success":
        crud.createtemp_user(email=email_id,db=db)
        return{"message":"OTP Verified Successfully"}
    else:
        return verification
        
        

#Create user API
@app.post("/create-user",status_code=status.HTTP_200_OK)
async def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # stmt = select(models.User).where(models.User.email == user.email)
    # is_valid = db.execute(stmt).scalar() 
    # print(is_valid.verified)
    # if is_valid.verified==False:
    #     return {"message":"Your Mail ID is not verified"}
    
    # else:
    creation=crud.update_user_by_email(user_update=user,db=db)
    logger.info(f"user created{creation}")
    send_welcome_email(receiver_email=user.email,user_name=user.username)
    return {"message": "User created successfully", "user": creation}



#Create NEW Roles API
@app.post("/define-roles",status_code=status.HTTP_200_OK)
async def roledefinition(role_definition: schemas.CreateRoles, db: Session = Depends(get_db)):
  return crud.roles_definition(role_def=role_definition,db=db)



#Assign roles to users API
@app.put("/assign-roles",status_code=status.HTTP_200_OK)
async def roledefinition(roles_assign: schemas.AssignRoles, db: Session = Depends(get_db)):
   return crud.assigning_roles(role_assign=roles_assign,db=db)
 


# @app.post('/login')
# async def login(login_item:schemas.Loginclass):
#     data=jsonable_encoder(login_item,db: Session = Depends(get_db))
#     login_check = select(models.User).where(models.User.email == login_item.email)
#     is_user_exists = db.execute(login_check).scalar() 
#     if dummy_user["username"]==data["username"] and dummy_user["password"]==data["password"]:
#         encoded_JWT=jwt.encode(data,SECRET_KEY,algorithm=ALGORITHM)
#         return {"message":"Login Successful","token":encoded_JWT}
#     else:
#         return {"message":"login_failed"}



if __name__ == "__main__":
    uvicorn.run("main:app", host="localhost", port=8002, log_level="info")