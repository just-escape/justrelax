from justrelax.node.plugin import AbstractNodeServiceMaker
from justrelax.node.echo import Echo


class ServiceMaker(AbstractNodeServiceMaker):
    tapname = "echo"
    service = Echo


service_maker = ServiceMaker()
