from unittest.mock import Mock
from uuid import UUID

import pytest

from app.core.exceptions import TaskNotFound
from app.models.task import TaskORM
from app.schemas.task import TaskCreateSchema, TaskSchema, TaskUpdateSchema
from app.services.task import TaskService


async def test_list_tasks_returns_pydantic_models(
    service: TaskService, repository_mock: Mock
) -> None:
    repository_mock.get_all.return_value = [
        TaskORM(
            id=UUID("00000000-0000-0000-0000-000000000001"),
            title="Изучить pytest",
            completed=False,
        ),
        TaskORM(
            id=UUID("00000000-0000-0000-0000-000000000002"),
            title="Написать первый тест",
            completed=True,
        ),
    ]

    result = await service.list_tasks()

    assert result == [
        TaskSchema(
            id=UUID("00000000-0000-0000-0000-000000000001"),
            title="Изучить pytest",
            completed=False,
        ),
        TaskSchema(
            id=UUID("00000000-0000-0000-0000-000000000002"),
            title="Написать первый тест",
            completed=True,
        ),
    ]


async def test_create_task_commits_created_task(
    service: TaskService, db_mock: Mock, repository_mock: Mock
) -> None:
    created_task = TaskORM(
        id=UUID("00000000-0000-0000-0000-000000000001"),
        title="Новая задача",
        completed=False,
    )
    repository_mock.create.return_value = created_task

    result = await service.create_task(TaskCreateSchema(title="Новая задача"))

    repository_mock.create.assert_called_once_with(title="Новая задача")
    db_mock.commit.assert_called_once_with()
    assert result.model_dump() == {
        "id": UUID("00000000-0000-0000-0000-000000000001"),
        "title": "Новая задача",
        "completed": False,
    }


@pytest.mark.parametrize(
    ("payload", "expected_title", "expected_completed"),
    [
        pytest.param(
            TaskUpdateSchema(title="Обновить заголовок"), "Обновить заголовок", False
        ),
        pytest.param(TaskUpdateSchema(completed=True), "Старая задача", True),
        pytest.param(TaskUpdateSchema(title="Готово", completed=True), "Готово", True),
    ],
)
async def test_update_task_updates_only_passed_fields(
    service: TaskService,
    db_mock: Mock,
    repository_mock: Mock,
    payload: TaskUpdateSchema,
    expected_title: str,
    expected_completed: bool,
) -> None:
    task = TaskORM(
        id=UUID("00000000-0000-0000-0000-000000000001"),
        title="Старая задача",
        completed=False,
    )
    repository_mock.get_by_id.return_value = task

    result = await service.update_task(
        UUID("00000000-0000-0000-0000-000000000001"), payload
    )

    repository_mock.get_by_id.assert_called_once_with(
        task_id=UUID("00000000-0000-0000-0000-000000000001")
    )
    db_mock.commit.assert_called_once_with()
    assert result.model_dump() == {
        "id": UUID("00000000-0000-0000-0000-000000000001"),
        "title": expected_title,
        "completed": expected_completed,
    }


async def test_update_task_raises_when_task_not_found(
    service: TaskService,
    db_mock: Mock,
    repository_mock: Mock,
) -> None:
    repository_mock.get_by_id.return_value = None

    with pytest.raises(TaskNotFound):
        await service.update_task(
            UUID("00000000-0000-0000-0000-000000000099"),
            TaskUpdateSchema(title="Неважно"),
        )
    db_mock.commit.assert_not_called()
