from justrelax.core.node import MagicNode, on_event
from twisted.internet import reactor


class Echo(MagicNode):
    @on_event
    def any_event(self, **kwargs):
        self.publish(kwargs)
