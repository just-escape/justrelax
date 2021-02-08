import yaml
import logging
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
        try:
            self.notify_error()
        except Exception:
            pass

    @staticmethod
    def exception(message=""):
        Logger.logger.exception(message)
        self.notify_error()

    @staticmethod
    def notify_error(message):
        try:
            self.notify_error()
        except Exception:
            pass


logger = Logger


def init_logging(config_path):
    if config_path is not None:
        with open(config_path, "rt") as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(
            format="[%(asctime)s][%(levelname)s] %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S%z",
            level=logging.DEBUG,
        )

    observer = log.PythonLoggingObserver()
    observer.start()


@implementer(ILogObserver)
class DisableTwistdLogs:
    def __call__(self, event):
        pass
