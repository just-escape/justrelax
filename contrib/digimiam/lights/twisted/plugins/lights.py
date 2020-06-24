from justrelax.node.plugin import AbstractNodeServiceMaker
from justrelax.node.lights import Lights


class ServiceMaker(AbstractNodeServiceMaker):
    service = Lights


service_maker = ServiceMaker()
