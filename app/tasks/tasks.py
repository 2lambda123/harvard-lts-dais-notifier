from celery import Celery
import os
from notifier.dais_notifier import SmtpMailingService
import logging

app = Celery()
app.config_from_object('celeryconfig')

logger = logging.getLogger('dais-notifier')
retries = os.getenv('MESSAGE_MAX_RETRIES', 3)

@app.task(serializer='json', name='notifier.tasks.send_email', max_retries=retries)
def send_email(message_body):
    try:
        subject = message_body["subject"]
        body = message_body["body"]
        recipients = message_body.get("recipients")
        mailing_service = SmtpMailingService()
        mailing_service.send_email(subject,body, recipients)
            
    except Exception:
        logger.exception(
            "Could not send message {}".format(message_body.get("destination_path"))
        )
