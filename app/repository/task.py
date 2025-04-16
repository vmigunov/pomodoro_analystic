from sqlalchemy import delete, select, update
from sqlalchemy.orm import Session

from app.database.database import get_db_session
from app.database.models import Categories, Tasks
from app.schema.task import Task


class TaskRepository:

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_tasks(self) -> Tasks | None:
        with self.db_session() as session:
            task: list[Tasks] = session.execute(select(Tasks)).scalars().all()
        return task

    def get_task(self, task_id: int) -> Tasks | None:
        with self.db_session() as session:
            task: list[Tasks] = session.execute(
                select(Tasks).where(Tasks.id == task_id)
            ).scalar_one_or_none()
        return task

    def create_task(self, task: Task) -> int:
        task_model = Tasks(
            name=task.name,
            pomodoro_count=task.pomodoro_count,
            category_id=task.category_id,
        )
        with self.db_session() as session:
            session.add(task_model)
            session.commit()

    def delete_task(self, task_id: int) -> None:
        query = delete(Tasks).where(Tasks.id == task_id)
        with self.db_session() as session:
            session.execute(query)
            session.commit()

    def get_task_by_category_name(self, category_name: str) -> list[Tasks]:
        query = select(Tasks).join(Categories, Tasks.category_id == Categories.id)
        return query

    def update_task_name(self, task_id: int, name: str) -> Tasks:
        query = (
            update(Tasks)
            .where(Tasks.id == task_id)
            .values(name=name)
            .returning(Tasks.id)
        )
        with self.db_session() as session:
            task_id: int = session.execute(query).scalar_one_or_none()
            session.commit()
            return self.get_task(task_id)
