import pytest
from datetime import datetime, timedelta

import task_manager


def test_create_task_success():
    """
    Проверяет создание задачи при корректных данных.

    Ожидается: возвращается int, данные сохраняются правильно.
    """
    project = task_manager.models.Project(
        name="TestProject",
        deadline=datetime.now() + timedelta(days=2)
    )
    pid = task_manager.project_repo.add_project(project)
    deadline = datetime.now() + timedelta(days=1)

    tid = task_manager.create_task(pid, "Some Task", deadline)

    assert isinstance(tid, int)

    stored = task_manager.task_repo.get_task(tid)
    assert stored.title == "Some Task"
    assert stored.project_id == pid
    assert stored.deadline == deadline


def test_create_task_project_not_found():
    """
    Проверяет, что при несуществующем проекте возникает ValueError.
    """
    with pytest.raises(ValueError):
        task_manager.create_task(9999, "Fake", datetime.now() + timedelta(days=1))


def test_create_task_deadline_in_past():
    """
    Проверяет, что нельзя создать задачу с дедлайном в прошлом.
    """
    project = task_manager.models.Project(
        name="AnyProj",
        deadline=datetime.now() + timedelta(days=3)
    )
    pid = task_manager.project_repo.add_project(project)

    with pytest.raises(ValueError):
        task_manager.create_task(pid, "Past Task", datetime.now() - timedelta(days=1))


def test_create_task_empty_title():
    """
    Проверяет, что пустой заголовок вызывает ValueError.
    """
    project = task_manager.models.Project(
        name="ProjectX",
        deadline=datetime.now() + timedelta(days=1)
    )
    pid = task_manager.project_repo.add_project(project)

    with pytest.raises(ValueError):
        task_manager.create_task(pid, "", datetime.now() + timedelta(hours=2))


def test_track_time_basic():
    """
    Проверяет увеличение часов по задаче.

    Ожидается: общее время накапливается корректно.
    """
    project = task_manager.models.Project(
        name="TimeTracker",
        deadline=datetime.now() + timedelta(days=1)
    )
    pid = task_manager.project_repo.add_project(project)
    tid = task_manager.create_task(pid, "Timed", datetime.now() + timedelta(hours=3))

    total = task_manager.track_time(tid, 2.0)
    assert total == 2.0

    total_again = task_manager.track_time(tid, 1.5)
    assert total_again == 3.5


def test_track_time_negative():
    """
    Проверяет реакцию на отрицательное значение часов.

    Ожидается: ValueError.
    """
    project = task_manager.models.Project(
        name="TimeCheck",
        deadline=datetime.now() + timedelta(days=1)
    )
    pid = task_manager.project_repo.add_project(project)
    tid = task_manager.create_task(pid, "NegativeTime", datetime.now() + timedelta(hours=4))

    with pytest.raises(ValueError):
        task_manager.track_time(tid, -2.0)


def test_track_time_task_not_found():
    """
    Проверяет поведение при передаче несуществующего ID задачи.

    Ожидается: ValueError.
    """
    with pytest.raises(ValueError):
        task_manager.track_time(123456, 1.0)
