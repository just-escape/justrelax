from justrelax.node.plugin import AbstractNodeServiceMaker
from justrelax.node.decoration_belt_rotary import DecorationBeltRotary


class ServiceMaker(AbstractNodeServiceMaker):
    service = DecorationBeltRotary


service_maker = ServiceMaker()
