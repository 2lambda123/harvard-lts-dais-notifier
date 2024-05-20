from celery import Celery
from celery import bootsteps
from celery.signals import worker_ready
from celery.signals import worker_shutdown
import os
from notifier.dais_notifier import SmtpMailingService
import logging
from pathlib import Path

app = Celery()
app.config_from_object('celeryconfig')

logger = logging.getLogger('dais-notifier')
retries = os.getenv('MESSAGE_MAX_RETRIES', 3)

# heartbeat setup
# code is from
# https://github.com/celery/celery/issues/4079#issuecomment-1270085680
hbeat_path = os.getenv("HEARTBEAT_FILE", "/tmp/worker_heartbeat")
ready_path = os.getenv("READINESS_FILE", "/tmp/worker_ready")
update_interval = float(os.getenv("HEALTHCHECK_UPDATE_INTERVAL", 60.0))
HEARTBEAT_FILE = Path(hbeat_path)
READINESS_FILE = Path(ready_path)
UPDATE_INTERVAL = update_interval  # touch file every 15 seconds

class LivenessProbe(bootsteps.StartStopStep):
    requires = {'celery.worker.components:Timer'}

    def __init__(self, worker, **kwargs):  # pragma: no cover
        self.requests = []
        self.tref = None

    def start(self, worker):  # pragma: no cover
        self.tref = worker.timer.call_repeatedly(
            UPDATE_INTERVAL, self.update_heartbeat_file,
                (worker,), priority=10,
        )

    def stop(self, worker):  # pragma: no cover
        HEARTBEAT_FILE.unlink(missing_ok=True)

    def update_heartbeat_file(self, worker):  # pragma: no cover
        HEARTBEAT_FILE.touch()

@worker_ready.connect
def worker_ready(**_):  # pragma: no cover
    READINESS_FILE.touch()

@worker_shutdown.connect
def worker_shutdown(**_):  # pragma: no cover
    READINESS_FILE.unlink(missing_ok=True)

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
