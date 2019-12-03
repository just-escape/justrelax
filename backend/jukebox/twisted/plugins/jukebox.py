from justrelax.node.plugin import AbstractNodeServiceMaker
from justrelax.node.jukebox import Jukebox


class ServiceMaker(AbstractNodeServiceMaker):
    service = Jukebox


service_maker = ServiceMaker()
