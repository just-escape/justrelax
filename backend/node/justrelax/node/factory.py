from twisted.internet.protocol import ReconnectingClientFactory

from autobahn.twisted.websocket import WebSocketClientFactory

from justrelax.common.logging_utils import logger
from justrelax.node.protocol import JustSockNodeClientProtocol


class JustSockNodeClientFactory(WebSocketClientFactory, ReconnectingClientFactory):
    maxDelay = 30

    def __init__(self, service, name, channel, *args, **kwargs):
        super(JustSockNodeClientFactory, self).__init__(*args, **kwargs)
        self.service = service
        self.name = name
        self.channel = channel
        self.protocol = None

    def startedConnecting(self, connector):
        logger.debug('Started to connect')

    def buildProtocol(self, addr):
        logger.debug('Connected')

        self.resetDelay()

        logger.debug("Building protocol")
        self.protocol = JustSockNodeClientProtocol(
            self,
            self.name,
            self.channel
        )

        return self.protocol

    def clientConnectionLost(self, connector, reason):
        logger.error('Connection lost. Reason: {}'.format(reason))
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        logger.error('Connection failed. Reason: {}'.format(reason))
        ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)

    def send_message(self, message):
        try:
            self.protocol.send_message(message)
        except Exception:
            logger.error("Error while trying to send message={}".format(message))
            logger.exception()

    def process_message(self, message):
        try:
            self.service.process_message(message)
        except Exception:
            logger.error("Error while trying to process message={}".format(message))
            logger.exception()
