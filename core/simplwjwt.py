import uvicorn
from pydantic import BaseModel
from fastapi import FastAPI
import jwt
from fastapi.encoders import jsonable_encoder

app =FastAPI()




#Dummy user

dummy_user={
    "username":"premnath",
    "password":"prem@123"
}

class Loginclass(BaseModel):
    username: str
    password: str

@app.get('/')
def hello():
    return {"hello":"world"}

@app.post('/login')
async def login(login_item:Loginclass):
    data=jsonable_encoder(login_item)
    if dummy_user["username"]==data["username"] and dummy_user["password"]==data["password"]:
        encoded_JWT=jwt.encode(data,SECRET_KEY,algorithm=ALGORITHM)
        return {"token":encoded_JWT}
    else:
        return {"message":"login_failed"}






if __name__=="__main__":
    uvicorn.run("simplwjwt:app",host="localhost",port=8000)