from fastapi import APIRouter

from .v1.router import router


Router = APIRouter(prefix="/api")
Router.include_router(router)