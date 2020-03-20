import json

from twisted.internet import reactor
from twisted.internet.serialport import SerialPort
from twisted.protocols.basic import LineOnlyReceiver

from justrelax.common.logging_utils import logger
from justrelax.node.service import JustSockClientService


class SerialProtocol(LineOnlyReceiver):
    delimiter = b'\n'

    def __init__(self, on_line_callback):
        self.on_line_callback = on_line_callback

    def lineReceived(self, line):
        self.on_line_callback(line)


class Proxuino(JustSockClientService):
    def start(self):
        port = self.node_params['port']
        baud_rate = self.node_params['baud_rate']
        self.serial_protocol = SerialProtocol(self.on_arduino_line)
        SerialPort(self.serial_protocol, port, reactor, baudrate=baud_rate)

    def on_arduino_line(self, line):
        try:
            decoded_line = line.decode('ascii')
            event = json.loads(decoded_line)
            self.factory.send_event(event)
        except Exception as e:
            formatted_exception = "{}: {}".format(type(e).__name__, e)
            self.factory.protocol.send_log_error("Error while trying to forward line={}: {}".format(
                line, formatted_exception))
            logger.error("Error while trying to forward line={}".format(line))
            logger.exception()

    def process_event(self, event):
        self.serial_protocol.sendLine(json.dumps(event).encode())
