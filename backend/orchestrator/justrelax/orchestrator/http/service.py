from importlib import import_module

from twisted.application import internet
from twisted.web.server import Site

from justrelax.orchestrator.http.core import resource


class JustRestService(internet.TCPServer):
    def __init__(self, port, *args, **kwargs):
        import_module('justrelax.orchestrator.http.room')
        import_module('justrelax.orchestrator.http.media')

        factory = Site(resource)

        super(JustRestService, self).__init__(port, factory, *args, **kwargs)
