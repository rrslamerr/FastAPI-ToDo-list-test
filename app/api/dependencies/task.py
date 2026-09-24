from typing import Annotated

from app.api.dependencies.db import SessionDep
from app.services.task import TaskService
from fastapi import Depends


def get_task_service(db: SessionDep) -> TaskService:
    return TaskService(db)


TaskServiceDep = Annotated[TaskService, Depends(get_task_service)]
