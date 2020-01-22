import requests

from twisted.application import internet

from justrelax.orchestrator.factory import JustSockServerFactory
from justrelax.orchestrator.processor import RulesProcessor


class JustSockServerService(internet.TCPServer):
    def __init__(self, port, storage_url, *args, **kwargs):
        self.storage_url = storage_url

        self.factory = JustSockServerFactory(self)
        self.processors = {}

        self.init_processors()

        super(JustSockServerService, self).__init__(port, self.factory, *args, **kwargs)

    def init_processors(self):
        scenarios = requests.get('{}/scenario/'.format(self.storage_url)).json()
        for s in scenarios:
            rooms = requests.get(
                '{}/room/'.format(self.storage_url),
                params={'room_id': s['id']},
            ).json()
            for r in rooms:
                self.new_processor(
                    r['id'],
                    r['channel'],
                )

    def new_processor(self, room_id, channel):
        processor = RulesProcessor(
            factory=self.factory,
            storage_url=self.storage_url,
            room_id=room_id,
            channel=channel,
        )
        self.processors[room_id] = processor
