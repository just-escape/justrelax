import yaml
import logging.config

from zope.interface import implementer
from twisted.logger import ILogObserver
from twisted.python import log


class Logger:
    logger = logging.getLogger()

    @staticmethod
    def debug(message):
        Logger.logger.debug(message)

    @staticmethod
    def info(message):
        Logger.logger.info(message)

    @staticmethod
    def warning(message):
        Logger.logger.warning(message)

    @staticmethod
    def error(message):
        Logger.logger.error(message)

    @staticmethod
    def exception(message=""):
        Logger.logger.exception(message)


logger = Logger


def init_logging(config_path):
    try:
        with open(config_path, "rt") as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    except Exception:
        logging.basicConfig(level=logging.INFO)
        logger.exception(
            "Could not load logging configuration in {}: using default "
            "configuration"
        )
    observer = log.PythonLoggingObserver()
    observer.start()


@implementer(ILogObserver)
class DisableTwistdLogs:
    def __call__(self, event):
        pass
