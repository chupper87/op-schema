from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from ..core.settings import settings


class EmailService:
    def __init__(self):
        self.conf = ConnectionConfig(
            MAIL_USERNAME=settings.SMTP_USERNAME,
            MAIL_PASSWORD=settings.SMTP_PASSWORD,
            MAIL_FROM=settings.SMTP_FROM,
            MAIL_PORT=settings.SMTP_PORT,
            MAIL_SERVER=settings.SMTP_SERVER,
            MAIL_STARTTLS=True,
            MAIL_SSL_TLS=False,
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=True,
        )

    async def send_invitation_email(self, to_email: str, token: str):
        message = MessageSchema(
            subject="Timepiece invitation",
            recipients=[to_email],
            body=f"Registration link: {settings.BASE_URL}/register?token={token}",
            subtype=MessageType.html,
        )

        fm = FastMail(self.conf)
        await fm.send_message(message)
