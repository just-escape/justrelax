from justrelax.node.plugin import AbstractNodeServiceMaker
from justrelax.node.emergency_exit import EmergencyExit


class ServiceMaker(AbstractNodeServiceMaker):
    service = EmergencyExit


service_maker = ServiceMaker()
