from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category import CategoryORM


class CategoryRepository:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def get_all(self) -> list[CategoryORM]:
        return list((await self.db.scalars(select(CategoryORM))).all())

    async def get_by_id(self, category_id: UUID) -> CategoryORM | None:
        category = await self.db.get(CategoryORM, category_id)
        return category

    async def create(self, name: str) -> CategoryORM:
        new_category = CategoryORM(name=name)
        self.db.add(new_category)
        return new_category

    async def delete(self, category: CategoryORM) -> None:
        await self.db.delete(category)
