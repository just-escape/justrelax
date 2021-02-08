import json

from autobahn.twisted.websocket import WebSocketServerProtocol

from justrelax.common.logging_utils import logger


class PublishSubscribeServerProtocol(WebSocketServerProtocol):
    def __init__(self):
        super(PublishSubscribeServerProtocol, self).__init__()
        self.channels = set()

    def onConnect(self, request):
        logger.info("Client connecting: {}".format(request.peer))

    def onOpen(self):
        logger.info("Client connected: {}".format(self.peer))
        self.factory.register(self)

    def connectionLost(self, reason):
        self.factory.unregister(self)

        logger.info("Lost connection with {}".format(self))

    def onMessage(self, payload, isBinary):
        if isBinary:
            logger.warning("Binary message received ({} bytes): ignoring".format(len(payload)))
            return

        unicode_message = payload.decode('utf8', 'replace')

        try:
            message = json.loads(unicode_message)
        except json.JSONDecodeError:
            logger.exception("Cannot load {}: ignoring".format(unicode_message))
            return

        # message could be validated here with something like pydantic

        logger.debug("{} >>> {}".format(self, message))

        try:
            if message["action"] == "publish":
                self.factory.publish(message["event"], message["channel"])

            elif message["action"] == "subscribe":
                self.subscribe(message["channel"])

        except Exception as e:
            formatted_exception = "{}: {}".format(type(e).__name__, e)
            logger.error("Error while trying to process message={} ({})".format(message, formatted_exception))

    def subscribe(self, channel):
        self.channels.add(channel)

    def is_subscribed_to(self, channel):
        return channel in self.channels

    def send_message(self, message):
        unicode_json = json.dumps(message, ensure_ascii=False)
        bytes_ = unicode_json.encode("utf8", "replace")
        self.sendMessage(bytes_)

    def __str__(self):
        return self.peer
