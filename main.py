import sys
from pathlib import Path

APP_DIR: str = Path(__file__).resolve().parent.parent.as_posix()
sys.path.append(APP_DIR)

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.application.modules.common.exceptions import BaseHttpException
from app.exception_handlers import http_exception_handler
from app.application.modules.auth.routers import (
    router as auth_router,
)
from app.application.modules.project.routers import (
    router as project_router,
)
from app.application.modules.user.routers import (
    router as user_router,
)

app = FastAPI()
app.include_router(user_router)
app.include_router(project_router)
app.include_router(auth_router)

app.add_exception_handler(BaseHttpException, http_exception_handler)  # type: ignore

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
