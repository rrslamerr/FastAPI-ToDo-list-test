from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routers.category import router as category_router
from app.api.routers.task import router as task_router
from app.core.config import settings
from app.core.logging import configure_logging
from app.core.middleware import log_requests, request_number

app = FastAPI()

configure_logging()

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.middleware("http")(log_requests)
app.middleware("http")(request_number)

app.include_router(task_router)
app.include_router(category_router)
