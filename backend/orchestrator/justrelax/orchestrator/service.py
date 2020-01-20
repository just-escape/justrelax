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
            rooms = requests.get('{}/room/'.format(self.storage_url), params={'scenario': s['id']}).json()
            for r in rooms:
                scenario_rules = requests.get('{}/get_scenario/'.format(self.storage_url)).json()
                self.new_processor(
                    r['id'],
                    r['channel'],
                    scenario_rules['rules'],
                    scenario_rules['variables'],
                )

    def new_processor(self, room_id, channel, rules, variables):
        processor = RulesProcessor(
            factory=self.factory,
            room_id=room_id,
            channel=channel,
            rules=rules,
            variables=variables,
        )
        self.processors[room_id] = processor
