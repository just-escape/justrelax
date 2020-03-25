from justrelax.node.plugin import AbstractNodeServiceMaker
from justrelax.node.chopsticks import Chopsticks


class ServiceMaker(AbstractNodeServiceMaker):
    service = Chopsticks


service_maker = ServiceMaker()
