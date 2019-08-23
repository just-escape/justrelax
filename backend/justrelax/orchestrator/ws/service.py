from twisted.application import internet

from justrelax.orchestrator.ws.factory import JustSockServerFactory


class JustSockServerService(internet.TCPServer):
    def __init__(self, port, *args, **kwargs):
        self.factory = JustSockServerFactory(self)

        super(JustSockServerService, self).__init__(port, self.factory, *args, **kwargs)
