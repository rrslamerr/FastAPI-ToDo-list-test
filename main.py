from contextlib import asynccontextmanager
from uuid import uuid4

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, select
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    sessionmaker,
)

DATABASE_URL = "postgresql+psycopg://postgres:admin@127.0.0.1:15432/postgres"
engine = create_engine(DATABASE_URL)
Sessionlocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    id: Mapped[str] = mapped_column(
        primary_key=True, default=lambda: str(uuid4())
    )


class TaskORM(Base):
    __tablename__ = "tasks"

    title: Mapped[str]
    completed: Mapped[bool] = mapped_column(default=False)


class CategoryORM(Base):
    __tablename__ = "categories"

    name: Mapped[str]


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
)


class TaskSchema(BaseModel):
    id: str
    title: str
    completed: bool = False


class TaskCreateSchema(BaseModel):
    title: str


class TaskUpdateSchema(BaseModel):
    title: str | None = None
    completed: bool | None = None


class CategorySchema(BaseModel):
    id: str
    name: str


class CategoryCreateSchema(BaseModel):
    name: str


class CategoryUpdateSchema(BaseModel):
    name: str | None = None


def get_db():
    db = Sessionlocal()
    try:
        yield db
    finally:
        db.close()


def task_orm_to_model(task_orm: TaskORM) -> TaskSchema:
    return TaskSchema(
        id=task_orm.id,
        title=task_orm.title,
        completed=task_orm.completed,
    )


def category_orm_to_model(category_orm: CategoryORM) -> CategorySchema:
    return CategorySchema(
        id=category_orm.id,
        name=category_orm.name,
    )


@app.get("/tasks")
def read_tasks(db: Session = Depends(get_db)) -> list[TaskSchema]:
    tasks_from_db = db.scalars(select(TaskORM)).all()
    return [task_orm_to_model(task) for task in tasks_from_db]


@app.post("/tasks", status_code=status.HTTP_201_CREATED)
def create_task(
    payload: TaskCreateSchema, db: Session = Depends(get_db)
) -> TaskSchema:
    new_task = TaskORM(title=payload.title, completed=False)
    db.add(new_task)
    db.commit()
    return task_orm_to_model(new_task)


@app.patch("/tasks/{task_id}")
def update_task(
    task_id: str, payload: TaskUpdateSchema, db: Session = Depends(get_db)
) -> TaskSchema:
    task_for_update = db.get(TaskORM, task_id)
    if task_for_update is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task not found"
        )
    if payload.title is not None:
        task_for_update.title = payload.title
    if payload.completed is not None:
        task_for_update.completed = payload.completed
    db.commit()
    return task_orm_to_model(task_for_update)


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str):
    for task in tasks:
        if task.id == task_id:
            tasks.remove(task)


@app.get("/categories")
def read_categories() -> list[CategorySchema]:
    return categories


@app.post("/categories", status_code=status.HTTP_201_CREATED)
def create_category(payload: CategoryCreateSchema) -> CategorySchema:
    new_category = CategorySchema(id=str(uuid4()), name=payload.name)
    categories.append(new_category)
    return new_category


@app.patch("/categories/{category_id}")
def update_category(category_id: str, payload: CategoryUpdateSchema):
    for category in categories:
        if category.id == category_id:
            if payload.name:
                category.name = payload.name
            return category
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
    )


@app.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: str):
    for category in categories:
        if category.id == category_id:
            categories.remove(category)
            return
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail="Category not found"
    )
