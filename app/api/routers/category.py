from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.api.dependencies.category import CategoryServiceDep
from app.schemas.category import (
    CategoryCreateSchema,
    CategorySchema,
    CategoryUpdateSchema,
)
from app.services.category import CategoryNotFound

router = APIRouter(prefix="/categories")


@router.get("")
def read_categories(
    category_service: CategoryServiceDep,
) -> list[CategorySchema]:
    return category_service.list_categories()


@router.post("", status_code=status.HTTP_201_CREATED)
def create_category(
    payload: CategoryCreateSchema, category_service: CategoryServiceDep
) -> CategorySchema:
    return category_service.create_category(category_create=payload)


@router.patch("/{category_id}")
def update_category(
    category_id: UUID,
    payload: CategoryUpdateSchema,
    category_service: CategoryServiceDep,
) -> CategorySchema:
    try:
        return category_service.update_category(
            category_id=category_id, category_update=payload
        )
    except CategoryNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: UUID, category_service: CategoryServiceDep
) -> None:
    try:
        category_service.delete_category(category_id=category_id)
    except CategoryNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)
        )
