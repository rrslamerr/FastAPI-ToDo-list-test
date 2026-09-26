from sqlalchemy import CheckConstraint, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class CategoryORM(Base):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(String(100))

    __table_args__ = (CheckConstraint("length(name) > 0", name="check_name_length"),)
