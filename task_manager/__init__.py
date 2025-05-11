from datetime import datetime, date

from task_manager.models import Project, Task
from task_manager.repositories import (
    InMemoryProjectRepository,
    InMemoryTaskRepository
)
from task_manager.notifications import NotificationService
from task_manager.services import TaskService, InvoiceService

# Инициализация хранилищ (in-memory реализация)
task_repo = InMemoryTaskRepository()
project_repo = InMemoryProjectRepository()

# Инициализация бизнес-сервисов
task_service = TaskService(task_repo, project_repo)
invoice_service = InvoiceService()
notification_service = NotificationService()


def create_task(project_id: int, title: str, deadline: datetime) -> int:
    """
    Создаёт задачу в рамках проекта.

    Args:
        project_id (int): Идентификатор проекта.
        title (str): Название задачи.
        deadline (datetime): Дата и время дедлайна.

    Returns:
        int: ID созданной задачи.
    """
    return task_service.create_task(project_id, title, deadline)


def track_time(task_id: int, hours: float) -> float:
    """
    Добавляет количество часов к задаче.

    Args:
        task_id (int): Идентификатор задачи.
        hours (float): Количество часов.

    Returns:
        float: Общее количество часов после добавления.
    """
    return task_service.track_time(task_id, hours)


def calculate_invoice(hours: float, rate: float, currency: str) -> float:
    """
    Рассчитывает сумму счёта за выполненные часы.

    Args:
        hours (float): Количество часов.
        rate (float): Ставка за час.
        currency (str): Валюта (например, 'USD').

    Returns:
        float: Рассчитанная сумма.
    """
    return invoice_service.calculate_invoice(hours, rate, currency)


def check_project_deadline(project_id: int) -> bool:
    """
    Проверяет, просрочен ли проект.

    Args:
        project_id (int): Идентификатор проекта.

    Returns:
        bool: True, если дедлайн не наступил или не установлен.
    """
    return task_service.check_project_deadline(project_id)


def send_task_notification(email: str, task_info: dict) -> bool:
    """
    Отправляет email-уведомление по задаче.

    Args:
        email (str): Email получателя.
        task_info (dict): Информация о задаче.

    Returns:
        bool: True при успешной отправке, False при ошибке.
    """
    return notification_service.send_task_notification(email, task_info)
