from justrelax.node.plugin import AbstractNodeServiceMaker
from justrelax.node.video_player import VideoPlayer


class ServiceMaker(AbstractNodeServiceMaker):
    service = VideoPlayer


service_maker = ServiceMaker()
