from fastapi import Depends, APIRouter, Response
from sqlalchemy.orm import Session
from starlette import status
from database.database import get_db
import database.schema as schema
from helpers.helper import User_Helper
from repository import order_repository


order_router = APIRouter(
    prefix="/api/v1/order",
    tags=["orders"]
)

@order_router.post("/create_order", status_code=status.HTTP_201_CREATED, tags=["orders"])
async def create_order(request:schema.Order, response:Response, db:Session=Depends(get_db), current_user: schema.User = Depends(User_Helper.get_current_user)):
    return order_repository.create_order(request, response, db, current_user)


@order_router.get("/all_orders", status_code=status.HTTP_200_OK, tags=["orders"])
async def all_order(db:Session = Depends(get_db), current_user: schema.User = Depends(User_Helper.get_current_user)):
    return order_repository.all_orders(db, current_user)


@order_router.get("/get_order/{order_id}", status_code=status.HTTP_200_OK, tags=["orders"])
async def get_order(order_id:int, response:Response, db:Session=Depends(get_db), current_user: schema.User = Depends(User_Helper.get_current_user)):
    return order_repository.get_order(order_id, response, db, current_user)


@order_router.put("/update_order/{order_id}", status_code=status.HTTP_201_CREATED, tags=["orders"])
async def update_order(order_id:int, request:schema.Order, response:Response, db:Session=Depends(get_db), current_user:schema.User=Depends(User_Helper.get_current_user)):
    return order_repository.update_order(order_id, request, response, db, current_user)


@order_router.delete("/delete_order/{order_id}", status_code=status.HTTP_200_OK, tags=["orders"])
async def delete_order(order_id:int, response:Response, db:Session = Depends(get_db),  current_user:schema.User=Depends(User_Helper.get_current_user)):
    return order_repository.delete_order(order_id, response, db, current_user)

