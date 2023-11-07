from datetime import datetime, timedelta
from fastapi import FastAPI, Response, Request
from fastapi.responses import JSONResponse
from jose import JWTError, jwt
from Consts import *
import Models
import Database as db

app = FastAPI()


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    print(decrypt_access_token(encoded_jwt))
    return encoded_jwt


def decrypt_access_token(token):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    user_id = payload.get("user_id")
    return user_id


@app.get("/tasks")
def get_tasks(request: Request):
    try:
        if request.cookies.get("token"):
            return db.get_tasks(decrypt_access_token(request.cookies.get("token")))
        else:
            return {"response": "You are not authorized"}
    except Exception as er:
        print(er)
        return {"response": "fail"}


@app.post('/tasks')
def create_task(task_body: Models.TaskBody, request: Request):
    if request.cookies.get("token"):
        db.create_task(task_body.title, task_body.coins,
                       decrypt_access_token(request.cookies.get("token")), task_body.is_daily,
                       task_body.task_priority_id, task_body.description
                       )
    else:
        return {"response": "You are not authorized"}


@app.put('/tasks/{task_id}')
def edit_task(task_id: int, task_body: Models.TaskBody, request: Request):
    if request.cookies.get("token"):
        user_id = decrypt_access_token(request.cookies.get("token"))
        if db.is_user_task(user_id, task_id):
            db.edit_task(task_id, task_body.title, task_body.coins,
                         task_body.is_daily, task_body.task_priority_id,
                         task_body.description
                         )
            return {"response": "task_is_complete"}
        return {"response": "You don't have the rights to do this"}
    else:
        return {"response": "You are not authorized"}


@app.patch('/tasks/{task_id}/complete')
def complete_task(task_id: int, request: Request):
    if request.cookies.get("token"):
        user_id = decrypt_access_token(request.cookies.get("token"))
        if db.is_user_task(user_id, task_id):
            db.complete_task(task_id)
            return {"response":"task_is_complete"}
        return {"response":"You don't have the rights to do this"}


@app.get("/priorities")
def get_priorities():
    return db.get_priorities()


@app.post("/auth")
def auth(user_data: Models.UserDataForAuth):
    user_id = db.auth(user_data.email, user_data.password)
    if user_id:
        response = JSONResponse(content={"response": "OK"})
        response.set_cookie(key="token", value=create_access_token(data={"user_id": user_id}))
        return response


@app.post("/register")
def register(user_data: Models.UserDataForRegistration):
    try:
        if db.check_user_by_email(user_data.email):
            return {"response": "This email already is used"}
        db.create_new_user(user_data.email, user_data.username, user_data.password)
        return {"response": "OK"}
    except Exception as er:
        print(er)
        return {"response": "fail"}
