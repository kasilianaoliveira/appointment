from abc import abstractmethod
from fastapi_mail import MessageSchema
import fastapi_mail


class NotificationService:
    @abstractmethod
    async def send_email(
        self, subject: str, recipients: list[str], body: str, is_html: bool = False
    ):
        message = MessageSchema(
            subject=subject,
            recipients=recipients,
            body=body,
            subtype="html" if is_html else "plain",
        )
        await fastapi_mail.send_message(message)
