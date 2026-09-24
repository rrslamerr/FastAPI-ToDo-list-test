from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class TaskSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    completed: bool = False


class TaskCreateSchema(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=100,
    )


class TaskUpdateSchema(BaseModel):
    title: str | None = Field(
        min_length=1,
        max_length=100,
        default=None,
    )
    completed: bool | None = None
