from twisted.application import internet

from justrelax.orchestrator.ws.factory import JustSockServerFactory
from justrelax.constants import ORCHESTRATOR


class JustSockServerService(internet.TCPServer):
    def __init__(self, port, *args, **kwargs):
        self.factory = JustSockServerFactory(self)

        self._just_process = None

        super(JustSockServerService, self).__init__(port, self.factory, *args, **kwargs)

    @property
    def just_process(self):
        if not self._just_process:
            self._just_process = self.parent.getServiceNamed(
                ORCHESTRATOR.SERVICE_JUST_PROCESS)
        return self._just_process

    def process_message(self, name, channel, message):
        self.just_process.process_message(name, channel, message)

    def send_to_node(self, name, channel, message):
        self.factory.send_to_node(name, channel, message)

    def send_beat(self, channel, ticks):
        self.factory.send_beat(channel, ticks)

    def send_record(self, channel, record):
        self.factory.send_record(channel, record)

    def send_reset(self, channel):
        self.factory.send_reset(channel)
