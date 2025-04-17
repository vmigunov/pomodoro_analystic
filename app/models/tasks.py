from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column

from app.database.database import Base


class Tasks(Base):
    __tablename__ = "Tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    pomodoro_count: Mapped[int]
    category_id: Mapped[int] = mapped_column(nullable=True)


class Categories(Base):
    __tablename__ = "Categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
