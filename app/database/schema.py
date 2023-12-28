from fastapi import Query
from typing import Union, Optional
from pydantic import BaseModel, EmailStr, validator


class RegisterUser(BaseModel):
    username:str
    email: str
    password:str
    
    class Config:
        orm_mode =True
        schema_extra = {
            "example" : {
                "username":"JohnDoe",
                "email": "johndoe@gmail.com",
                "password":"password",
                "is_staff": False,
                "is_active": True
            }
        }
        
class LoginUser(BaseModel):
    email: str
    password:str
    
class ShowUser(BaseModel):
    id: int
 
class User(BaseModel):
    email: Union[str, None] 
    password: Union[str, None] 
 
  
class Order(BaseModel):
    # name: str
    quantity: int
    order_size: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: str
    id: int