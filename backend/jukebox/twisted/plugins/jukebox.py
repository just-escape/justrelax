from justrelax.node.plugin import AbstractNodeServiceMaker
from justrelax.node.jukebox import Jukebox


class ServiceMaker(AbstractNodeServiceMaker):
    tapname = "jukebox"
    service = Jukebox


service_maker = ServiceMaker()
