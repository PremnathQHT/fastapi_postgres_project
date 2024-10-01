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
from pydantic import BaseModel,EmailStr
from typing import Optional
from datetime import datetime


#create Organization account
class create_Org(BaseModel):
    org_name: str
    org_description: str
    location: Optional[str] = None
    user_name:str
    email: EmailStr
    password: str

    class Config:
        from_attributes = True  # Enable ORM mode
        


class Update_Org(BaseModel):
    org_name: str
    org_description: str
    location: Optional[str] = None

    class Config:
        from_attributes = True  # Enable ORM mode

########################## Validation Mail Model ##################################

class Validate_Mail(BaseModel):
    email: EmailStr

class Verify_Mail(Validate_Mail):
    otp:int



class Define_role(BaseModel):
    role_name: str
    role_description: str



class Userlogin(BaseModel):
    email: EmailStr
    password: str


class UserCreate(BaseModel):
    user_name: str
    email: EmailStr
    password: str
   
class ListUsers(BaseModel):
    user_name: str
    user_id:int
    email: EmailStr
    org_id: int
    account_type: str
    created_at: Optional[datetime]
    modified_at: Optional[datetime]

    class Config:
        from_attributes = True




class Refresh_token(BaseModel):
    access_token: str
    token_type: str

    class Config:
        from_attributes = True

class Token(Refresh_token):
    refresh_token:str
    class Config:
        from_attributes = True


class TokenData(BaseModel):
    id:Optional[int]=None
    org_id: Optional[int]=None
    user_role:Optional[str] =None
    class Config:
        from_attributes = True



class Org_list(BaseModel):
    org_id: int
    org_name: str
    org_description: str
    location: Optional[str] = None
    created_at: datetime
    modified_at: datetime

    class Config:
        from_attributes = True



class Res_user(BaseModel):
    user_id: int
    org_id:int
    user_name: str
    email: EmailStr
    

    class Config:
        from_attributes = True  



class ListProjects(BaseModel):
    project_id: int
    project_name:str
    org_id: int
    project_description: str
    created_at: Optional[datetime]
    modified_at: Optional[datetime]

    class Config:
        from_attributes = True     

class CreateProjects(BaseModel):
    project_name:str
    project_description: str

    class Config:
        from_attributes = True