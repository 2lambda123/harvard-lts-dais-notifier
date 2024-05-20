import logging
import os, os.path
from logging.handlers import TimedRotatingFileHandler

from flask import Flask, Response
import werkzeug
import time
from pathlib import Path

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
    
    app = Flask(__name__)

    @app.route('/readiness', endpoint="readiness")
    @app.errorhandler(werkzeug.exceptions.BadRequest)
    def readiness():
        ready_path = os.getenv("READINESS_FILE", "/tmp/worker_ready")
        readiness_file = Path(ready_path)

        if not readiness_file.is_file():
            return "DAIS Notifier worker NOT ready", 503
        return "DAIS Notifier worker ready", 200
    
    @app.route('/liveness', endpoint="liveness")
    @app.errorhandler(werkzeug.exceptions.BadRequest)
    def liveness():
        # check timestamp file
        try:
            current_ts = int(time.time())
            hbeat_path = os.getenv("HEARTBEAT_FILE", "/tmp/worker_heartbeat")
            heartbeat_file = Path(hbeat_path)
            heartbeat_window = int(os.getenv("HEARTBEAT_WINDOW", 60))
            fstats = os.stat(heartbeat_file)
            mtime = int(fstats.st_mtime)
            seconds_diff = int(current_ts - mtime)

            if (seconds_diff < heartbeat_window):
                print("healthy: last updated %d secs ago" % (seconds_diff))
                return "DAIS Notifier healthy", 200
            else:
                print("UNHEALTHY: last updated %d secs ago" % (seconds_diff))
                return "UNHEALTHY: DAIS Notifier liveness last updated \
                 %d secs ago" % (seconds_diff), 500

        except Exception:
            print("Error: file not found")
            return "Error: DAIS Notifier liveness file not found", 500

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

def disable_cached_responses(app: Flask) -> None:
    @app.after_request
    def add_response_headers(response: Response) -> Response:
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        response.headers['Cache-Control'] = 'public, max-age=0'
        return response
