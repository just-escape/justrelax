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


def check_config_path(path):
    if path is None:
        raise ValueError("--config (-c) argument is mandatory")
    return path


class Options(usage.Options):
    optParameters = [
        [
            "config", "c", None,
            "YAML configuration file (orchestrator.yaml)",
            check_config_path
        ],
        ["websocket-port", "w", None, "Port number to listen on"],
        ["http-port", "t", None, "Port number to listen on"],
        ["media-directory", "m", None, "Root directory serving media files"],
    ]


def absolutify(config, config_path):
    config_dir = os.path.dirname(config_path)

    if "media_directory" in config:
        config["media_directory"] = abs_path_if_not_abs(
            config["media_directory"], config_dir)
    config["logging"] = abs_path_if_not_abs(config["logging"], config_dir)


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
        with open(options["config"], "rt") as f:
            config = yaml.safe_load(f.read())

        if options["websocket-port"] is not None:
            config["websocket_port"] = options["websocket-port"]

        if options["http-port"] is not None:
            config["http_port"] = options["http-port"]

        if options["media-directory"] is not None:
            config["media_directory"] = options["media-directory"]

        absolutify(config, options["config"])

        init_logging(config["logging"])

        if "storage" in config:
            init_storage_engine(config["storage"])

        if "media_directory" in config:
            conf.MEDIA_DIRECTORY = config["media_directory"]

        rm = RoomManager()
        rooms = rm.get_all()

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
