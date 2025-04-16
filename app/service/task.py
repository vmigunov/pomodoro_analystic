from dataclasses import dataclass
from app.repository import TaskRepository, TaskCache
from app.schema.task import Task


@dataclass
class TaskService:
    task_repository: TaskRepository
    task_cache: TaskCache

    def get_tasks(self):
        if cache_tasks := self.task_cache.get_tasks():
            return cache_tasks
        else:
            tasks = self.task_repository.get_tasks()
            tasks_schema = [Task.model_validate(task) for task in tasks]
            self.task_cache.set_tasks(tasks_schema)
            return tasks_schema
