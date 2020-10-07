from justrelax.node.plugin import AbstractNodeServiceMaker
from justrelax.node.secure_floor import SecureFloor


class ServiceMaker(AbstractNodeServiceMaker):
    service = SecureFloor


service_maker = ServiceMaker()
