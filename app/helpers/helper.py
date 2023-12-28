from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from starlette import status
import os
from datetime import datetime, timedelta
from typing import Union
from passlib.context import CryptContext
from jose import JWTError
import jwt as pyjwt
import database.schema as schema
from dotenv import load_dotenv

load_dotenv()
oauth2_scheme = HTTPBearer()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class PassWord_Helper:
    def hash_password(plain_password: str):
        return pwd_context.hash(plain_password)


    def verify_password(plain_password: str, hashed_password: str):
        return pwd_context.verify(plain_password, hashed_password)

    
class JWT_Helper:
    def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=60)
        to_encode.update({"exp": expire})
        encoded_jwt = pyjwt.encode(to_encode, os.environ.get('SECRET_KEY'), algorithm=os.environ.get('ALGORITHM'))
        return encoded_jwt


    def verify_token(credentials, credentials_exception):
        try:
            token = credentials.credentials
            payload = pyjwt.decode(token, os.environ.get('SECRET_KEY'), algorithms=[os.environ.get('ALGORITHM')])
            user = payload.get('sub')
            if user is None:
                raise credentials_exception
            return schema.TokenData(id=user['id'], email=user['email'])
        except JWTError:
            raise credentials_exception


class User_Helper:
    async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)):
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        return JWT_Helper.verify_token(credentials, credentials_exception)
       