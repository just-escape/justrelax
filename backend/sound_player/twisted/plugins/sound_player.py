from justrelax.node.plugin import AbstractNodeServiceMaker
from justrelax.node.sound_player import SoundPlayer


class ServiceMaker(AbstractNodeServiceMaker):
    service = SoundPlayer


service_maker = ServiceMaker()
