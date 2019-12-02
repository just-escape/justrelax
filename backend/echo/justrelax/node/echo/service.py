from justrelax.node.service import JustSockNodeClientService


class Echo(JustSockNodeClientService):
    def process_message(self, message):
        self.factory.send_message(message)
