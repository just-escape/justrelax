from justrelax.node.plugin import AbstractNodeServiceMaker
from justrelax.node.scenario import Scenario


class ServiceMaker(AbstractNodeServiceMaker):
    service = Scenario


service_maker = ServiceMaker()
