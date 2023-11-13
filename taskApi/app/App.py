import fastapi
import sys
import database.database 
from app.routes.priorities import router as priorities_router
from app.routes.tasks import router as tasks_router
from app.routes.user import router as user_router
app = fastapi.FastAPI()
app.include_router(priorities_router)
app.include_router(tasks_router)
app.include_router(user_router)