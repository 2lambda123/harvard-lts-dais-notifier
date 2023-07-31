import os

broker_url = os.getenv('BROKER_URL')
task_serializer = 'json'
accept_content = ['application/json']
result_serializer = 'json'
timezone = 'US/Eastern'
enable_utc = True
worker_enable_remote_control = False
task_routes = {
    'notifier.tasks.send_email':
        {'queue': os.getenv("CONSUME_QUEUE_NAME")}
}
