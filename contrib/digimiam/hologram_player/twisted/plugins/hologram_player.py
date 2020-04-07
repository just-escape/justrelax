from justrelax.node.plugin import AbstractNodeServiceMaker
from justrelax.node.hologram_player import HologramPlayer


class ServiceMaker(AbstractNodeServiceMaker):
    service = HologramPlayer


service_maker = ServiceMaker()
