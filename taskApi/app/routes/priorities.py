from fastapi import APIRouter

import database.functions.priorities as db

router = APIRouter()
@router.get("/api/priorities")
def get_priorities():
    return db.get_priorities()