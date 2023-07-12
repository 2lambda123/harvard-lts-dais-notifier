from celery import Celery
import os

app1 = Celery('tasks')
app1.config_from_object('celeryconfig')

arguments = {
            "subject": "Notifier Test Email",
            "body": "Notifier Test Email Body"
        }

res = app1.send_task('notifier.tasks.send_email',
                     args=[arguments], kwargs={},
                     queue=os.getenv("CONSUME_QUEUE_NAME"))
