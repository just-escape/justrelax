from justrelax.node.plugin import AbstractNodeServiceMaker
from justrelax.node.cylinders import Cylinders


class ServiceMaker(AbstractNodeServiceMaker):
    service = Cylinders


service_maker = ServiceMaker()
