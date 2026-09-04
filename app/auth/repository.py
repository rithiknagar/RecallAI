from app.auth.schema import UserSchema, LoginSchema
from sqlalchemy.orm import Session
from app.vectorstore.models import UserModel as User
from fastapi import HTTPException
from app.auth.utils import get_hash_password, verify_password, create_access_token

def register_user(body:UserSchema,db:Session):

    user=db.query(User).filter(User.email==body.email).first()
    if user:
        raise HTTPException(status_code=400,detail="User with this email already exists")

    hash_password=get_hash_password(body.password)

    new_user=User(
        email=body.email,
        password_hash=hash_password
    )

    db.add(new_user)
    db.flush()
    db.refresh(new_user)

    return new_user

def login_user(body:LoginSchema, db:Session):
    try:
        user=db.query(User).filter(User.email==body.email).first()
        
        if not user:
            raise HTTPException(status_code=401, detail="Incorrect credentials")
    
        verify_pass=verify_password(body.password, user.password_hash)
    
        if not verify_pass:
            raise HTTPException(status_code=401, detail="Incorrect credentials")
    
        payload={
            "id":str(user.id),
            "email":user.email,
        }
        token=create_access_token(payload)
        print(token)
    
        return token
    
    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))

    
