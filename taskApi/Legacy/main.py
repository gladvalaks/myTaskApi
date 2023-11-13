from datetime import datetime, timedelta
from fastapi import FastAPI, Response, Request, Body, status
from fastapi.responses import JSONResponse
from jose import JWTError, jwt
from consts import *
import taskApi.models as models
import taskApi.database as db

app = FastAPI()


def get_user_id(request):
    return decrypt_access_token(request.cookies.get("token"))
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    print(decrypt_access_token(encoded_jwt))
    return encoded_jwt

def is_token_valid(request):
    token = request.cookies.get("token")
    if token:
        return db.is_user(decrypt_access_token(token))
    else:
        return False


def decrypt_access_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
    except Exception as err:
        return 0
    return user_id


@app.get("/api/tasks")
def get_tasks(request: Request, response:Response):
    try:
        if is_token_valid(request):
            response.status_code = status.HTTP_200_OK
            return db.get_tasks(get_user_id(request))
        else:
            response.status_code = status.HTTP_401_UNAUTHORIZED
    except Exception as er:
        print(er)
        return {"response": "fail"}


@app.post('/api/tasks')
def create_task(task_body: models.TaskBody, request: Request, response:Response):
    if is_token_valid(request):
        db.create_task(
            task_body.title,
            task_body.coins,
            get_user_id(request),
            task_body.is_daily,
            task_body.task_priority_id,
            task_body.description,
        )
        response.status_code = status.HTTP_201_CREATED
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED

@app.delete('/api/tasks/{task_id}')
def delete_task(task_id: int, request: Request, response:Response):
    if is_token_valid(request):
        user_id = decrypt_access_token(request.cookies.get("token"))
        if db.is_user_task(user_id, task_id):
            db.delete_task(task_id)
            return {"response": "task was deleted"}
        return {"response": "You don't have the rights to do this"}
    else:
        return {"response": "You are not authorized"}

@app.put('/api/tasks/{task_id}')
def edit_task(task_id: int, task_body: models.TaskBody, request: Request, response:Response):
    if is_token_valid(request):
        user_id = decrypt_access_token(request.cookies.get("token"))
        if db.is_user_task(user_id, task_id):
            db.edit_task(
                task_id,
                task_body.title,
                task_body.coins,
                task_body.is_daily,
                task_body.task_priority_id,
                task_body.description,
            )
            response.status_code = status.HTTP_202_ACCEPTED
            return {"response": "task_is_edited"}
        return {"response": "You don't have the rights to do this"}
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return {"response": "You are not authorized"}


@app.patch('/api/tasks/{task_id}/complete')
def complete_task(task_id: int, request: Request, response:Response):   
    if is_token_valid(request):
        user_id = decrypt_access_token(request.cookies.get("token"))
        if db.is_user_task(user_id, task_id):
            db.complete_task(task_id)
            response.status_code = status.HTTP_202_ACCEPTED
            return {"response": "task_is_complete"}
        response.status_code = status.HTTP_403_FORBIDDEN
        return {"response": "You don't have the rights to do this"}
    else:
        return {"response": "You are not authorized"}
    


@app.get("/api/priorities")
def get_priorities():
    return db.get_priorities()


@app.post("/api/auth")
def auth(user:models.UserDataForAuth, response:Response):
    user_id = db.auth(user.email, user.password)    
    if user_id:
        res = JSONResponse(content={"response": "OK"})
        res.set_cookie(
            key="token",
            value=create_access_token(data={"user_id": user_id}),
            secure=False,
            samesite=None,
        )
        response.status_code = status.HTTP_200_OK
        return res
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED


@app.post("/api/register")
def register(user_data: models.UserDataForRegistration, response:Response):
    try:
        if db.check_user_by_email(user_data.email):
            response.status_code = status.HTTP_409_CONFLICT
            return {"response": "This email already is used"}
        db.create_new_user(user_data.email, user_data.username, user_data.password)
        response.status_code = status.HTTP_201_CREATED
        return {"response": "OK"}
    except Exception as er:
        print(er)
        return {"response": "fail"}
    
@app.get("/api/user")
def get_name(request:Request,response:Response):
    if is_token_valid(request):
        response.status_code = status.HTTP_200_OK
        return db.get_username(get_user_id(request))
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED
