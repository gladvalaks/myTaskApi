from pydantic import BaseModel

class Task_priority(BaseModel):
    id: int
    title: str
    order: int