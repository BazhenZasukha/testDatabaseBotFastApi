from pydantic import BaseModel


class LineSchema(BaseModel):
    summ: float
    description: str
    created_by: str