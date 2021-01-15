from justrelax.node.plugin import AbstractNodeServiceMaker
from justrelax.node.stock_lights import StockLights


class ServiceMaker(AbstractNodeServiceMaker):
    service = StockLights


service_maker = ServiceMaker()
