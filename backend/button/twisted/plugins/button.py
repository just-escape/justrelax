from justrelax.node.plugin import AbstractNodeServiceMaker
from justrelax.node.button import Button


class ServiceMaker(AbstractNodeServiceMaker):
    tapname = "button"
    service = Button


service_maker = ServiceMaker()
