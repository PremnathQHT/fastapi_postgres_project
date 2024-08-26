from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime



class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

    class Config:
        orm_mode = True

class CreateRoles(BaseModel):
    role_id: int
    role_name: str        

    class Config:
        orm_mode=True

class AssignRoles(BaseModel):
    user_id: int
    role_id: int      

    class Config:
        orm_mode=True


# Request model for OTP validation
class OTPRequest(BaseModel):
    mail_id:str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None

#User Login
class Loginclass(BaseModel):
    username: str
    password: str    