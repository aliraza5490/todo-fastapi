from fastapi import APIRouter
from .item import items_router 
from .auth import auth_router

api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(items_router)