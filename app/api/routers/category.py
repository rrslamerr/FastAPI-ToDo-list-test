from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.api.dependencies.category import CategoryServiceDep
from app.core.exceptions import CategoryNotFound
from app.schemas.category import (
    CategoryCreateSchema,
    CategorySchema,
    CategoryUpdateSchema,
)

router = APIRouter(prefix="/categories")


@router.get("")
async def read_categories(
    category_service: CategoryServiceDep,
) -> list[CategorySchema]:
    return await category_service.list_categories()


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_category(
    payload: CategoryCreateSchema, category_service: CategoryServiceDep
) -> CategorySchema:
    return await category_service.create_category(category_create=payload)


@router.patch("/{category_id}")
async def update_category(
    category_id: UUID,
    payload: CategoryUpdateSchema,
    category_service: CategoryServiceDep,
) -> CategorySchema:
    try:
        return await category_service.update_category(
            category_id=category_id, category_update=payload
        )
    except CategoryNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: UUID, category_service: CategoryServiceDep
) -> None:
    try:
        await category_service.delete_category(category_id=category_id)
    except CategoryNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
