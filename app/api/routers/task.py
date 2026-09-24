from uuid import UUID

from app.api.dependencies.task import TaskServiceDep
from app.core.exceptions import TaskNotFound
from app.schemas.task import (
    TaskCreateSchema,
    TaskSchema,
    TaskUpdateSchema,
)
from fastapi import APIRouter, HTTPException, status

router = APIRouter(prefix="/tasks")


@router.get("")
def read_tasks(task_service: TaskServiceDep) -> list[TaskSchema]:
    return task_service.list_tasks()


@router.post("", status_code=status.HTTP_201_CREATED)
def create_task(
    payload: TaskCreateSchema,
    task_service: TaskServiceDep,
) -> TaskSchema:
    return task_service.create_task(task_create=payload)


@router.patch("/{task_id}")
def update_task(
    task_id: UUID,
    payload: TaskUpdateSchema,
    task_service: TaskServiceDep,
) -> TaskSchema:
    try:
        return task_service.update_task(task_id=task_id, task_update=payload)
    except TaskNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: UUID,
    task_service: TaskServiceDep,
) -> None:
    try:
        return task_service.delete_task(task_id=task_id)
    except TaskNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
