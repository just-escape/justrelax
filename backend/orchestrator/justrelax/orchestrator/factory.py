import json

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
        for room_id, processor in self.service.processors.items():
            records = processor.records
            session_time = processor.session_timer.session_time
            admin.send_live_data(room_id, session_time, records)

    def unregister_admin(self, admin):
        self.admins.remove(admin)

    def register_node(self, node):
        if (node.name, node.channel,) not in self.nodes:
            self.nodes[(node.name, node.channel,)] = set()
        self.nodes[(node.name, node.channel,)].add(node)

        for room_id, processor in self.service.processors.items():
            if processor.is_subscribed_to_channel(node.channel):
                processor.on_node_connection(node.name)

    def unregister_node(self, node):
        self.nodes[(node.name, node.channel,)].remove(node)
        if not self.nodes[(node.name, node.channel,)]:
            self.nodes.pop((node.name, node.channel,), None)

        for room_id, processor in self.service.processors.items():
            if processor.is_subscribed_to_channel(node.channel):
                processor.on_node_disconnection(node.name)

    def process_event(self, name, channel, event):
        for _, processor in self.service.processors.items():
            if processor.is_subscribed_to_channel(channel):
                processor.on_event(name, event)

    def send_log_error(self, channel, node_name, content):
        for admin in self.admins:
            admin.send_log_error(channel, node_name, content)

    def send_log_info(self, channel, node_name, content):
        for admin in self.admins:
            admin.send_log_info(channel, node_name, content)

    def process_run_room(self, room_id):
        self.service.processors[room_id].run_room()

    def process_halt_room(self, room_id):
        self.service.processors[room_id].halt_room()

    def process_reset_room(self, room_id):
        self.service.processors[room_id].reset_room()

    def process_send_event_to(self, room_id, node_name, event):
        channel = self.service.processors[room_id].channel
        event = json.loads(event)
        self.send_to_node(node_name, channel, event)

    def process_send_event_as(self, room_id, node_name, event):
        processor = self.service.processors[room_id]
        event = json.loads(event)
        processor.on_event(node_name, event)

    def process_on_admin_button_pressed(self, room_id, button_id):
        self.service.processors[room_id].on_admin_button_pressed(button_id)

    def send_notification(self, type_, message):
        for admin in self.admins:
            admin.send_notification(type_, message)

    def send_tic_tac(self, room_id, session_time):
        for admin in self.admins:
            admin.send_tic_tac(room_id, session_time)

    def send_record(self, room_id, record_id, session_time, label):
        for admin in self.admins:
            admin.send_record(room_id, record_id, session_time, label)

    def send_reset(self, room_id):
        for admin in self.admins:
            admin.send_reset(room_id)

    def send_to_node(self, name, channel, event):
        nodes = self.nodes.get((name, channel,), [])
        if nodes:
            for node in nodes:
                node.send_event(event)
        else:
            logger.warning(
                "Node {}@{} is not registered: skipping event".format(
                    name, channel
                )
            )
