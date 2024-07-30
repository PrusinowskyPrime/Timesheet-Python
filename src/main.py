# pylint: disable=C0413
import sys
from pathlib import Path

APP_DIR: str = Path(__file__).resolve().parent.parent.as_posix()
sys.path.append(APP_DIR)

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.application.modules.common.exceptions import BaseHttpException
from src.application.modules.common.exception_handlers import http_exception_handler
from src.api.modules.user.routers import router as user_router
from src.api.modules.auth.routers import router as auth_router

app = FastAPI()
app.add_exception_handler(BaseHttpException, http_exception_handler)  # type: ignore

app.include_router(user_router)
app.include_router(auth_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Hello World!"}

if __name__ == "__main__":
    uvicorn.run("main:src", host="127.0.0.1", port=8000, reload=True)
