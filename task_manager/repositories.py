from abc import ABC, abstractmethod
from typing import Dict
import uuid

from task_manager.models import Task, Project


class TaskRepository(ABC):
    """
    Абстрактный репозиторий задач.

    Определяет интерфейс для операций с задачами.
    """

    @abstractmethod
    def add_task(self, task: Task) -> int:
        """
        Добавляет задачу и возвращает её ID.

        Args:
            task (Task): Экземпляр задачи.

        Returns:
            int: Присвоенный ID задачи.
        """
        pass

    @abstractmethod
    def get_task(self, task_id: int) -> Task:
        """
        Возвращает задачу по ID.

        Args:
            task_id (int): Идентификатор задачи.

        Returns:
            Task: Объект задачи.
        """
        pass

    @abstractmethod
    def clear(self):
        """
        Удаляет все задачи из репозитория.
        """
        pass


class ProjectRepository(ABC):
    """
    Абстрактный репозиторий проектов.

    Определяет интерфейс для операций с проектами.
    """

    @abstractmethod
    def add_project(self, project: Project) -> int:
        """
        Добавляет проект и возвращает его ID.

        Args:
            project (Project): Экземпляр проекта.

        Returns:
            int: Присвоенный ID проекта.
        """
        pass

    @abstractmethod
    def get_project(self, project_id: int) -> Project:
        """
        Возвращает проект по ID.

        Args:
            project_id (int): Идентификатор проекта.

        Returns:
            Project: Объект проекта.
        """
        pass

    @abstractmethod
    def clear(self):
        """
        Удаляет все проекты из репозитория.
        """
        pass


class InMemoryTaskRepository(TaskRepository):
    """
    Реализация TaskRepository в оперативной памяти.
    """

    def __init__(self):
        self._tasks: Dict[int, Task] = {}

    def add_task(self, task: Task) -> int:
        new_id = uuid.uuid4().int
        task.id = new_id
        self._tasks[new_id] = task
        return new_id

    def get_task(self, task_id: int) -> Task:
        if task_id not in self._tasks:
            raise KeyError(f"Задача с id={task_id} не найдена.")
        return self._tasks[task_id]

    def clear(self):
        self._tasks.clear()


class InMemoryProjectRepository(ProjectRepository):
    """
    Реализация ProjectRepository в оперативной памяти.
    """

    def __init__(self):
        self._projects: Dict[int, Project] = {}

    def add_project(self, project: Project) -> int:
        new_id = uuid.uuid4().int
        project.id = new_id
        self._projects[new_id] = project
        return new_id

    def get_project(self, project_id: int) -> Project:
        if project_id not in self._projects:
            raise KeyError(f"Проект с id={project_id} не найден.")
        return self._projects[project_id]

    def clear(self):
        self._projects.clear()
