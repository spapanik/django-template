import logging
import re
from collections.abc import Iterable
from dataclasses import dataclass
from smtplib import SMTPException

from django.conf import settings
from django.core.mail import EmailMultiAlternatives, get_connection

from {{cookiecutter.project_name}}.users.models import User

CAPITAL_SPLIT = re.compile("[A-Z][^A-Z]*")
PREVIEW_LENGTH = 300
SUFFIXES = {"html": ".html", "plain": ".txt"}


logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Attachment:
    name: str
    content: str
    mimetype: str


class TransactionalEmail:

    @classmethod
    def send_email(
        cls,
        recipient: User,
        subject: str,
        message: str,
        html_message: str = "",
        attachments: Iterable[Attachment] = (),
    ) -> bool:
        mail = EmailMultiAlternatives(
            subject,
            message,
            f"noreply@{settings.BARE_DOMAIN}",
            [recipient.email],
            connection=get_connection(),
        )
        if html_message:
            mail.attach_alternative(html_message, "text/html")

        for attachment in attachments:
            mail.attach(attachment.name, attachment.content, attachment.mimetype)

        try:
            number_sent = mail.send()
        except SMTPException:
            success = False
        else:
            success = bool(number_sent)

        logger.info(
            "Attempted to sent % to %s with subject (success: %s).",
            cls.__qualname__,
            recipient.email,
            success,
        )
        return success
