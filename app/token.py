from jose import JWTError, jwt
from datetime import datetime, timedelta

from database.functions.user import is_user 

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

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
        return is_user(decrypt_access_token(token))
    else:
        return False

def decrypt_access_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("user_id")
    except Exception as err:
        return 0
    return user_id

def get_user_id_by_token(request):
    return decrypt_access_token(request.cookies.get("token"))