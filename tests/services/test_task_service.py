from unittest.mock import Mock
from uuid import UUID

import pytest

from app.core.exceptions import TaskNotFound
from app.models.task import TaskORM
from app.schemas.task import TaskCreateSchema, TaskSchema, TaskUpdateSchema
from app.services.task import TaskService


async def test_list_tasks_returns_pydantic_models(
    task_service: TaskService, task_repository_mock: Mock
) -> None:
    task_repository_mock.get_all.return_value = [
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

    result = await task_service.list_tasks()

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
    task_service: TaskService, db_mock: Mock, task_repository_mock: Mock
) -> None:
    created_task = TaskORM(
        id=UUID("00000000-0000-0000-0000-000000000001"),
        title="Новая задача",
        completed=False,
    )
    task_repository_mock.create.return_value = created_task

    result = await task_service.create_task(TaskCreateSchema(title="Новая задача"))

    task_repository_mock.create.assert_called_once_with(title="Новая задача")
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
    task_service: TaskService,
    db_mock: Mock,
    task_repository_mock: Mock,
    payload: TaskUpdateSchema,
    expected_title: str,
    expected_completed: bool,
) -> None:
    task = TaskORM(
        id=UUID("00000000-0000-0000-0000-000000000001"),
        title="Старая задача",
        completed=False,
    )
    task_repository_mock.get_by_id.return_value = task

    result = await task_service.update_task(
        UUID("00000000-0000-0000-0000-000000000001"), payload
    )

    task_repository_mock.get_by_id.assert_called_once_with(
        task_id=UUID("00000000-0000-0000-0000-000000000001")
    )
    db_mock.commit.assert_called_once_with()

    assert result.model_dump() == {
        "id": UUID("00000000-0000-0000-0000-000000000001"),
        "title": expected_title,
        "completed": expected_completed,
    }


async def test_update_task_raises_when_task_not_found(
    task_service: TaskService,
    db_mock: Mock,
    task_repository_mock: Mock,
) -> None:
    task_repository_mock.get_by_id.return_value = None

    with pytest.raises(TaskNotFound):
        await task_service.update_task(
            UUID("00000000-0000-0000-0000-000000000099"),
            TaskUpdateSchema(title="Неважно"),
        )

    db_mock.commit.assert_not_called()


async def test_delete_task(
    task_service: TaskService,
    task_repository_mock: Mock,
    db_mock: Mock,
) -> None:
    task = TaskORM(
        id=UUID("00000000-0000-0000-0000-000000000001"),
        title="Тестовая задача",
        completed=True,
    )

    task_repository_mock.get_by_id.return_value = task

    result = await task_service.delete_task(
        UUID("00000000-0000-0000-0000-000000000001")
    )

    task_repository_mock.delete.assert_called_once_with(task)
    task_repository_mock.get_by_id.assert_called_once_with(
        task_id=UUID("00000000-0000-0000-0000-000000000001")
    )
    db_mock.commit.assert_called_once_with()

    assert result is None


async def test_delete_task_raises_when_task_not_found(
    task_service: TaskService,
    task_repository_mock: Mock,
    db_mock: Mock,
) -> None:
    task_repository_mock.get_by_id.return_value = None

    with pytest.raises(TaskNotFound):
        await task_service.delete_task(
            UUID("00000000-0000-0000-0000-000000000001"),
        )

    task_repository_mock.get_by_id.assert_called_once_with(
        task_id=UUID("00000000-0000-0000-0000-000000000001")
    )
    task_repository_mock.delete.assert_not_called()
    db_mock.commit.assert_not_called()
