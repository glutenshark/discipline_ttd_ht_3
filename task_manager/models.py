from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class Task:
    """
    Модель данных задачи.

    Атрибуты:
        id (Optional[int]): Идентификатор задачи. Устанавливается автоматически.
        project_id (int): ID проекта, к которому относится задача.
        title (str): Название задачи.
        deadline (datetime): Дедлайн задачи.
        hours_spent (float): Общее количество отработанных часов.
    """
    id: Optional[int] = field(init=False, default=None)
    project_id: int = 0
    title: str = ""
    deadline: datetime = None
    hours_spent: float = 0.0

    def __post_init__(self):
        """Проверка типов и значений полей после инициализации."""
        if not isinstance(self.project_id, int):
            raise TypeError("project_id должен быть целым числом.")
        if not isinstance(self.title, str):
            raise TypeError("title должен быть строкой.")
        if self.title.strip() == "":
            raise ValueError("title не может быть пустым.")
        if not isinstance(self.deadline, datetime):
            raise TypeError("deadline должен быть экземпляром datetime.")
        if not isinstance(self.hours_spent, (int, float)):
            raise TypeError("hours_spent должен быть числом.")
        if self.hours_spent < 0:
            raise ValueError("hours_spent не может быть отрицательным.")


@dataclass
class Project:
    """
    Модель данных проекта.

    Атрибуты:
        id (Optional[int]): Идентификатор проекта. Устанавливается автоматически.
        name (str): Название проекта.
        deadline (Optional[datetime]): Дедлайн проекта. Может быть None.
    """
    id: Optional[int] = field(init=False, default=None)
    name: str = "Untitled"
    deadline: Optional[datetime] = None

    def __post_init__(self):
        """Проверка типов полей после инициализации."""
        if not isinstance(self.name, str):
            raise TypeError("name должен быть строкой.")
        if self.deadline is not None and not isinstance(self.deadline, datetime):
            raise TypeError("deadline должен быть datetime или None.")
