
from fastapi import  Response, Request,status,APIRouter,Depends,Cookie
from typing import Annotated

import models.requests.task as task_models
import database.functions.task as db
import app.token as jwt_token

router = APIRouter()

@router.get("/api/tasks")
def get_tasks(request:Request, response:Response,token: Annotated[str, Cookie()]):
    try:
        if jwt_token.is_token_valid(request):
            response.status_code = status.HTTP_200_OK
            return db.get_serialized_today_tasks(jwt_token.get_user_id(request))
        else:
            response.status_code = status.HTTP_401_UNAUTHORIZED
    except Exception as er:
        print(er)
        return {"response": "fail"}


@router.post('/api/tasks')
def create_task(task_body: task_models.TaskBody, request: Request, response:Response):
    if jwt_token.is_token_valid(request):
        db.create_task(
            task_body.title,
            task_body.coins,
            jwt_token.get_user_id(request),
            task_body.is_daily,
            task_body.task_priority_id,
            task_body.description,
        )
        response.status_code = status.HTTP_201_CREATED
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED

@router.delete('/api/tasks/{task_id}')
def delete_task(task_id: int, request: Request, response:Response):
    if jwt_token.is_token_valid(request):
        user_id = jwt_token.decrypt_access_token(request.cookies.get("token"))
        if db.is_user_task(user_id, task_id):
            db.delete_task(task_id)
            return {"response": "task was deleted"}
        return {"response": "You don't have the rights to do this"}
    else:
        return {"response": "You are not authorized"}

@router.put('/api/tasks/{task_id}')
def edit_task(task_id: int, task_body: task_models.TaskBody, request: Request, response:Response):
    if jwt_token.is_token_valid(request):
        user_id = jwt_token.decrypt_access_token(request.cookies.get("token"))
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


@router.patch('/api/tasks/{task_id}/complete')
def complete_task(task_id: int, request: Request, response:Response):   
    if jwt_token.is_token_valid(request):
        user_id = jwt_token.decrypt_access_token(request.cookies.get("token"))
        if db.is_user_task(user_id, task_id):
            db.complete_task(task_id)
            response.status_code = status.HTTP_202_ACCEPTED
            return {"response": "task_is_complete"}
        response.status_code = status.HTTP_403_FORBIDDEN
        return {"response": "You don't have the rights to do this"}
    else:
        return {"response": "You are not authorized"}
    