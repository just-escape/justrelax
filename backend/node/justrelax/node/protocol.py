import json

from autobahn.twisted.websocket import WebSocketClientProtocol

from justrelax.common.constants import JUST_SOCK_PROTOCOL as P
from justrelax.common.logging import logger


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

    def log_event(self, event, to_server=True):
        identifier = "{}@{}".format(self.name, self.channel)

        if to_server:
            from_ = identifier
            to = P.SERVER
        else:
            from_ = P.SERVER
            to = identifier

        type_ = event[P.EVENT_TYPE]

        content = event.get(P.EVENT_CONTENT, "")

        logger.info("[{} > {}] {} {}".format(from_, to, type_, content))

    def onMessage(self, payload, isBinary):
        if isBinary:
            logger.warning("Binary message received ({} bytes): ignoring".format(len(payload)))
            return

        try:
            unicode_event = payload.decode('utf8')
        except UnicodeDecodeError:
            logger.exception("Cannot decode {}: ignoring".format(payload))
            return

        try:
            event_dict = json.loads(unicode_event)
        except json.JSONDecodeError:
            logger.exception("Cannot load {}: ignoring".format(unicode_event))
            return

        ok, warning = self.validate_event(event_dict)
        if not ok:
            logger.info("Received {}".format(event_dict))
            logger.warning(warning)
            logger.info("Ignoring")
        else:
            logger.debug("Received {}".format(event_dict))
            self.log_event(event_dict, to_server=False)
            self.factory.process_message(event_dict[P.EVENT_CONTENT])

    @staticmethod
    def validate_event(event):
        try:
            event[P.EVENT_TYPE]
        except KeyError:
            return False, "Event has no type"

        try:
            event[P.EVENT_CONTENT]
        except KeyError:
            return False, "Event has no content"

        if event[P.EVENT_TYPE] != P.EVENT_TYPE_MESSAGE:
            return False, "Only message events are handled"

        return True, None

    def onClose(self, wasClean, code, reason):
        logger.info("WebSocket connection closed: {}".format(reason))

    def send_i_am_node(self):
        event = {
            P.EVENT_TYPE: P.EVENT_TYPE_I_AM,
            P.EVENT_CONTENT: {
                P.I_AM_CLIENT_TYPE: P.CLIENT_NODE,
                P.I_AM_NAME: self.name,
                P.I_AM_CHANNEL: self.channel,
            },
        }
        logger.debug("Declaring as a node")
        self.send_json(event)

    def send_message(self, message):
        event = {
            P.EVENT_TYPE: P.EVENT_TYPE_MESSAGE,
            P.EVENT_CONTENT: message,
        }
        logger.debug("Messaging the server: {}".format(message))
        self.send_json(event)

    def send_json(self, dict_):
        unicode_json = json.dumps(dict_, ensure_ascii=False)
        bytes_ = unicode_json.encode("utf8")

        logger.debug("Sending {}".format(dict_))
        self.log_event(dict_, to_server=True)

        self.sendMessage(bytes_)

    def __str__(self):
        return "{}@{}".format(self.name, self.channel)
