from justrelax.node.plugin import AbstractNodeServiceMaker
from justrelax.node.floppy_reader import FloppyReader


class ServiceMaker(AbstractNodeServiceMaker):
    service = FloppyReader


service_maker = ServiceMaker()
