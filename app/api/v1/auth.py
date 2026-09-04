from fastapi import APIRouter, Depends, status
from app.auth.schema import UserSchema, UserResponseSchema, LoginSchema
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.auth.repository import register_user, login_user

router=APIRouter(prefix="/auth",tags=["auth"])

@router.post("/register",response_model=UserResponseSchema,status_code=status.HTTP_201_CREATED)
def register(body:UserSchema, db:Session=Depends(get_db)):
    return register_user(body,db)

@router.post("/login", status_code=status.HTTP_200_OK)
def login(data:LoginSchema, db:Session=Depends(get_db)):
    return login_user(data,db)