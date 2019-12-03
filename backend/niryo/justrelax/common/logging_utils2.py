import sys
import yaml
import logging

from zope.interface import implementer
from twisted.logger import ILogObserver
from twisted.python import log


logger = logging


def init_logging(config_path):
    if config_path is not None:
        with open(config_path, "rt") as f:
            config = yaml.safe_load(f.read())
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(
            stream=sys.stdout,
            format="[%(asctime)s][%(levelname)s] %(message)s",
            datefmt="%Y-%m-%dT%H:%M:%S%z",
            level=logging.INFO,
        )

    observer = log.PythonLoggingObserver()
    observer.start()


@implementer(ILogObserver)
class DisableTwistdLogs:
    def __call__(self, event):
        pass
