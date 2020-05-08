from justrelax.node.plugin import AbstractNodeServiceMaker
from justrelax.node.holographic_menu import HolographicMenu


class ServiceMaker(AbstractNodeServiceMaker):
    service = HolographicMenu


service_maker = ServiceMaker()
