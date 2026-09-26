from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import CategoryNotFound
from app.repositories.category import CategoryRepository
from app.schemas.category import (
    CategoryCreateSchema,
    CategorySchema,
    CategoryUpdateSchema,
)


class CategoryService:
    def __init__(self, db: AsyncSession) -> None:
        self.db = db
        self.category_repository = CategoryRepository(db=db)

    async def list_categories(self) -> list[CategorySchema]:
        categories_orm = await self.category_repository.get_all()
        return [CategorySchema.model_validate(category) for category in categories_orm]

    async def create_category(
        self, category_create: CategoryCreateSchema
    ) -> CategorySchema:
        category_orm = await self.category_repository.create(name=category_create.name)
        await self.db.commit()
        return CategorySchema.model_validate(category_orm)

    async def update_category(
        self, category_id: UUID, category_update: CategoryUpdateSchema
    ) -> CategorySchema:
        category_for_update = await self.category_repository.get_by_id(
            category_id=category_id
        )
        if category_for_update is None:
            raise CategoryNotFound(f"Category with id {category_id} not found")
        if category_update.name is not None:
            category_for_update.name = category_update.name
        await self.db.commit()
        return CategorySchema.model_validate(category_for_update)

    async def delete_category(self, category_id: UUID) -> None:
        category_for_delete = await self.category_repository.get_by_id(
            category_id=category_id
        )
        if category_for_delete is None:
            raise CategoryNotFound(f"Category with id {category_id} not found")
        await self.category_repository.delete(category_for_delete)
        await self.db.commit()
