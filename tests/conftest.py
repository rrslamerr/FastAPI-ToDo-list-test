from unittest.mock import Mock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.task import TaskRepository
from app.services.task import TaskService


@pytest.fixture
def db_mock() -> Mock:
    return Mock(spec=AsyncSession)


@pytest.fixture
def repository_mock() -> Mock:
    return Mock(spec=TaskRepository)


@pytest.fixture
def service(db_mock: Mock, repository_mock: Mock) -> TaskService:
    task_service = TaskService(db_mock)
    task_service.task_repository = repository_mock
    return task_service
