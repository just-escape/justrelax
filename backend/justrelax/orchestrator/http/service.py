from twisted.application import internet
from twisted.web.server import Site

from justrelax.orchestrator.http.api import App
from justrelax.constants import ORCHESTRATOR


class JustRestService(internet.TCPServer):
    def __init__(self, port, *args, **kwargs):
        app = App()
        App.service = self  # Dangerous but it works and is convenient
        factory = Site(app.get_resource())

        self._just_process = None

        super(JustRestService, self).__init__(port, factory, *args, **kwargs)

    @property
    def just_process(self):
        if not self._just_process:
            self._just_process = self.parent.getServiceNamed(
                ORCHESTRATOR.SERVICE_JUST_PROCESS)
        return self._just_process

    def get_processor_configs(self):
        return self.just_process.get_processor_configs()

    def process_action(self, channel, action):
        self.just_process.process_action(channel, action)

    def run_room(self, channel):
        self.just_process.run_room(channel)

    def halt_room(self, channel):
        self.just_process.halt_room(channel)

    def reset_room(self, channel):
        self.just_process.reset_room(channel)
