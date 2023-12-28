from fastapi import Response, APIRouter, Depends, status
from sqlalchemy.orm import Session
import database.schema as schema
from database.database import get_db
from repository import user_repository


user_router = APIRouter(
    prefix="/api/v1/auth",
    tags= ["users"]
)


@user_router.post('/sign_up', status_code=status.HTTP_201_CREATED, tags=['users'])
async def signup(request:schema.RegisterUser, response:Response, db:Session=Depends(get_db)):
    return user_repository.sign_up(request, response, db)
    


@user_router.post('/login', status_code=status.HTTP_200_OK, tags=['users'])
async def login(request:schema.LoginUser, response:Response, db:Session=Depends(get_db)):
    return user_repository.login(request, response, db)
    

    
@user_router.get('/user/{user_id}', status_code=status.HTTP_200_OK, tags=['users'])
async def show(user_id: int, response: Response, db: Session = Depends(get_db)):
    return user_repository.show(user_id, response, db)