from twisted.application.service import Service

from justrelax.constants import ORCHESTRATOR
from justrelax.orchestrator.processor.engine import RulesProcessor


class JustProcessService(Service):
    def __init__(self, rooms):
        self.processors = []
        for room in rooms:
            storage_config = room["storage"]
            storage_class = storage_config.pop("class")
            storage = storage_class(**storage_config)

            self.processor = RulesProcessor(
                service=self,
                scenario=room["scenario"],
                room=room["room"],
                channel=room["channel"],
                rules=room["rules"],
                storage=storage,
                cams=room["cams"],
            )
            self.processors.append(self.processor)

        self._just_sock = None

        super(JustProcessService, self).__init__()

    @property
    def just_sock(self):
        if not self._just_sock:
            self._just_sock = self.parent.getServiceNamed(
                ORCHESTRATOR.SERVICE_JUST_SOCK)
        return self._just_sock

    def get_processor_configs(self):
        configs = []
        for processor in self.processors:
            configs.append(processor.get_config())
        return configs

    def process_message(self, name, channel, message):
        for processor in self.processors:
            if processor.is_subscribed_to_channel(channel):
                processor.process_message(name, message)

    def process_action(self, channel, action):
        for processor in self.processors:
            if processor.is_subscribed_to_channel(channel):
                processor.process_action_from_name(action)

    def run_room(self, channel):
        for processor in self.processors:
            if processor.is_subscribed_to_channel(channel):
                processor.run_room()

    def halt_room(self, channel):
        for processor in self.processors:
            if processor.is_subscribed_to_channel(channel):
                processor.halt_room()

    def reset_room(self, channel):
        for processor in self.processors:
            if processor.is_subscribed_to_channel(channel):
                processor.reset_room()

    def send_to_node(self, name, channel, message):
        self.just_sock.send_to_node(name, channel, message)

    def send_beat(self, channel, ticks):
        self.just_sock.send_beat(channel, ticks)

    def send_record(self, channel, record):
        self.just_sock.send_record(channel, record)

    def send_reset(self, channel):
        self.just_sock.send_reset(channel)
