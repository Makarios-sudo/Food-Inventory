from fastapi import FastAPI
from routers.order_routes import order_router
from routers.user_routes import user_router


app = FastAPI()

@app.get("/")
async def home():
    return {"message": "Welcome to Food Inventory"}


app.include_router(user_router)
app.include_router(order_router)

