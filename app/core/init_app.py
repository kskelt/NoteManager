# app/init_app.py
from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.core.settings import get_settings
from app.core.logger import configure_logging
from app.routes.auth import auth_router
from app.routes.notes import note_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from app.database import get_db, get_db_instance

settings = get_settings()


def init_app():

    app = FastAPI(
        title=settings.app_name,
        description="API for  notes management",
        version="1.0.0",
        lifespan=lifespan
    )
    configure_logging(settings.log_file)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(auth_router)
    app.include_router(note_router)

    return app


def append_swagger(app: FastAPI):
    """Enabling swagger, redoc and json api doc"""

    @app.get("/docs", include_in_schema=False)
    def get_swagger():
        return get_swagger_ui_html(
            openapi_url="/openapi.json",
            title=settings.app_name,
            swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@4/swagger-ui-bundle.js",
            swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@4/swagger-ui.css",
        )


def lifespan(app: FastAPI):
    """Lifespan with async database connection"""
    # Connect to database on startup

    get_db_instance.connect(url=settings.mongo_url, db_name=settings.database_name)
    yield
    # Disconnect on shutdown
    get_db_instance.close()