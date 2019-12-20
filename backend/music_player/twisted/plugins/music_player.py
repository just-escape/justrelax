from justrelax.node.plugin import AbstractNodeServiceMaker
from justrelax.node.music_player import MusicPlayer


class ServiceMaker(AbstractNodeServiceMaker):
    service = MusicPlayer


service_maker = ServiceMaker()
