# from justrelax.common.logging_utils import logging
from justrelax.node.service import JustSockNodeClientService


class Niryo(JustSockNodeClientService):
    def process_message(self, message):
        self.factory.send_message(message)
