from justrelax.node.plugin import AbstractNodeServiceMaker
from justrelax.node.output_device import OutputDevice


class ServiceMaker(AbstractNodeServiceMaker):
    service = OutputDevice


service_maker = ServiceMaker()
