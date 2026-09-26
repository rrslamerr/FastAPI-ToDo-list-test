from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import TaskORM


class TaskRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_all(self) -> list[TaskORM]:
        return list((await self.db.scalars(select(TaskORM))).all())

    async def get_by_id(self, task_id: UUID) -> TaskORM | None:
        task = await self.db.get(TaskORM, task_id)
        return task

    async def create(self, title: str) -> TaskORM:
        new_task = TaskORM(title=title, completed=False)
        self.db.add(new_task)
        return new_task

    async def delete(self, task: TaskORM) -> None:
        await self.db.delete(task)
