import json

from twisted.internet import reactor
from twisted.internet.serialport import SerialPort

from justrelax.common.logging_utils import logger
from justrelax.node.service import JustSockClientService
from justrelax.node.protocol import JSONSerialProtocol


class Proxuino(JustSockClientService):
    def __init__(self, *args, **kwargs):
        super(Proxuino, self).__init__(*args, **kwargs)

        port = self.node_params['port']
        baud_rate = self.node_params['baud_rate']
        self.serial_protocol = JSONSerialProtocol(self.on_arduino_event)
        SerialPort(self.serial_protocol, port, reactor, baudrate=baud_rate)

    def on_arduino_event(self, event):
        try:
            self.send_event(event)
        except Exception as e:
            formatted_exception = "{}: {}".format(type(e).__name__, e)
            self.factory.protocol.send_log_error("Error while trying to forward event={}: {}".format(
                event, formatted_exception))
            logger.error("Error while trying to forward event={}".format(event))
            logger.exception()

    def process_event(self, event):
        self.serial_protocol.sendLine(json.dumps(event).encode())
