import logging
import os, os.path
from logging.handlers import TimedRotatingFileHandler

from flask import Flask, Response
from healthcheck import HealthCheck, EnvironmentDump

from app.mqresources.listener.process_notify_queue_listener import ProcessNotifyQueueListener
from app.mqresources.listener.transfer_notify_queue_listener import TransferNotifyQueueListener
from app.health.exceptions.get_current_commit_hash_exception import GetCurrentCommitHashException
from app.health.git_service import GitService

LOG_FILE_DEFAULT_PATH = "/home/appuser/logs/dais_notifier.log"
LOG_FILE_DEFAULT_LEVEL = logging.DEBUG
LOG_FILE_MAX_SIZE_BYTES = 2 * 1024 * 1024
LOG_FILE_BACKUP_COUNT = 1
LOG_ROTATION = "midnight"

APPLICATION_MAINTAINER = "Harvard Library Technology Services"
APPLICATION_GIT_REPOSITORY = "https://github.com/harvard-lts/dais-notifier"

instance = os.getenv("ENV", "development")

logger = logging.getLogger('dais-notifier')

#Only print important information for the root and stomp loggers
logging.getLogger("stomp.py").setLevel(logging.WARNING)
logging.getLogger().setLevel(logging.WARNING)

def create_app() -> Flask:
    configure_logger()
    setup_queue_listeners()

    app = Flask(__name__)
    setup_health_check(app)
    disable_cached_responses(app)

    return app


def configure_logger() -> None:
    
    log_file_path = os.getenv('LOGFILE_PATH', LOG_FILE_DEFAULT_PATH)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    file_handler = TimedRotatingFileHandler(
        filename=log_file_path,
        when=LOG_ROTATION,
        backupCount=LOG_FILE_BACKUP_COUNT
    )
    logger.addHandler(file_handler)
    file_handler.setFormatter(formatter)
    log_level = os.getenv('LOG_LEVEL', LOG_FILE_DEFAULT_LEVEL)
    logger.setLevel(log_level)


def setup_queue_listeners() -> None:
    ProcessNotifyQueueListener()
    TransferNotifyQueueListener()


def setup_health_check(app: Flask) -> None:
    health_check = HealthCheck(success_ttl=None, failed_ttl=None)
    
    git_service = GitService()
    try:
        current_commit_hash = git_service.get_current_commit_hash()
    except GetCurrentCommitHashException as e:
        logger.error(str(e))
        raise e

    add_application_section_to_health_check(current_commit_hash, health_check)

     # add a check for the process mq connection
    def checkprocessmqconnection():
        proc = ProcessNotifyQueueListener()
        connection = proc._create_mq_connection()
        if connection is None:
            return False, "process mq connection failed"
        connection.disconnect()
        return True, "process mq connection ok"
    
         # add a check for the process mq connection
    def checktransfermqconnection():
        tran = TransferNotifyQueueListener()
        connection = tran._create_mq_connection()
        if connection is None:
            return False, "transfer mq connection failed"
        connection.disconnect()
        return True, "transfer mq connection ok"
    
    health_check.add_check(checkprocessmqconnection)
    
    app.add_url_rule("/healthcheck", "healthcheck", view_func=lambda: health_check.run())
    if instance != "production":
        envdump = EnvironmentDump()
        app.add_url_rule("/environment", "environment", view_func=envdump.run)


def add_application_section_to_health_check(current_commit_hash: str, health_check: HealthCheck) -> None:
    health_check.add_section(
        "application",
        {
            "maintainer": APPLICATION_MAINTAINER,
            "git_repository": APPLICATION_GIT_REPOSITORY,
            "code_version": {
                "commit_hash": current_commit_hash,
            }
        }
    )


def disable_cached_responses(app: Flask) -> None:
    @app.after_request
    def add_response_headers(response: Response) -> Response:
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        response.headers['Cache-Control'] = 'public, max-age=0'
        return response
