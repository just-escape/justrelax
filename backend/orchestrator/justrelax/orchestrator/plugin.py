import os
import yaml

from zope.interface import implementer

from twisted.python import usage
from twisted.plugin import IPlugin
from twisted.application import service

from justrelax.common.logging import init_logging
from justrelax.common.utils import abs_path_if_not_abs
from justrelax.orchestrator import conf
from justrelax.orchestrator.manager.room import RoomManager
from justrelax.orchestrator.storage.session import DataBaseAccess
from justrelax.orchestrator.services import Services
from justrelax.orchestrator.ws.service import JustSockServerService
from justrelax.orchestrator.http.service import JustRestService
from justrelax.orchestrator.processor.service import JustProcessService


class Options(usage.Options):
    optParameters = [
        [
            "config", "c", None,
            "YAML configuration file (orchestrator.yaml)",
        ],
    ]


def get_config(options):
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


def init_storage_engine(storage_config):
    if "protocol" not in storage_config:
        return

    kwargs = {
        "protocol": storage_config["protocol"]
    }

    for key in ["user", "password", "host", "port", "base"]:
        if key in storage_config:
            kwargs[key] = storage_config[key]

    DataBaseAccess.init_engine(**kwargs)


@implementer(service.IServiceMaker, IPlugin)
class OrchestratorServiceMaker(object):
    tapname = "orchestrator"
    description = "Launch an orchestrator."
    options = Options

    def makeService(self, options):
        config = get_config(options)

        config["websocket_port"] = options.get("websocket-port", 3031)
        config["http_port"] = options.get("http-port", 3032)
        config["media_directory"] = options.get("media-directory", "/tmp")

        if "logging" in config and config["logging"]:
            init_logging(config["logging"])

        if "storage" in config:
            init_storage_engine(config["storage"])
            rm = RoomManager()
            rooms = rm.get_all()
        else:
            rooms = []

        if "media_directory" in config:
            conf.MEDIA_DIRECTORY = config["media_directory"]

        just_sock = JustSockServerService(config["websocket_port"])
        just_sock.setServiceParent(Services.parent_service)
        Services.just_sock = just_sock

        just_rest = JustRestService(config["http_port"])
        just_rest.setServiceParent(Services.parent_service)
        Services.just_rest = just_rest

        just_process = JustProcessService(rooms)
        just_process.setServiceParent(Services.parent_service)
        Services.just_process = just_process

        return Services.parent_service
