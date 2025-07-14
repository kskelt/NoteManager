import uvicorn
from fastapi import FastAPI

from app.core.settings import Settings, get_settings
from app.core.init_app import init_app

# Loading app
app: FastAPI = init_app()
_settings: Settings = get_settings()

if __name__ == "__main__":
    uvicorn.run("app.main:app", reload=True, host="0.0.0.0", port=_settings.app_port)
