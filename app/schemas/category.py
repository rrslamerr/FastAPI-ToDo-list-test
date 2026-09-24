from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class CategorySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str


class CategoryCreateSchema(BaseModel):
    name: str = Field(
        min_length=1,
        max_length=100,
    )


class CategoryUpdateSchema(BaseModel):
    name: str | None = Field(
        min_length=1,
        max_length=100,
        default=None,
    )
