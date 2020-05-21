from justrelax.node.plugin import AbstractNodeServiceMaker
from justrelax.node.load_cells import LoadCells


class ServiceMaker(AbstractNodeServiceMaker):
    service = LoadCells


service_maker = ServiceMaker()
