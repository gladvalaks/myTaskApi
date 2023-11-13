import pydantic

class UserForRegistration(pydantic.BaseModel):
    email: str
    username: str
    password: str

class UserForAuth(pydantic.BaseModel):
    email: str
    password: str

class UserForGetTasks(pydantic.BaseModel):
    user_id: int