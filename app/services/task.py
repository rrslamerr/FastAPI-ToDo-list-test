from uuid import UUID

from app.core.exceptions import TaskNotFound
from app.repositories.task import TaskRepository
from app.schemas.task import TaskCreateSchema, TaskSchema, TaskUpdateSchema
from sqlalchemy.ext.asyncio import AsyncSession


class TaskService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.task_repository = TaskRepository(db=db)

    async def list_tasks(self) -> list[TaskSchema]:
        tasks_orm = await self.task_repository.get_all()
        return [TaskSchema.model_validate(task) for task in tasks_orm]

    async def create_task(self, task_create: TaskCreateSchema) -> TaskSchema:
        task_orm = await self.task_repository.create(title=task_create.title)
        await self.db.commit()
        return TaskSchema.model_validate(task_orm)

    async def update_task(
        self, task_id: UUID, task_update: TaskUpdateSchema
    ) -> TaskSchema:
        task_for_update = await self.task_repository.get_by_id(task_id=task_id)
        if task_for_update is None:
            raise TaskNotFound(f"Task with id {task_id} not found")
        if task_update.title is not None:
            task_for_update.title = task_update.title
        if task_update.completed is not None:
            task_for_update.completed = task_update.completed
        await self.db.commit()
        return TaskSchema.model_validate(task_for_update)

    async def delete_task(self, task_id: UUID) -> None:
        task_for_delete = await self.task_repository.get_by_id(task_id=task_id)
        if task_for_delete is None:
            raise TaskNotFound(f"Task with id {task_id} not found")
        await self.task_repository.delete(task_for_delete)
        await self.db.commit()
