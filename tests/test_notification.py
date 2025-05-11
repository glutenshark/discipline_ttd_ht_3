import pytest
import smtplib
import time
from datetime import datetime, timedelta
from aiosmtpd.controller import Controller

from task_manager.notifications import NotificationService


class CaptureHandler:
    """
    Обработчик писем для встроенного SMTP-сервера в тесте.

    Сохраняет полученные сообщения для последующей проверки.
    """

    def __init__(self):
        self.messages = []

    async def handle_DATA(self, server, session, envelope):
        content = envelope.content
        if isinstance(content, bytes):
            content = content.decode('utf-8', errors='replace')
        self.messages.append({
            "from": envelope.mail_from,
            "to": envelope.rcpt_tos,
            "data": content
        })
        return '250 OK'


def test_send_task_notification_success():
    """
    Проверяет успешную отправку письма через локальный SMTP-сервер.

    Ожидается, что NotificationService вернёт True и письмо будет доставлено.
    """
    handler = CaptureHandler()
    controller = Controller(handler, hostname='localhost', port=8025)
    controller.start()
    time.sleep(0.2)  # Дать серверу подняться

    try:
        service = NotificationService(smtp_host='localhost', smtp_port=8025)
        task_info = {
            "title": "Test Task",
            "deadline": datetime.now() + timedelta(days=1),
            "completed": False
        }
        result = service.send_task_notification("test@example.com", task_info)

        assert result is True
        assert len(handler.messages) == 1

        message = handler.messages[0]
        assert message["from"] == "no-reply@example.com"
        assert "test@example.com" in message["to"]
        assert "Test Task" in message["data"]
        assert "создана" in message["data"]
    finally:
        controller.stop()


def test_send_task_notification_invalid_email():
    """
    Проверяет поведение при передаче некорректного email-адреса.

    Метод должен вернуть False.
    """
    service = NotificationService()
    task_info = {"title": "Bad Email"}
    result = service.send_task_notification("bad-email", task_info)
    assert result is False


def test_send_task_notification_smtp_failure(monkeypatch):
    """
    Проверяет поведение при сбое соединения с SMTP-сервером.

    Эмулируется сбой через подмену smtplib.SMTP. Ожидается False.
    """
    class DummySMTP:
        def __init__(self, host, port):
            raise ConnectionRefusedError("SMTP server not available")

    monkeypatch.setattr(smtplib, "SMTP", DummySMTP)

    service = NotificationService()
    task_info = {"title": "Error Test"}
    result = service.send_task_notification("test@example.com", task_info)
    assert result is False
