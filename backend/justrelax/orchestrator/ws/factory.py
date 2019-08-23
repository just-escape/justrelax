from autobahn.twisted.websocket import WebSocketServerFactory

from justrelax.common.logging import logger
from justrelax.orchestrator.services import Services
from justrelax.orchestrator.ws.protocol import JustSockServerProtocol


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

    @staticmethod
    def process_message(name, channel, message):
        Services.just_process.process_message(name, channel, message)

    def send_beat(self, room_id, ticks):
        for admin in self.admins:
            admin.send_beat(room_id, ticks)

    def send_record(self, room_id, record):
        for admin in self.admins:
            admin.send_record(room_id, record)

    def send_reset(self, room_id):
        for admin in self.admins:
            admin.send_reset(room_id)

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
