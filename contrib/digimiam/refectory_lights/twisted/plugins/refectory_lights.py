from justrelax.node.plugin import AbstractNodeServiceMaker
from justrelax.node.refectory_lights import RefectoryLights


class ServiceMaker(AbstractNodeServiceMaker):
    service = RefectoryLights


service_maker = ServiceMaker()
