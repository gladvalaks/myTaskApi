from fastapi import  Response, Request,status
from fastapi import APIRouter
from fastapi.responses import JSONResponse
import Models.requests.user as models
import database.functions.user as db
import taskApi.App.token as token

router = APIRouter()
@router.post("/api/auth")
def auth(user:models.UserForAuth, response:Response):
    user_id = db.auth(user.email, user.password)    
    if user_id:
        res = JSONResponse(content={"response": "OK"})
        res.set_cookie(
            key="token",
            value=token.create_access_token(data={"user_id": user_id}),
            secure=False,
            samesite=None,
        )
        response.status_code = status.HTTP_200_OK
        return res
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED


@router.post("/api/register")
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
    
@router.get("/api/user")
def get_name(request:Request,response:Response):
    if token.is_token_valid(request):
        response.status_code = status.HTTP_200_OK
        return db.get_username(token.get_user_id(request))
    else:
        response.status_code = status.HTTP_401_UNAUTHORIZED