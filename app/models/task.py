from sqlalchemy import CheckConstraint, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class TaskORM(Base):
    __tablename__ = "tasks"

    title: Mapped[str] = mapped_column(String(100))
    completed: Mapped[bool] = mapped_column(default=False)

    __table_args__ = (CheckConstraint("length(title) > 0", name="check_title_length"),)
