from fastapi import APIRouter, Depends
from .controllers import AuthController
from ...utilities.tags import Tags
from ...models.user import User, UserLogin, UserCreate
from ...utilities.auth import get_user_from_token
from ...utilities.db import get_session

auth_router = APIRouter(prefix="/auth", tags=[Tags.users])


@auth_router.post("/register")
def register(user: UserCreate, session = Depends(get_session)):
    return AuthController.register(user, session)


@auth_router.post("/protected")
def protected(user: User = Depends(get_user_from_token)):
    return AuthController.protected(user)

@auth_router.post("/login")
def login(user: UserLogin, session = Depends(get_session)):
    return AuthController.login(user, session)

