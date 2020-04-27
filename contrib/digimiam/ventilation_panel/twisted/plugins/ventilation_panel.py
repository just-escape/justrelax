from justrelax.node.plugin import AbstractNodeServiceMaker
from justrelax.node.ventilation_panel import VentilationPanel


class ServiceMaker(AbstractNodeServiceMaker):
    service = VentilationPanel


service_maker = ServiceMaker()
