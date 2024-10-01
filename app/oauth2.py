from jose import JWTError,jwt
from datetime import datetime, timedelta
from app.config import SECRET_KEY
from app.schemas import TokenData
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
import app.toolsmgtlogger as qtslogger

logger = qtslogger.logger()

oauth2_scheme =OAuth2PasswordBearer(tokenUrl='login')

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
ACCESS_TOKEN_EXPIRE_DAYS=1



role_access_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Role access restricted"
    )


def create_access_token(data: dict):
    to_encode = data.copy()
    expire_time = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire_time})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict):
    to_encode = data.copy()
    # Refresh token expiration time (e.g., 30 days)
    expire_time = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire_time})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logger.info(payload)
        user_id: int = payload.get("user_id")
        token_type: str = payload.get("token_type")
        print("token type",token_type)
        print(type(token_type))
        user_id: int = payload.get("user_id")
        user_role: str = payload.get("user_role")
        org_id: int = payload.get("org_id")

        if user_id is None or token_type=="refresh_token":
            raise credentials_exception
        token_data =TokenData(id=user_id,org_id=org_id,user_id=user_id,user_role=user_role)
        print("Token_data",token_data)
    except JWTError:
        raise credentials_exception
    print("Token_data",token_data)
    return token_data




def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    print("JWT Ra",token, credentials_exception)
    return verify_access_token(token, credentials_exception)





# Function to verify refresh token
def verify_refresh_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        logger.info(payload)
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token",
                headers={"WWW-Authenticate": "Bearer"}
            )
        token_data = TokenData(id=user_id)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
            headers={"WWW-Authenticate": "Bearer"}
        )
    return token_data
