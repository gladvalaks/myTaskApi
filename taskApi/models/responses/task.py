import pydantic


class Task(pydantic.BaseModel):
    id: int
    title: str
    description: str
    coins: int
    is_daily: bool
    task_priority_id: int
    created_at: int
    finished_at:int | None
