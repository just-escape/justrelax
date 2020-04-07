import json

from twisted.internet import reactor
from twisted.internet.serialport import SerialPort

from justrelax.node.service import JustSockClientService
from justrelax.node.protocol import JSONSerialProtocol


class Proxuino(JustSockClientService):
    def __init__(self, *args, **kwargs):
        super(Proxuino, self).__init__(*args, **kwargs)

        port = self.node_params['port']
        baud_rate = self.node_params['baud_rate']
        self.serial_protocol = JSONSerialProtocol(self)
        SerialPort(self.serial_protocol, port, reactor, baudrate=baud_rate)

    def process_arduino_event(self, event):
        self.send_event(event)

    def process_event(self, event):
        self.serial_protocol.sendLine(json.dumps(event).encode())
