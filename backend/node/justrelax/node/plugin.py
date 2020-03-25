import os
import yaml

from zope.interface import implementer

from twisted.python import usage
from twisted.plugin import IPlugin
from twisted.application.service import IServiceMaker

from justrelax.common.logging_utils import init_logging


class Options(usage.Options):
    optParameters = [
        [
            "config", "c", None,
            "YAML configuration file",
        ],
    ]


def get_config_dict(options, etc_filename):
    if options['config']:
        with open(options["config"], "rt") as f:
            config = yaml.safe_load(f.read())
        return config

    try:
        with open(os.path.join('/etc/justrelax', etc_filename), 'rt') as f:
            config = yaml.safe_load(f.read())
    except Exception:
        return {}
    else:
        return config


@implementer(IServiceMaker, IPlugin)
class AbstractNodeServiceMaker(object):
    options = Options

    service = None

    @property
    def tapname(self):
        try:
            return self.service.__name__.lower()
        except Exception:
            return "abstract_node"

    @property
    def description(self):
        return "A {} node.".format(self.tapname)

    def get_default_node_name(self):
        try:
            return self.service.__name__.lower()
        except Exception:
            return "node"

    def get_config(self, options):
        # default
        config = {
            "host": "localhost",
            "port": 3031,
            "name": self.get_default_node_name(),
            "channel": "digimiam1",
            "environment": "rpi",
            "node_params": {},
            "logging": None,
        }

        etc_filename = self.service.__name__.lower()
        parsed_config = get_config_dict(options, etc_filename)

        config.update(parsed_config)
        return config

    def makeService(self, options):
        if self.service is None:
            # The implementer decorator is a lie. The goal is to keep
            # plugins lightweight.
            raise NotImplementedError(
                "This is an abstract plugin. Subclass it and overload "
                "the service attribute.")

        config = self.get_config(options)
        logging_config = config.pop("logging")
        init_logging(logging_config)

        return self.service(**config)
