from fastapi import Depends
from sqlalchemy.orm import Session
from starlette import status
import database.models as models, database.schema as schema
from database.database import get_db
from helpers.helper import (PassWord_Helper, JWT_Helper)



def sign_up(request: schema.RegisterUser, response, db:Session):
    db_email = db.query(models.User).filter(models.User.email == request.email).first()
    
    if db_email:
        response.status_code = status.HTTP_409_CONFLICT
        return {
            'message': "User already exist",
            'status_code': 409,
            'error': 'CONFLICT'
        }
        
    hash_password = PassWord_Helper.hash_password(request.password)
    new_user = models.User(
        username=request.username,
        email=request.email, 
        password=hash_password
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {
            'message': "SignIn Succesfull",
            'details': {
                "username":new_user.username,
                "email":new_user.email,
            }
        }
    
    
def login(request: schema.LoginUser, response, db:Session):
    db_user: models.User = db.query(models.User).filter(models.User.email == request.email).first()
    
    
    if not db_user:
        response.status_code = status.HTTP_403_FORBIDDEN
        return {
            'message': "Invalid email and/or password",
            'status_code': 403,
            'error': 'FORBIDDEN'
        }
    
    if not (PassWord_Helper.verify_password(request.password, db_user.password)):
        response.status_code = status.HTTP_403_FORBIDDEN
        return {
            'message': "Invalid email and/or password",
            'status_code': 403,
            'error': 'FORBIDDEN'
        }
        
    #  Generate jwt
    access_token = JWT_Helper.create_access_token(data={"sub": {'email': db_user.email, 'id': db_user.id}})
    return {
        'message': 'Success',
        'status_code': 200,
        'data': {
            'email': db_user.email,
            'id': db_user.id
        },
        'access_token': access_token
    }
    
    
def show(user_id: int, response, db:Session):
    user: models.User = db.query(models.User).filter(models.User.id == user_id).first()
    
    if not user:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {
            'message': "Not found",
            'status_code': 404,
            'error': 'NOT FOUND'
        }
    
    return {
        'message': "success",
        'status_code': 200,
        'status': 'Success',
        'data': {
            "username":user.username,
            "email":user.email,
            "is_active":user.is_active,
            "is_staff":user.is_staff,
            "id":user.id            
        }
    }