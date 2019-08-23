from twisted.application import internet
from twisted.web.server import Site

from justrelax.orchestrator.http.api import App


class JustRestService(internet.TCPServer):
    def __init__(self, port, *args, **kwargs):
        app = App()
        factory = Site(app.resource)

        super(JustRestService, self).__init__(port, factory, *args, **kwargs)
