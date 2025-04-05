from pydantic_settings import BaseSettings


class V1Settings(BaseSettings):
    prefix: str = '/v1'
    tags: str = 'Api version 1.0'


settings = V1Settings()