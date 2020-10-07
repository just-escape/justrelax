from justrelax.common.logging_utils import logger
from justrelax.node.service import JustSockClientService


class SecureFloor(JustSockClientService):
    def __init__(self, *args, **kwargs):
        super(SecureFloor, self).__init__(*args, **kwargs)
        logger.info(self.node_params)
        self.send_event({'hello': 'world'})

    def event_hello(self):
        pass
