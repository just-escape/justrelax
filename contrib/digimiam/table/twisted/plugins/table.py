from justrelax.node.plugin import AbstractNodeServiceMaker
from justrelax.node.table import Table


class ServiceMaker(AbstractNodeServiceMaker):
    service = Table


service_maker = ServiceMaker()
