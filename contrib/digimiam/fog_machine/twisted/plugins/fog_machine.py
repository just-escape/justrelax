from justrelax.node.plugin import AbstractNodeServiceMaker
from justrelax.node.fog_machine import FogMachine


class ServiceMaker(AbstractNodeServiceMaker):
    service = FogMachine


service_maker = ServiceMaker()
