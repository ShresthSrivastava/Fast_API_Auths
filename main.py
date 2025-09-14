from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt
from pydantic import BaseModel
from typing import List, Dict, Any
import pandas as pd
import logging
from datetime import datetime, timedelta

log = logging.basicConfig(level=logging.INFO)

app = FastAPI()

SECRET_KEY = "A123"
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

fake_user = {
    "username": "shresth",
    "password": "fastapi123"
}

def verify_Token(Token:str):
    payload = jwt.decode(Token,SECRET_KEY,algorithms=[ALGORITHM])
    return payload.get("sub")

@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if form_data.username != fake_user["username"] or form_data.password != fake_user["password"]:
        raise HTTPException(status_code=401,detail="Invalid Credential")
    
    token_data = {
        "sub":form_data.username,
        "exp":datetime.now() + timedelta(minutes=30)
    }

    token = jwt.encode(claims=token_data,key=SECRET_KEY,algorithm=ALGORITHM)
    print(token)
    return {"access_Token":token,"token_type":"Bearer"}

################################
@app.get("/")
def excel_get():
    return {"Welcome"}
################################



################################
class Struct(BaseModel):
    Data: List[Dict[str, Any]]

@app.post("/excel/")
def excel_post(data: Struct, Token:str = Depends(oauth2_scheme)):
    user = verify_Token(Token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    df = pd.DataFrame(data.Data)
    logging.info(len(df))
    return df.to_dict(orient="records")
#################################