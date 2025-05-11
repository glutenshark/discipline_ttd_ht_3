from datetime import datetime
from task_manager.models import Task
from task_manager.repositories import TaskRepository, ProjectRepository

class TaskService:
    """
    Сервис для операций над задачами:
    - create_task
    - track_time
    - check_project_deadline
    """
    def __init__(self, task_repo: TaskRepository, project_repo: ProjectRepository):
        self._task_repo = task_repo
        self._project_repo = project_repo

    def create_task(self, project_id: int, title: str, deadline: datetime) -> int:
        """
        Создаёт новую задачу и возвращает её уникальный идентификатор (int).
        Бросает ValueError, если проект не найден или дедлайн в прошлом.
        """
        if deadline < datetime.now():
            raise ValueError("Нельзя задать дедлайн в прошлом.")
        # Проверяем наличие проекта
        try:
            self._project_repo.get_project(project_id)
        except KeyError:
            raise ValueError(f"Проект с id={project_id} не найден.")
        # Создаём объект Task (dataclass)
        new_task = Task(project_id=project_id, title=title, deadline=deadline)
        new_id = self._task_repo.add_task(new_task)
        return new_id

    def track_time(self, task_id: int, hours: float) -> float:
        """
        Добавляет указанное число часов к задаче.
        Возвращает итоговое значение hours_spent по задаче.
        """
        if hours <= 0:
            raise ValueError("Нельзя добавить неположительное число часов.")
        # Проверяем, есть ли такая задача
        try:
            task = self._task_repo.get_task(task_id)
        except KeyError:
            raise ValueError(f"Задача с id={task_id} не найдена.")
        task.hours_spent += hours
        return task.hours_spent

    def check_project_deadline(self, project_id: int) -> bool:
        """
        Возвращает True, если проект просрочен (дедлайн уже прошел), и False в остальных случаях.
        Бросает ValueError, если проект не найден.
        """
        try:
            project = self._project_repo.get_project(project_id)
        except KeyError:
            raise ValueError(f"Проект с id={project_id} не найден.")
        if project.deadline is None:
            return False
        return datetime.now() > project.deadline


class InvoiceService:
    """
    Сервис для расчёта счета (calculate_invoice).
    Фиктивно поддерживает список валют, а фактический расчёт — hours * rate.
    """
    SUPPORTED_CURRENCIES = {"USD", "EUR", "GBP", "RUB"}

    def calculate_invoice(self, hours: float, rate: float, currency: str) -> float:
        """
        Рассчитывает оплату: hours * rate, если валюта поддерживается.
        Бросает ValueError при отрицательных значениях или неподдерживаемой валюте.
        """
        if hours < 0:
            raise ValueError("Количество часов не может быть отрицательным.")
        if rate < 0:
            raise ValueError("Ставка (rate) не может быть отрицательной.")
        if currency not in self.SUPPORTED_CURRENCIES:
            raise ValueError(f"Валюта {currency} не поддерживается.")
        return hours * rate
