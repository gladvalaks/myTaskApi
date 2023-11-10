from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int


class UserDataForRegistration(BaseModel):
    email: str
    username: str
    password: str

class UserDataForAuth(BaseModel):
    email: str
    password: str

class TaskBody(BaseModel):
    title: str
    description: str
    coins: int
    is_daily: bool
    task_priority_id: int




class GetTasks(BaseModel):
    user_id: int
