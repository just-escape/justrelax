from justrelax.node.plugin import AbstractNodeServiceMaker
from justrelax.node.front_door_magnet import FrontDoorMagnet


class ServiceMaker(AbstractNodeServiceMaker):
    service = FrontDoorMagnet


service_maker = ServiceMaker()
