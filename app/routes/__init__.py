from fastapi import APIRouter
from .item import items_router 
from .auth import auth_router
from .group import group_router
from ..settings import settings

api_router = APIRouter(prefix=settings.API_V1_STR)

api_router.include_router(auth_router)
api_router.include_router(items_router)
api_router.include_router(group_router)