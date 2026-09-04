from pwdlib import PasswordHash
import jwt
from typing import Dict
from app.core.config import settings
from datetime import datetime,timedelta,timezone
from fastapi import Request,Depends, HTTPException
from app.core.database import get_db
from sqlalchemy.orm import Session
from app.vectorstore.models import UserModel as User
from jwt.exceptions import InvalidTokenError


passowrd_hash=PasswordHash.recommended()

def get_hash_password(password:str):
    return passowrd_hash.hash(password)

def verify_password(plain_password,hash_password):
    return passowrd_hash.verify(plain_password,hash_password)

def create_access_token(payload:Dict):
    expiry_time=datetime.now(timezone.utc)+timedelta(minutes=settings.EXP_TIME)
    payload["exp"]=expiry_time
    token= jwt.encode(payload,settings.SECRET_KEY,settings.ALGORITHM)
    return token

from fastapi.security import APIKeyHeader
authorization_header = APIKeyHeader(name="Authorization", auto_error=False)

# def verify_token(request : Request, db:Session=Depends(get_db)):
def verify_token(token: str | None = Depends(authorization_header), db:Session=Depends(get_db)):

    try:    
        # token=request.headers.get("Authorization")
        print(token)
        if not token:
            raise HTTPException(status_code=401,detail="You are unathorized")
        
        token=token.split(" ")[-1]

        is_verified=jwt.decode(token,settings.SECRET_KEY,settings.ALGORITHM)

        user=db.query(User).filter(User.id==is_verified.get("id")).first()

        print(user)

        if not user:
            raise HTTPException(status_code=401,detail="You are unauthorize")
        
        return user
    
    except InvalidTokenError:
        raise HTTPException(status_code=401,detail="You are unauthorize")
    
    