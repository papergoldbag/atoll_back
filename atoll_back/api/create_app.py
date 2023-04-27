import logging

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

from atoll_back.api.events import on_startup, on_shutdown
from atoll_back.api.v1 import api_v1_router
from atoll_back.core import settings
from atoll_back.log import setup_logging

log = logging.getLogger(__name__)


def create_app() -> FastAPI:
    setup_logging()

    app = FastAPI(
        title=settings.api_title,
        on_startup=[on_startup],
        on_shutdown=[on_shutdown],
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/api/openapi.json"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    app.include_router(api_v1_router, prefix=settings.api_prefix)

    return app
