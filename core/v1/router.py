from fastapi import APIRouter

from .setting import settings


router = APIRouter(
    prefix=settings.prefix, tags=[settings.tags]
)


@router.get('/')
def check():
    return {"message": "OK"}
