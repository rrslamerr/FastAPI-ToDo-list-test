from unittest.mock import Mock
from uuid import UUID

import pytest

from app.core.exceptions import CategoryNotFound
from app.models.category import CategoryORM
from app.schemas.category import (
    CategoryCreateSchema,
    CategorySchema,
    CategoryUpdateSchema,
)
from app.services.category import CategoryService


async def test_list_categories_return_pydantic_model(
    category_service: CategoryService, category_repository_mock: Mock
) -> None:
    category_repository_mock.get_all.return_value = [
        CategoryORM(
            id=UUID("00000000-0000-0000-0000-000000000001"), name="Тестовая категория"
        ),
        CategoryORM(
            id=UUID("00000000-0000-0000-0000-000000000002"),
            name="Вторая тестовая категория",
        ),
    ]

    result = await category_service.list_categories()

    assert result == [
        CategorySchema(
            id=UUID("00000000-0000-0000-0000-000000000001"), name="Тестовая категория"
        ),
        CategorySchema(
            id=UUID("00000000-0000-0000-0000-000000000002"),
            name="Вторая тестовая категория",
        ),
    ]


async def test_create_category_commits_created_category(
    category_service: CategoryService, category_repository_mock: Mock, db_mock: Mock
) -> None:
    created_category = CategoryORM(
        id=UUID("00000000-0000-0000-0000-000000000001"),
        name="Новая категория",
    )

    category_repository_mock.create.return_value = created_category

    result = await category_service.create_category(
        CategoryCreateSchema(name="Новая категория")
    )

    category_repository_mock.create.assert_called_once_with(name="Новая категория")
    db_mock.commit.assert_called_once_with()

    assert result.model_dump() == {
        "id": UUID("00000000-0000-0000-0000-000000000001"),
        "name": "Новая категория",
    }


async def test_update_category(
    category_service: CategoryService,
    category_repository_mock: Mock,
    db_mock: Mock,
) -> None:
    category = CategoryORM(
        id=UUID("00000000-0000-0000-0000-000000000001"),
        name="Старая категория",
    )

    category_repository_mock.get_by_id.return_value = category

    result = await category_service.update_category(
        UUID("00000000-0000-0000-0000-000000000001"),
        CategoryUpdateSchema(name="Обновленная категория"),
    )

    category_repository_mock.get_by_id.assert_called_once_with(
        category_id=UUID("00000000-0000-0000-0000-000000000001")
    )
    db_mock.commit.assert_called_once_with()

    assert result.model_dump() == {
        "id": UUID("00000000-0000-0000-0000-000000000001"),
        "name": "Обновленная категория",
    }


async def test_category_update_raises_when_category_not_found(
    category_service: CategoryService,
    category_repository_mock: Mock,
    db_mock: Mock,
) -> None:
    category_repository_mock.get_by_id.return_value = None

    with pytest.raises(CategoryNotFound):
        await category_service.update_category(
            UUID("00000000-0000-0000-0000-000000000001"),
            CategoryUpdateSchema(name="Неважно"),
        )

    db_mock.commit.assert_not_called()


async def test_delete_category(
    category_service: CategoryService, category_repository_mock: Mock, db_mock: Mock
) -> None:
    category = CategoryORM(
        id=UUID("00000000-0000-0000-0000-000000000001"),
        name="Тестовая категория",
    )

    category_repository_mock.get_by_id.return_value = category

    result = await category_service.delete_category(
        category_id=UUID("00000000-0000-0000-0000-000000000001")
    )

    category_repository_mock.delete.assert_called_once_with(category)
    category_repository_mock.get_by_id.assert_called_once_with(
        category_id=UUID("00000000-0000-0000-0000-000000000001")
    )
    db_mock.commit.assert_called_once_with()

    assert result is None
