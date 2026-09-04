from pydantic import BaseModel, EmailStr, ConfigDict
from uuid import UUID

class UserSchema(BaseModel):
    email: EmailStr
    password:str

class UserResponseSchema(BaseModel):
    id:UUID
    email: EmailStr

    model_config=ConfigDict(from_attributes=True)

class LoginSchema(BaseModel):
    email:EmailStr
    password:str