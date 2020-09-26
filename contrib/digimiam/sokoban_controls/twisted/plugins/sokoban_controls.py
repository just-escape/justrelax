from justrelax.node.plugin import AbstractNodeServiceMaker
from justrelax.node.sokoban_controls import SokobanControls


class ServiceMaker(AbstractNodeServiceMaker):
    service = SokobanControls


service_maker = ServiceMaker()
