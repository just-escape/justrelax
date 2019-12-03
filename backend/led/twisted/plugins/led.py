from justrelax.node.plugin import AbstractNodeServiceMaker
from justrelax.node.led import Led


class ServiceMaker(AbstractNodeServiceMaker):
    service = Led


service_maker = ServiceMaker()
