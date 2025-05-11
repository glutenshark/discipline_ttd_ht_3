import re
import smtplib
from datetime import datetime


class NotificationService:
    """
    Сервис отправки email-уведомлений по задачам.

    Использует SMTP или подменяемый клиент (например, в тестах).
    """

    def __init__(self, smtp_host: str = "localhost", smtp_port: int = 25,
                 use_tls: bool = False, mailer=None):
        """
        Инициализация сервиса отправки.

        Args:
            smtp_host (str): Адрес SMTP-сервера.
            smtp_port (int): Порт SMTP-сервера.
            use_tls (bool): Использовать TLS-соединение.
            mailer (Optional): Класс SMTP-клиента для замены (используется в тестах).
        """
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.mailer = mailer if mailer is not None else (
            smtplib.SMTP_SSL if use_tls else smtplib.SMTP
        )

    def send_task_notification(self, email: str, task_info: dict) -> bool:
        """
        Отправляет уведомление о задаче на указанный email.

        Args:
            email (str): Email-адрес получателя.
            task_info (dict): Информация о задаче, включая title, deadline и completed.

        Returns:
            bool: True — при успешной отправке, False — в случае ошибки.
        """
        if not self._is_valid_email(email):
            return False

        status = "создана"
        completed = task_info.get("completed", False)
        deadline = task_info.get("deadline")

        if completed:
            status = "завершена"
        elif isinstance(deadline, datetime):
            if deadline < datetime.now():
                status = "просрочена"

        title = task_info.get("title", "")
        subject = "Notification: Task Update"
        body = f'Задача "{title}" {status}.'

        message = (
            f"From: no-reply@example.com\r\n"
            f"To: {email}\r\n"
            f"Subject: {subject}\r\n\r\n"
            f"{body}"
        )

        try:
            with self.mailer(self.smtp_host, self.smtp_port) as smtp:
                smtp.sendmail("no-reply@example.com", [email], message.encode("utf-8"))
            return True
        except Exception:
            return False

    def _is_valid_email(self, email: str) -> bool:
        """
        Проверка формата email через регулярное выражение.

        Args:
            email (str): Email для проверки.

        Returns:
            bool: True — если email валиден.
        """
        return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))


class StubMailSender:
    """
    Тестовая реализация отправщика email-сообщений.

    Ничего не отправляет, сохраняет данные для проверки.
    """

    def __init__(self):
        self.sent = []

    def send(self, to_address: str, subject: str, body: str):
        """
        Сохраняет отправленные параметры в список.

        Args:
            to_address (str): Получатель.
            subject (str): Тема письма.
            body (str): Текст письма.

        Returns:
            bool: Всегда True (симулируется успешная отправка).
        """
        self.sent.append({
            "to": to_address,
            "subject": subject,
            "body": body
        })
        return True
