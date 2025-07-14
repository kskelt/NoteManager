from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from app.models.users import BaseUser, UserCreate
from app.services.auth import AuthService

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/register")
def register(user: UserCreate, service: AuthService = Depends(AuthService)):
    created_user = service.register_user(user)
    return {"msg": "User registered", "username": created_user["username"]}


@auth_router.post("/login")
def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), service:  AuthService = Depends(AuthService)):
    response, username = service.authenticate_user(form_data)
    request.state.login = username
    return response
