import os
from fastapi import BackgroundTasks
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from core.settings import settings
from schemas.auth import EmailSchema


conf = ConnectionConfig(
    MAIL_USERNAME=settings.MAIL_USERNAME,
    MAIL_PASSWORD=settings.MAIL_PASSWORD,
    MAIL_FROM=settings.MAIL_FROM,
    MAIL_PORT=settings.MAIL_PORT,
    MAIL_SERVER=settings.MAIL_SERVER,
    MAIL_FROM_NAME=settings.PROJECT_TITLE,
    TEMPLATE_FOLDER=f"{os.path.dirname(os.path.dirname(os.path.realpath(__file__)))}/templates",
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True
)


def send_mail(background_tasks: BackgroundTasks, subject: str, emails: EmailSchema, template_name: str):
    message = MessageSchema(
        subject=subject,
        recipients=emails.emails,
        template_body=emails.body,
        subtype='html',
    )

    fm = FastMail(conf)
    background_tasks.add_task(fm.send_message, message,
                              template_name=template_name)
