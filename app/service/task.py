from dataclasses import dataclass

from app.repository import TaskRepository, TaskCache
from app.schema.task import Task, TaskCreateSchema


@dataclass
class TaskService:
    task_repository: TaskRepository
    task_cache: TaskCache

    async def get_tasks(self) -> list[Task]:
        if cache_tasks := await self.task_cache.get_tasks():
            return cache_tasks
        else:
            tasks = self.task_repository.get_tasks()
            tasks_schema = [Task.model_validate(task) for task in tasks]
            await self.task_cache.set_tasks(tasks_schema)
            return tasks_schema

    def create_task(self, body: TaskCreateSchema, user_id: int) -> Task:
        task_id = self.task_repository.create_task(body, user_id)
        task = self.task_repository.get_task(task_id)
        return Task.model_validate(task)

    def update_task_name(self, task_id: int, name: str, user_id: int) -> Task:
        task = self.task_repository.get_user_task(user_id=user_id, task_id=task_id)
        if not task:
            raise ValueError("Task not found")
        task = self.task_repository.update_task_name(task_id=task_id, name=name)
        return Task.model_validate(task)

    def delete_task(self, task_id: int, user_id: int) -> None:
        task = self.task_repository.get_user_task(user_id=user_id, task_id=task_id)
        if not task:
            raise ValueError("Task not found")
        self.task_repository.delete_task(task_id=task_id, user_id=user_id)
