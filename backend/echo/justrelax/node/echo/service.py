from justrelax.node.service import JustSockClientService


class Echo(JustSockClientService):
    def process_event(self, event):
        self.send_event(event)
