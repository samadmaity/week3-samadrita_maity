from fastapi import FastAPI
from app.database import engine, Base
from routers.user_router import router as user_router
from routers.category_router import router as category_router
from routers.product_router import router as product_router
from routers.cart_router import router as cart_router
from routers.order_router import router as order_router
from routers.auth_router import router as auth_router
from utils.logger import logger

Base.metadata.create_all(bind= engine)


app= FastAPI()

app.include_router(user_router)
app.include_router(category_router)
app.include_router(product_router)
app.include_router(cart_router)
app.include_router(order_router)
app.include_router(auth_router)


@app.get("/")
def home():
    return "Online Shopping API is running successfully"
