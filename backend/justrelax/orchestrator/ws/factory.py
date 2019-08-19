from autobahn.twisted.websocket import WebSocketServerFactory

from justrelax.orchestrator.ws.protocol import JustSockServerProtocol
from justrelax.common.logging import logger


class JustSockServerFactory(WebSocketServerFactory):
    def __init__(self, service, *args, **kwargs):
        super(JustSockServerFactory, self).__init__(*args, **kwargs)
        self.service = service
        self.protocol = JustSockServerProtocol
        self.nodes = {}
        self.admins = set()

    def register_admin(self, admin):
        self.admins.add(admin)

    def unregister_admin(self, admin):
        self.admins.remove(admin)

    def register_node(self, node):
        if (node.name, node.channel,) not in self.nodes:
            self.nodes[(node.name, node.channel,)] = set()
        self.nodes[(node.name, node.channel,)].add(node)

    def unregister_node(self, node):
        self.nodes[(node.name, node.channel,)].remove(node)
        if not self.nodes[(node.name, node.channel,)]:
            self.nodes.pop((node.name, node.channel,), None)

    def process_message(self, name, channel, message):
        self.service.process_message(name, channel, message)

    def send_beat(self, channel, ticks):
        for admin in self.admins:
            admin.send_beat(channel, ticks)

    def send_record(self, channel, record):
        for admin in self.admins:
            admin.send_record(channel, record)

    def send_reset(self, channel):
        for admin in self.admins:
            admin.send_reset(channel)

    def send_to_node(self, name, channel, message):
        nodes = self.nodes.get((name, channel,), [])
        if nodes:
            for node in nodes:
                node.send_message(message)
        else:
            logger.warning(
                "Node {}@{} is not registered: skipping message".format(
                    name, channel
                )
            )
