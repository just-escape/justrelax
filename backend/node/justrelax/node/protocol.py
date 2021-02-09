import json

from twisted.internet.protocol import connectionDone

from autobahn.twisted.websocket import WebSocketClientProtocol

from justrelax.common.logging_utils import logger


class PublishSubscribeClientProtocol(WebSocketClientProtocol):
    def onConnect(self, response):
        logger.info("Connected to broker at {}".format(response.peer))

    def onConnecting(self, transport_details):
        logger.debug("Connecting. Transport details: {}".format(transport_details))

    def onOpen(self):
        logger.debug("WebSocket connection opened")

        for subscription in self.factory.subscriptions:
            logger.info("Subscribing to {}".format(subscription))
            self.send_message(
                {
                    "action": "subscribe",
                    "channel": subscription,
                }
            )

    def onMessage(self, payload, isBinary):
        if isBinary:
            logger.warning("Binary message received ({} bytes): ignoring".format(len(payload)))
            return

        unicode_message = payload.decode('utf8', 'replace')

        try:
            message = json.loads(unicode_message)
        except json.JSONDecodeError:
            logger.warning("Cannot load {}: ignoring".format(unicode_message))
            return

        # message could be validated here with something like pydantic

        self.factory.process_event(message['event'], message['channel'])

    def onClose(self, wasClean, code, reason):
        logger.info("WebSocket connection closed: {}".format(reason))

    def send_message(self, event):
        unicode_json = json.dumps(event, ensure_ascii=False)
        bytes_ = unicode_json.encode("utf8", "replace")
        self.sendMessage(bytes_)
