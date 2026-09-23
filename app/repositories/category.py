from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.category import CategoryORM


class CategoryRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self) -> list[CategoryORM]:
        return list(self.db.scalars(select(CategoryORM)).all())

    def get_by_id(self, category_id: UUID) -> CategoryORM:
        category = self.db.get(CategoryORM, category_id)
        if category is None:
            raise ValueError(f"category with id {category_id} not found")
        return category

    def create(self, name: str) -> CategoryORM:
        new_category = CategoryORM(name=name)
        self.db.add(new_category)
        return new_category

    def delete(self, category: CategoryORM) -> None:
        self.db.delete(category)
