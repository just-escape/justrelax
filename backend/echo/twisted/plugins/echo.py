from justrelax.node.plugin import AbstractNodeServiceMaker
from justrelax.node.echo import Echo


class ServiceMaker(AbstractNodeServiceMaker):
    service = Echo


service_maker = ServiceMaker()
