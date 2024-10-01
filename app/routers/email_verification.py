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
from fastapi import APIRouter,status,HTTPException,Depends,BackgroundTasks
from fastapi.responses import JSONResponse
from app.schemas import Validate_Mail,Verify_Mail
from app.auth.otp import generate_otp,verify_otp
from app.email_settings.email_sender import mail_engine
import app.toolsmgtlogger as qtslogger
import app.models as DBmodel
from sqlalchemy.exc import IntegrityError,SQLAlchemyError
from app.database import engine,get_db
from sqlalchemy.orm import Session
from sqlalchemy import select
# Initialize logger
logger = qtslogger.logger()



router=APIRouter(prefix="/main",tags=["Email-Validation"])

################################################################




@router.post('/validate-email/', status_code=status.HTTP_200_OK)
async def Send_OTP(email_data: Validate_Mail,background_tasks: BackgroundTasks,db: Session = Depends(get_db)):
    """
    Validate Email API Endpoint
    """
    try:
        # Check if email already exists
        existing_user_mail = db.query(DBmodel.User).filter(DBmodel.User.email == email_data.email,DBmodel.User.verified==True).first()
        
        if existing_user_mail:
            # Email already exists, return an HTTP 400 Bad Request error
           return JSONResponse(status_code=400, content={"detail": "User Email already exists"})
        else:
            logger.info(f"Getting the mail from user for validation {email_data.email}")
            otp = generate_otp(email_data.email)
            logger.info(f"OTP generated successfully {otp}")
            # Uncomment the following line once mail_engine is properly configured
            background_tasks.add_task(mail_engine.send_otp_email,receiver_email=email_data.email, otp=otp)
            logger.info(f"OTP sent successfully to mail {email_data.email}")
            return {"message": f"Check your mail for OTP {otp}"}
    
    except SQLAlchemyError as e:
        logger.error(f"Database error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while accessing the database"
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )

@router.post('/verify-email/',status_code=status.HTTP_200_OK)
async def Verify_OTP(user_data:Verify_Mail, background_tasks:BackgroundTasks,db:Session = Depends(get_db)):
    """
    Verify Email API Endpoint
    """
    # Check if email already exists
    existing_user_mail = db.query(DBmodel.User).filter(DBmodel.User.email == user_data.email,DBmodel.User.verified==True).first()
    print(existing_user_mail)
    logger.info("Verifying email")

    if existing_user_mail:
        # Email already exists, return an HTTP 400 Bad Request error
       return JSONResponse(status_code=400, content={"detail": "User Email already exists"})
    
    logger.info(f"User data:{user_data}")
    result=verify_otp(email=user_data.email,otp=user_data.otp)
    if result=="success":
        
            # make an entry in the database for this email verified.

            verified_email = DBmodel.User(email=user_data.email,verified=True)
            db.add(verified_email)
            db.commit()
            db.refresh(verified_email)
            logger.info(f"Email Id has verified successfully and added entry in db {user_data.email}")
            background_tasks.add_task(mail_engine.send_verification_success_email,receiver_email=user_data.email)
            logger.info(f"Verification Email sent Successfully to Mail {user_data.email}")

            return JSONResponse(status_code=200, content={"Message": "OTP verified successfully"})
    else:
           return JSONResponse(status_code=400, content={"Message":f"{result}"})


