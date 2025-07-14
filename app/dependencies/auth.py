from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2
from fastapi.openapi.models import OAuthFlows
from typing import Optional
from app.core.settings import Settings, get_settings
from app.dependencies.jwt_data import Jwt, get_jwt
from app.models.users import BaseUser, User

class OAuth2PasswordBearerWithCookie(OAuth2):
    def __init__(
        self,
        tokenUrl: str,
        scheme_name: Optional[str] = None,
        scopes: Optional[dict[str, str]] = None,
        auto_error: bool = True,
    ):
        flows = OAuthFlows(password={"tokenUrl": tokenUrl, "scopes": scopes or {}})
        super().__init__(flows=flows, scheme_name=scheme_name, auto_error=auto_error)

    async def __call__(self, request: Request) -> Optional[str]:
        token = request.cookies.get("access_token")
        if not token:
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Missing access token in cookies",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            return None
        return token

oauth2_scheme = OAuth2PasswordBearerWithCookie(tokenUrl="/auth/login")

class IsAuthenticated:
    def __init__(
        self,
        request: Request,
        token: str = Depends(oauth2_scheme),
        jwt: Jwt = Depends(get_jwt),
        settings: Settings = Depends(get_settings),
    ) -> None:
        try:
            data = jwt.verify_access_token(token)
            self.login = data["username"]
            self.role = data.get("role", "user")
            request.state.login = self.login
            request.state.role = self.role
        except HTTPException:
            raise  # Пробрасываем уже существующие HTTPException
        except Exception as ex:
            detail = str(ex) if settings.debug else "Could not validate credentials"
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=detail,
                headers={"WWW-Authenticate": "Bearer"},
            )