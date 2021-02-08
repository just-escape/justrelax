from twisted.internet.protocol import ReconnectingClientFactory

from autobahn.twisted.websocket import WebSocketClientFactory

from justrelax.common.logging_utils import logger
from justrelax.node.protocol import PublishSubscribeClientProtocol


class PublishSubscribeClientFactory(WebSocketClientFactory, ReconnectingClientFactory):
    maxDelay = 30

    def __init__(self, service, subscriptions, *args, **kwargs):
        super(PublishSubscribeClientFactory, self).__init__(*args, **kwargs)
        self.service = service
        self.subscriptions = subscriptions
        self.protocol = None
        logger.notify_error = self.publish_error

    def startedConnecting(self, connector):
        logger.debug('Started to connect')

    def buildProtocol(self, addr):
        logger.debug('Connected')

        self.resetDelay()

        self.protocol = PublishSubscribeClientProtocol()
        self.protocol.factory = self
        return self.protocol

    def clientConnectionLost(self, connector, reason):
        logger.error('Connection lost. Reason: {}'.format(reason))
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        logger.error('Connection failed. Reason: {}'.format(reason))
        ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)

    def publish(self, event, channel):
        logger.debug("{} <<< {}".format(channel, event))
        self.protocol.send_message({'action': 'publish', 'channel': channel, 'event': event})

    def publish_error(self, message):
        from_ = "{}@{}".format(self.service.name, self.subscriptions)

        self.protocol.send_message(
            {
                'action': 'publish',
                'channel': 'error',
                'event': {
                    'from': from_,
                    'log': message,
                }
            }
        )

    def process_event(self, event, channel):
        logger.debug("{} >>> {}".format(channel, event))

        try:
            self.service.process_event(event, channel)
        except Exception as e:
            formatted_exception = "{}: {}".format(type(e).__name__, e)
            logger.error("Error while trying to process message={} ({})".format(message, formatted_exception))
