# app/modules/auth/service.py
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException
from typing import Tuple

from app.core.settings import get_settings
from app.dependencies.jwt_data import Jwt, get_jwt
from app.repository.users import UserRepository
from app.models.users import BaseUser, UserCreate
from app.utils.auth import hash_password, verify_password

settings = get_settings()


class AuthService:
    def __init__(
        self, 
        jwt_data: Jwt = Depends(get_jwt), 
        user_repo: UserRepository = Depends(UserRepository)
    ):
        self._jwt = jwt_data
        self.user_repo = user_repo

    def register_user(self, user_data: UserCreate) -> dict:
        if self.user_repo.get_user_by_username(user_data.username):
            raise HTTPException(
                status_code=400, 
                detail="Username already exists"
            )

        user_dict = user_data.model_dump()
        user_dict.update({
            "password": hash_password(user_dict["password"]),
            "role": "user"
        })
        
        return self.user_repo.create_user(user_dict)

    def authenticate_user(
        self, 
        user_data: OAuth2PasswordRequestForm
    ) -> Tuple[dict, str]:
        user = self.user_repo.get_user_by_username(user_data.username)
        
        if not user or not verify_password(user_data.password, user["password"]):
            raise HTTPException(
                status_code=401, 
                detail="Invalid credentials"
            )
            
        user_model = BaseUser(**user)
        user_dict = user_model.model_dump(exclude="id")
        token = self._jwt.create_access_token(user_dict)
        
        return (
            self._jwt.build_success_response(token, user_model),
            user_model.username
        )