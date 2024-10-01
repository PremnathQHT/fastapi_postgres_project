
#import
from fastapi import APIRouter, Depends, status,HTTPException,Response,Header
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import Token,Userlogin
from app.models import User,Organization,user_roles,role_permissions
from app.utils import verify_password
import app.toolsmgtlogger as qtslogger
import app.oauth2 as oauth2

# Initialize logger
logger = qtslogger.logger()

router =APIRouter(tags=['Authentication'])

@router.post('/login',response_model=Token)
def login(user_credentials:Userlogin,db: Session=Depends(get_db)):
    user = (
        db.query(User, Organization, user_roles, role_permissions)
        .join(Organization, User.org_id == Organization.org_id)
        .join(user_roles, User.user_id == user_roles.user_id)
        .join(role_permissions, user_roles.role_id == role_permissions.role_id)
        .filter(User.email == user_credentials.email)
        .first()
    )


    logger.info(f"User_credentials:{user_credentials}")
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid Credentials')
    
    if not verify_password(plain_password=user_credentials.password,hashed_password=user[0].password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid Credentials')
    
    #return token

    access_token=oauth2.create_access_token(data={"user_id":user[0].user_id,"org_id":user[0].org_id,"user_name":user[0].user_name,"organization_name":user[1].org_name,"user_role":user[3].role_name})
    refresh_token=oauth2.create_refresh_token(data={"user_id":user[0].user_id,"org_id":user[0].org_id,"user_name":user[0].user_name,"organization_name":user[1].org_name,"user_role":user[3].role_name,"token_type":"refresh_token"})
    logger.info(user)
    return {"access_token": access_token,"refresh_token": refresh_token,"token_type": "bearer"}



# Endpoint to refresh access token
@router.post("/refresh_token", status_code=status.HTTP_200_OK)
async def refresh_token_func(refresh_token: str = Header(), db: Session = Depends(get_db)):
    # Verify and decode refresh token
    token_data = oauth2.verify_refresh_token(refresh_token)
    
    # Create a new access token
    access_token = oauth2.create_access_token(data={"user_id": token_data.id, "token_type": "access_token"})
    
    return {"access_token": access_token, "token_type": "bearer"}