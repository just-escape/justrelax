from justrelax.node.plugin import AbstractNodeServiceMaker
from justrelax.node.niryo import Niryo


class ServiceMaker(AbstractNodeServiceMaker):
    service = Niryo


service_maker = ServiceMaker()
