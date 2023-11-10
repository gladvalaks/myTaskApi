import fastapi
import sys

from app.routes.priorities import router as priorities_router
from app.routes.tasks import router as tasks_router
app = fastapi.FastAPI()
app.include_router(priorities_router)
app.include_router(tasks_router)