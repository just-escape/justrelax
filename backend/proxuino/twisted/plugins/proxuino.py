from justrelax.node.plugin import AbstractNodeServiceMaker
from justrelax.node.proxuino import Proxuino


class ServiceMaker(AbstractNodeServiceMaker):
    service = Proxuino


service_maker = ServiceMaker()
