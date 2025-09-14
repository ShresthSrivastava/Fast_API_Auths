from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer, HTTPBasic, HTTPBasicCredentials
from jose import jwt
from pydantic import BaseModel
from typing import List, Dict, Any, Annotated
import pandas as pd
import logging
from datetime import datetime, timedelta
import mysql.connector

app =FastAPI()

def establish_Sql_Connection():
    try:
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="admin",
        database="user"
        )
        if mydb.is_connected():
            return mydb
    except Exception as e:
        print("SQL connector error: "+e)

def get_sql_Data(username:str) -> Dict:
    mysqldb = establish_Sql_Connection()
    cursor = mysqldb.cursor()
    cursor.execute("Select username,password from user where username = '"+username+"'")
    result = cursor.fetchall()
    result = {"username": result[0][0],"password": result[0][1]}
    return result

class Data(BaseModel):
    data: List[Dict[str,Any]]


# def verify_Cred(credentials: Annotated[HTTPBasicCredentials,Depends(security)]) -> bool:
#     result = get_sql_Data(credentials.username)
#     if result["username"] == credentials.username and result["password"] == credentials.password:
#         return True

security = HTTPBasic()
@app.post("/data")
async def data_manipulation(data:Data,credentials: Annotated[HTTPBasicCredentials,Depends(security)]):
    result = get_sql_Data(credentials.username)
    if result["username"] == credentials.username and result["password"] == credentials.password:
        return data.data