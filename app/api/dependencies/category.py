from typing import Annotated

from app.api.dependencies.db import SessionDep
from app.services.category import CategoryService
from fastapi import Depends


def get_category_service(db: SessionDep) -> CategoryService:
    return CategoryService(db)


CategoryServiceDep = Annotated[CategoryService, Depends(get_category_service)]
