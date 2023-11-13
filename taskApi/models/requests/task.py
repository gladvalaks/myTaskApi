import pydantic


class TaskBody(pydantic.BaseModel):
    title: str
    description: str
    coins: int
    is_daily: bool
    task_priority_id: int
