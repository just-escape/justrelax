from twisted.application import internet

from justrelax.common.logging_utils import logger
from justrelax.node.factory import JustSockNodeClientFactory


class JustSockNodeClientService(internet.TCPClient):
    def __init__(self, host, port, name, channel, node_params, *args, **kwargs):
        self.host = host
        self.port = port

        self.factory = JustSockNodeClientFactory(self, name, channel)

        self.node_params = node_params

        super(JustSockNodeClientService, self).__init__(host, port, self.factory, *args, **kwargs)

    def startService(self):
        logger.info("Starting service '{}' on '{}:{}'".format(self.name, self.host, self.port))
        self.start()
        super(JustSockNodeClientService, self).startService()

    def start(self):
        pass

    def stopService(self):
        self.stop()
        super(JustSockNodeClientService, self).stopService()

    def stop(self):
        pass

    def process_message(self, message):
        pass
