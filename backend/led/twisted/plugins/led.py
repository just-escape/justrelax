from justrelax.node.plugin import AbstractNodeServiceMaker
from justrelax.node.led import Led


class ServiceMaker(AbstractNodeServiceMaker):
    tapname = "led"
    service = Led


service_maker = ServiceMaker()
