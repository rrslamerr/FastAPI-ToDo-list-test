from typing import Annotated

from fastapi import Depends

from app.api.dependencies.db import SessionDep
from app.services.task import TaskService


def get_task_service(db: SessionDep) -> TaskService:
    return TaskService(db)


TaskServiceDep = Annotated[TaskService, Depends(get_task_service)]
