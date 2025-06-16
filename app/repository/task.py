from sqlalchemy import delete, insert, select, update
from sqlalchemy.orm import Session

from app.models.tasks import Categories, Tasks
from app.schema.task import Task, TaskCreateSchema
from app.exceptions import TaskNotFound


class TaskRepository:

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_tasks(self) -> Tasks | None:
        with self.db_session() as session:
            task: list[Tasks] = session.execute(select(Tasks)).scalars().all()
        return task

    async def get_task(self, task_id: int) -> Tasks | None:
        async with self.db_session as session:
            task: Tasks = (
                await session.execute(select(Tasks).where(Tasks.id == task_id))
            ).scalar_one_or_none()
        return task

    async def get_user_task(self, task_id: int, user_id: int) -> Tasks | None:
        query = (
            select(Tasks, Categories)
            .join(Categories, Categories.id == Tasks.category_id)
            .where(Tasks.id == task_id, Tasks.user_id == user_id)
        )
        async with self.db_session as session:
            task: Tasks = (await session.execute(query)).scalar_one_or_none()
        return task

    async def create_task(self, task: TaskCreateSchema, user_id: int) -> int:
        query = (
            insert(Tasks)
            .values(
                name=task.name,
                pomodoro_count=task.pomodoro_count,
                category_id=task.category_id,
                user_id=user_id,
            )
            .returning(Tasks.id)
        )
        async with self.db_session as session:
            task_id = (await session.execute(query)).scalar_one_or_none()
            await session.commit()
            return task_id

    def delete_task(self, task_id: int, user_id: int) -> None:
        query = delete(Tasks).where(Tasks.id == task_id, Tasks.user_id == user_id)
        with self.db_session() as session:
            session.execute(query)
            session.commit()

    async def get_task_by_category_name(self, category_name: str) -> list[Tasks]:
        query = (
            select(Tasks).join(Categories, Tasks.category_id == Categories.id).where(Categories.name == category_name)
        )
        async with self.db_session as session:
            task: list[Tasks] = (await session.execute(query)).scalars().all()
            return task

    async def update_task_name(self, task_id: int, name: str) -> Tasks:
        query = update(Tasks).where(Tasks.id == task_id).values(name=name).returning(Tasks.id)
        async with self.db_session as session:
            task_id: int = (await session.execute(query)).scalar_one_or_none()
            await session.commit()
            await session.flush()
            return await self.get_task(task_id)
