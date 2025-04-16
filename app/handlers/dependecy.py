from app.database.database import get_db_session
from app.repository.task import TaskRepository


def get_tasks_repository():
    db_session = get_db_session()
    return TaskRepository(db_session)
