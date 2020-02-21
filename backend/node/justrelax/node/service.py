from twisted.application import internet

from justrelax.common.logging_utils import logger
from justrelax.node.factory import JustSockClientFactory


class JustSockClientService(internet.TCPClient):
    def __init__(self, host, port, name, channel, node_params, *args, **kwargs):
        self.host = host
        self.port = port

        self.factory = JustSockClientFactory(self, name, channel)

        self.node_params = node_params

        super(JustSockClientService, self).__init__(host, port, self.factory, *args, **kwargs)

    def startService(self):
        logger.info("Starting service '{}' on '{}:{}'".format(self.name, self.host, self.port))
        self.start()
        super(JustSockClientService, self).startService()

    def start(self):
        pass

    def stopService(self):
        self.stop()
        super(JustSockClientService, self).stopService()

    def stop(self):
        pass

    def process_event(self, event):
        pass
