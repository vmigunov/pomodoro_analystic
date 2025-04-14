from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.database import get_db_session
from app.database.models import Categories, Tasks


class TaskRepository:

    def __init__(self, db_session: Session):
        self.db_session = db.session

    def get_tasks(self) -> Tasks | None:
        with self.db_session() as session:
            task: list[Tasks] = session.execute(select(Tasks)).scalars().all()
        return task

    def get_task(self, task_id: int) -> Tasks | None:
        with self.db_session() as session:
            task: list[Tasks] = session.execute(
                select(Tasks).where(Tasks.id == task_id)
            ).scalar_one_or_none()

    
    def create_task(self, task: Tasks) -> None:
        with self.db_session() as session:
            session.add(task)
            session.commit()


    def delete_rask(self, task_id: int) -> None:
        query = delete(Tasks).where(Tasks.id == task_id)
        with self.db_session() as session:
            session.execute(query)
            session.commit()

    
    def get_task_by_category_name(self, category_name: str) -> list[Tasks]:
        query = select(Tasks).join(Categories, Tasks.category_id == Categories.id)

def get_tasks_repository():
    db_session = get_db_session()
    return TaskRepository(db_session)
