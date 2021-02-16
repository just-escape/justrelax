import json
import argparse

from twisted.internet import reactor
from autobahn.twisted.websocket import WebSocketServerFactory, WebSocketServerProtocol

from justrelax.core.logging_utils import init_logging, logger


class BrokerProtocol(WebSocketServerProtocol):
    def __init__(self):
        super(BrokerProtocol, self).__init__()
        self.channels = set()

    def onConnect(self, request):
        logger.debug("Node connecting: {}".format(request.peer))

    def onOpen(self):
        logger.info("Node connected ({})".format(self.peer))
        self.factory.register(self)

    def connectionLost(self, reason):
        self.factory.unregister(self)

        logger.info("Node disconnected ({})".format(self))

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

        except Exception:
            logger.error("Error while trying to process message={}: skipping".format(message), exc_info=True)

    def subscribe(self, channel):
        self.channels.add(channel)
        logger.info("{} subscribed to {}".format(self.peer, channel))

    def is_subscribed_to(self, channel):
        return channel in self.channels

    def send_message(self, message):
        unicode_json = json.dumps(message, ensure_ascii=False)
        bytes_ = unicode_json.encode("utf8", "replace")
        self.sendMessage(bytes_)

    def __str__(self):
        return self.peer


class BrokerFactory(WebSocketServerFactory):
    def __init__(self, *args, **kwargs):
        super(BrokerFactory, self).__init__(*args, **kwargs)
        self.protocol = BrokerProtocol
        self.nodes = set()

    def register(self, protocol):
        self.nodes.add(protocol)

    def unregister(self, protocol):
        self.nodes.discard(protocol)

    def publish(self, event, channel):
        logger.info("{} <<< {}".format(channel, event))
        message = {'channel': channel, 'event': event}
        for node in self.nodes:
            if node.is_subscribed_to(channel):
                node.send_message(message)


def run_broker():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=3031, help='3031 by default')
    parser.add_argument('-l', '--log-level', type=str, default='INFO', help='INFO by default')
    parser.add_argument('-f', '--log-file', type=str, default='/dev/null', help='/dev/null by default (no file)')
    parser.add_argument('-t', '--twisted-logs', action='store_true', help='Include twisted logs (no by default)')
    args = parser.parse_args()

    init_logging(level=args.log_level, file=args.log_file, twisted_logs=args.twisted_logs)

    logger.info("Starting broker")

    reactor.listenTCP(args.port, BrokerFactory())

    logger.info("Listening on port {}".format(args.port))

    reactor.run()


if __name__ == '__main__':
    run_broker()
