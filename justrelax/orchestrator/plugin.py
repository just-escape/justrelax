import os
import yaml

from zope.interface import implementer

from twisted.python import usage
from twisted.plugin import IPlugin
from twisted.application import service

from justrelax.common.logging import init_logging
from justrelax.common.utils import abs_path_if_not_abs, import_string
from justrelax.orchestrator.ws.service import JustSockServerService
from justrelax.orchestrator.http.service import JustRestService
from justrelax.constants import ORCHESTRATOR
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
    ]


def absolutify(config, config_path):
    config_dir = os.path.dirname(config_path)

    config["logging"] = abs_path_if_not_abs(config["logging"], config_dir)

    for room in config["rooms"]:
        room["rules"] = abs_path_if_not_abs(room["rules"], config_dir)

        if "db_file" in room["storage"]:
            db_file = room["storage"]["db_file"]
            room["storage"]["db_file"] = abs_path_if_not_abs(db_file, config_dir)


def classify(config):
    for room in config["rooms"]:
        room["storage"]["class"] = import_string(room["storage"]["class"])


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

        absolutify(config, options["config"])
        classify(config)

        init_logging(config["logging"])

        parent_service = service.MultiService()

        just_sock = JustSockServerService(port=config["websocket_port"])
        just_sock.setName(ORCHESTRATOR.SERVICE_JUST_SOCK)
        just_sock.setServiceParent(parent_service)

        just_rest = JustRestService(config["http_port"])
        just_rest.setName(ORCHESTRATOR.SERVICE_JUST_REST)
        just_rest.setServiceParent(parent_service)

        just_process = JustProcessService(config["rooms"])
        just_process.setName(ORCHESTRATOR.SERVICE_JUST_PROCESS)
        just_process.setServiceParent(parent_service)

        return parent_service
