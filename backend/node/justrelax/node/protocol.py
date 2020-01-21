import json

from autobahn.twisted.websocket import WebSocketClientProtocol

from justrelax.common.constants import JUST_SOCK_PROTOCOL as P
from justrelax.common.logging_utils import logger


class JustSockNodeClientProtocol(WebSocketClientProtocol):
    def __init__(self, factory, name, channel):
        super(JustSockNodeClientProtocol, self).__init__()
        self.factory = factory
        self.name = name
        self.channel = channel

    def onConnect(self, response):
        logger.info("Connected to server: {}".format(response.peer))

    def onConnecting(self, transport_details):
        logger.debug("Connecting. Transport details: {}".format(transport_details))

    def onOpen(self):
        logger.debug("WebSocket connection opened")

        self.send_i_am_node()

    def log_message(self, message, to_server=True):
        identifier = "{}@{}".format(self.name, self.channel)

        if to_server:
            from_ = identifier
            to = P.SERVER
        else:
            from_ = P.SERVER
            to = identifier

        type_ = message[P.MESSAGE_TYPE]

        content = message.get(P.EVENT, "")

        logger.info("[{} > {}] {} {}".format(from_, to, type_, content))

    def onMessage(self, payload, isBinary):
        if isBinary:
            logger.warning("Binary message received ({} bytes): ignoring".format(len(payload)))
            return

        try:
            unicode_message = payload.decode('utf8')
        except UnicodeDecodeError:
            logger.exception("Cannot decode {}: ignoring".format(payload))
            return

        try:
            message = json.loads(unicode_message)
        except json.JSONDecodeError:
            logger.exception("Cannot load {}: ignoring".format(unicode_message))
            return

        ok, warning = self.validate_message(message)
        if not ok:
            logger.info("Received {}".format(message))
            logger.warning(warning)
            logger.info("Ignoring")
        else:
            logger.debug("Received {}".format(message))
            self.log_message(message, to_server=False)
            self.factory.process_event(message[P.EVENT])

    @staticmethod
    def validate_message(message):
        try:
            message[P.MESSAGE_TYPE]
        except KeyError:
            return False, "Message has no type"

        if message[P.MESSAGE_TYPE] != P.MESSAGE_TYPE_EVENT:
            return False, "Only event messages are handled"

        try:
            message[P.EVENT]
        except KeyError:
            return False, "Message has no event"

        return True, None

    def onClose(self, wasClean, code, reason):
        logger.info("WebSocket connection closed: {}".format(reason))

    def send_i_am_node(self):
        message = {
            P.MESSAGE_TYPE: P.MESSAGE_TYPE_I_AM,
            P.I_AM_CLIENT_TYPE: P.CLIENT_NODE,
            P.I_AM_NAME: self.name,
            P.I_AM_CHANNEL: self.channel,
        }
        logger.debug("Declaring as a node")
        self.send_json(message)

    def send_event(self, event):
        message = {
            P.MESSAGE_TYPE: P.MESSAGE_TYPE_EVENT,
            P.EVENT: event,
        }
        logger.debug("Sending message to the server: {}".format(message))
        self.send_json(message)

    def send_json(self, dict_):
        unicode_json = json.dumps(dict_, ensure_ascii=False)
        bytes_ = unicode_json.encode("utf8")

        logger.debug("Sending {}".format(dict_))
        self.log_message(dict_, to_server=True)

        self.sendMessage(bytes_)

    def __str__(self):
        return "{}@{}".format(self.name, self.channel)
