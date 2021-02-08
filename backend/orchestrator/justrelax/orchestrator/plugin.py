import yaml

from zope.interface import implementer

from twisted.python import usage
from twisted.plugin import IPlugin
from twisted.application import service

from justrelax.common.logging_utils import init_logging
from justrelax.orchestrator.service import PublishSubscribeServerService


class Options(usage.Options):
    optParameters = [
        [
            "config", "c", None,
            "YAML configuration file (orchestrator.yaml)",
        ],
    ]


def get_config_dict(options):
    if options['config']:
        with open(options["config"], "rt") as f:
            config = yaml.safe_load(f.read())
        return config
    
    try:
        with open('/etc/justrelax/orchestrator.yaml', 'rt') as f:
            config = yaml.safe_load(f.read())
    except FileNotFoundError:
        return {}
    else:
        return config


@implementer(service.IServiceMaker, IPlugin)
class PublishSubscribeServerServiceMaker(object):
    tapname = "orchestrator"
    description = "Launch an orchestrator."
    options = Options

    def makeService(self, options):
        config = get_config_dict(options)

        websocket_port = config.get("websocket_port", 3031)

        init_logging(config.get("logging", None))

        s = PublishSubscribeServerService(websocket_port)
        return s
