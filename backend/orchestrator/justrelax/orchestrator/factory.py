from autobahn.twisted.websocket import WebSocketServerFactory

from justrelax.common.logging_utils import logger
from justrelax.orchestrator.protocol import JustSockServerProtocol


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
        for _, processor in self.service.processors.items():
            if processor.is_subscribed_to_channel(channel):
                processor.process_message(name, message)

    def process_run_room(self, room_id):
        self.service.processors[room_id].run_room()

    def process_halt_room(self, room_id):
        self.service.processors[room_id].halt_room()

    def process_reset_room(self, room_id):
        self.service.processors[room_id].reset_room()

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
