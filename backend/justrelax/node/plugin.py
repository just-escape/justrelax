import os
import yaml

from zope.interface import implementer

from twisted.python import usage
from twisted.plugin import IPlugin
from twisted.application.service import IServiceMaker

from justrelax.common.logging import init_logging
from justrelax.common.utils import abs_path_if_not_abs, import_string
from justrelax.common.validation import validate_node_name, validate_channel


def check_config_path(path):
    if path is None:
        raise ValueError("--config (-c) argument is mandatory")
    return path


def check_node_name(name):
    if not validate_node_name(name):
        raise ValueError("Name must be an alphanumeric string")
    return name


def check_channel(channel):
    if not validate_channel(channel):
        raise ValueError("Channel must be an alphanumeric string")
    return channel


class Options(usage.Options):
    optParameters = [
        [
            "config", "c", None,
            "YAML configuration file (node.yaml)",
            check_config_path
        ],
        ["host", "h", None, "The hostname to connect to"],
        ["port", "p", None, "The port number to connect to"],
        ["name", "n", None, "Node name", check_node_name],
        ["channel", "l", None, "Channel to push/subscribe on", check_channel],
        ["class", "s", None, "Node implementation class"]
    ]


def absolutify(config, config_path):
    config_dir = os.path.dirname(config_path)
    config["logging"] = abs_path_if_not_abs(config["logging"], config_dir)


def classify(config):
    config["class"] = import_string(config["class"])


@implementer(IServiceMaker, IPlugin)
class NodeServiceMaker(object):
    tapname = "node"
    description = "Launch a node."
    options = Options

    def makeService(self, options):
        with open(options["config"], "rt") as f:
            config = yaml.safe_load(f.read())

        overloadables = ("host", "port", "class", "channel", "name",)
        for key in overloadables:
            if options[key] is not None:
                config[key] = options[key]

        absolutify(config, options["config"])
        classify(config)

        init_logging(config["logging"])

        return config["class"](
            host=config["host"],
            port=config["port"],
            name=config["name"],
            channel=config["channel"],
            media=config["media"],
        )
