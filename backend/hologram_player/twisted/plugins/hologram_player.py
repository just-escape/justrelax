from justrelax.node.plugin import AbstractNodeServiceMaker
from justrelax.node.hologram_player import HologramPlayer


class ServiceMaker(AbstractNodeServiceMaker):
    tapname = "hologram_player"
    service = HologramPlayer


service_maker = ServiceMaker()
