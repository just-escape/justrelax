from justrelax.node.service import JustSockNodeClientService


class Echo(JustSockNodeClientService):
    def process_event(self, event):
        self.factory.send_event(event)
