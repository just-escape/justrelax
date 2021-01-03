from justrelax.node.plugin import AbstractNodeServiceMaker
from justrelax.node.laser_maze import LaserMaze


class ServiceMaker(AbstractNodeServiceMaker):
    service = LaserMaze


service_maker = ServiceMaker()
