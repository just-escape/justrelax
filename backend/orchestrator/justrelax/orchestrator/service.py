from twisted.application import internet

from justrelax.orchestrator.factory import PublishSubscribeServerFactory


class PublishSubscribeServerService(internet.TCPServer):
    def __init__(self, port, *args, **kwargs):
        self.factory = PublishSubscribeServerFactory(self)

        super(PublishSubscribeServerService, self).__init__(port, self.factory, *args, **kwargs)
