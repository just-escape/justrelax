from justrelax.node.plugin import AbstractNodeServiceMaker
from justrelax.node.control_panel import ControlPanel


class ServiceMaker(AbstractNodeServiceMaker):
    service = ControlPanel


service_maker = ServiceMaker()
