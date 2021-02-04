from justrelax.node.plugin import AbstractNodeServiceMaker
from justrelax.node.human_authenticator import HumanAuthenticator


class ServiceMaker(AbstractNodeServiceMaker):
    service = HumanAuthenticator


service_maker = ServiceMaker()
