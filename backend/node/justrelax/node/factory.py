from twisted.internet.protocol import ReconnectingClientFactory

from autobahn.twisted.websocket import WebSocketClientFactory

from justrelax.common.logging_utils import logger
from justrelax.node.protocol import JustSockClientProtocol


class JustSockClientFactory(WebSocketClientFactory, ReconnectingClientFactory):
    maxDelay = 30

    def __init__(self, service, name, channel, *args, **kwargs):
        super(JustSockClientFactory, self).__init__(*args, **kwargs)
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
        self.protocol = JustSockClientProtocol(
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

    def send_event(self, event):
        try:
            self.protocol.send_event(event)
        except Exception as e:
            formatted_exception = "{}: {}".format(type(e).__name__, e)
            self.protocol.send_log_error("Error while trying to send event={}: {}".format(
                event, formatted_exception))
            logger.error("Error while trying to send message={}".format(event))
            logger.exception()

    def process_event(self, event):
        try:
            self.service.process_event(event)
        except Exception as e:
            formatted_exception = "{}: {}".format(type(e).__name__, e)
            self.protocol.send_log_error("Error while trying to process event={}: {}".format(
                event, formatted_exception))
            logger.error("Error while trying to process event={}".format(event))
            logger.exception()
