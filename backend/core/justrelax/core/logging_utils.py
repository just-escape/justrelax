import logging
import logging.config
import logging.handlers

from twisted.python import log


logger = logging.getLogger()


def init_logging(level='INFO', file='/dev/null', twisted_logs=False, stdout=False):
    l = logger
    l.setLevel(level)

    line_formatter = logging.Formatter("[%(asctime)s][%(levelname)s] %(message)s", datefmt="%Y-%m-%dT%H:%M:%S%z")

    if stdout:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(line_formatter)
        l.addHandler(stream_handler)

    rotating_file_handler = logging.handlers.RotatingFileHandler(file, maxBytes=1485760, backupCount=3)
    rotating_file_handler.setFormatter(line_formatter)
    l.addHandler(rotating_file_handler)

    if twisted_logs:
        observer = log.PythonLoggingObserver()
        observer.start()
