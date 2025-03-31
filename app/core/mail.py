from fastapi_mail import FastMail, ConnectionConfig, MessageSchema, MessageType
from app.core.config import settings
from pathlib import Path
import resend
from typing import List

BASE_DIR = Path(__file__).resolve().parent

# FastAPI-Mail Configuration
mail_config = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.MAIL_FROM_NAME,
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True,
    # TEMPLATE_FOLDER=Path(BASE_DIR, "templates"),
)

mail = FastMail(config=mail_config)

# Resend Email API Key
resend.api_key = settings.RESEND_API_KEY


async def send_email(
    recipients: List[str], subject: str, body: str, use_resend: bool = False
):
    """
    Sends an email using either FastAPI-Mail or Resend.

    - `recipients`: List of recipient emails
    - `subject`: Email subject
    - `body`: HTML body content
    - `use_resend`: If `True`, send via Resend, else use FastAPI-Mail
    """
    if use_resend:
        # Sending email via Resend API
        params: resend.Emails.SendParams = {
            "from": settings.RESEND_MAIL_FROM,  # Ensure it's a verified sender
            "to": recipients,
            "subject": subject,
            "html": body,
        }
        try:
            email_response = resend.Emails.send(params)
            return {"status": "success", "provider": "resend", "response": email_response}
        except Exception as e:
            return {"status": "error", "provider": "resend", "error": str(e)}

    else:
        # Sending email via FastAPI-Mail
        message = MessageSchema(
            recipients=recipients, subject=subject, body=body, subtype=MessageType.html
        )
        try:
            await mail.send_message(message)
            return {"status": "success", "provider": "fastapi-mail"}
        except Exception as e:
            return {"status": "error", "provider": "fastapi-mail", "error": str(e)}


async def send_multiple_emails(recipients: List[str], subject: str, body: str):
    """
    Send multiple emails using Resend only
    - `recipients`: List of recipient emails
    - `subject`: Email subject
    - `body`: HTML body content
    """
    params: List[resend.Emails.SendParams] = []
    for recipient_email in recipients:
        params.append({
            "from": settings.RESEND_MAIL_FROM,
            "to": [recipient_email],
            "subject": subject,
            "html": body,
        })
    resend.Batch.send(params)
