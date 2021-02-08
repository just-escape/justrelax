from justrelax.node.service import MagicNode, on_event


class Echo(MagicNode):
    @on_event
    def any_event(self, channel, /, **kwargs):
        logger.info("{}: {}".format(channel, kwargs))
