from justrelax.node.service import JustSockClientService
from justrelax.node.helper import Serial


class Proxuino(JustSockClientService):
    def __init__(self, *args, **kwargs):
        super(Proxuino, self).__init__(*args, **kwargs)

        port = self.node_params['port']
        baud_rate = self.node_params['baud_rate']
        self.serial = Serial(self, port, baud_rate)

    def process_serial_event(self, event):
        self.send_event(event)

    def process_event(self, event):
        self.serial.send_event(event)
