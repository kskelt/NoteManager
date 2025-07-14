from datetime import datetime, timedelta, timezone
from functools import lru_cache
from uuid import uuid4
from fastapi import HTTPException, status
from fastapi.responses import JSONResponse
import jwt
from app.core.settings import get_settings
from app.models.users import User


class Jwt:
    def __init__(
        self,
        access_secret_key: str,
        algorithm: str,
        access_lifetime: timedelta,
    ):
        self.access_secret_key = access_secret_key
        self.algorithm = algorithm
        self.access_lifetime = access_lifetime

    def create_access_token(self, data: dict) -> str:
        """Генерация access токена"""
        expire = datetime.now(timezone.utc) + self.access_lifetime
        to_encode = data.copy()
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.access_secret_key, self.algorithm)

    def verify_access_token(self, token: str) -> dict:
        """Валидация access токена"""
        return self._verify_token(token, self.access_secret_key)


    def get_token_id(self, token: str) -> str:
        """Получение идентификатора токена без валидации"""
        try:
            payload = jwt.decode(token, options={"verify_signature": False})
            return payload.get("jti")
        except jwt.PyJWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate token",
            )

    def _verify_token(self, token: str, secret_key: str) -> dict:
        """Общая логика валидации токенов"""
        try:
            payload = jwt.decode(token, secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
            )
        except jwt.PyJWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate token",
            )
    def build_success_response(
        self, access_token: str, user: User | None = None
    ):
        content = {}

        if user is not None:
            content["user"] = user.model_dump(mode="json")

        response = JSONResponse(
            status_code=status.HTTP_200_OK,
            content=content,
        )
        response.set_cookie("access_token", access_token, httponly=True)
        return response


@lru_cache()
def get_jwt() -> Jwt:
    """Фабрика для создания сервиса JWT"""
    settings = get_settings()
    return Jwt(
        access_secret_key=settings.access_token_secret,
        algorithm=settings.token_algorithm,
        access_lifetime=timedelta(minutes=settings.access_token_expire_minutes),

    )