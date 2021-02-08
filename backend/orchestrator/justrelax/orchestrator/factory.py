import json

from autobahn.twisted.websocket import WebSocketServerFactory

from justrelax.common.logging_utils import logger
from justrelax.orchestrator.protocol import PublishSubscribeServerProtocol


class PublishSubscribeServerFactory(WebSocketServerFactory):
    def __init__(self, service, *args, **kwargs):
        super(PublishSubscribeServerFactory, self).__init__(*args, **kwargs)
        self.service = service
        self.protocol = PublishSubscribeServerProtocol
        self.nodes = set()
        logger.notify_error = self.publish_error

    def register(self, protocol):
        self.nodes.add(protocol)

    def unregister(self, protocol):
        self.nodes.remove(protocol)

    def publish(self, event, channel):
        logger.debug("{} <<< {}".format(channel, event))
        message = {'channel': channel, 'event': event}
        for node in self.nodes:
            if node.is_subscribed_to(channel):
                node.send_message(message)

    def publish_error(self, message):
        self.publish({'event': {'from': 'orchestrator', 'log': message}}, 'error')
