import pytest
from datetime import datetime, timedelta

import task_manager


def test_check_project_deadline_not_overdue():
    """
    Возвращает False, если дедлайн ещё не наступил.

    Создаётся проект с дедлайном в будущем.
    """
    future = datetime.now() + timedelta(days=1)
    project = task_manager.models.Project(name="FutureProj", deadline=future)
    pid = task_manager.project_repo.add_project(project)
    assert task_manager.check_project_deadline(pid) is False


def test_check_project_deadline_overdue():
    """
    Возвращает True, если дедлайн уже прошёл.

    Создаётся проект с дедлайном в прошлом.
    """
    past = datetime.now() - timedelta(days=1)
    project = task_manager.models.Project(name="PastProj", deadline=past)
    pid = task_manager.project_repo.add_project(project)
    assert task_manager.check_project_deadline(pid) is True


def test_check_project_deadline_none():
    """
    Возвращает False, если у проекта нет дедлайна.

    Проверяется поведение без заданной даты.
    """
    project = task_manager.models.Project(name="NoDeadline", deadline=None)
    pid = task_manager.project_repo.add_project(project)
    assert task_manager.check_project_deadline(pid) is False


def test_check_project_deadline_not_found():
    """
    При попытке проверить несуществующий проект выбрасывается ValueError.
    """
    with pytest.raises(ValueError):
        task_manager.check_project_deadline(999999)
