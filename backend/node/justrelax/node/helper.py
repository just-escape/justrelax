from twisted.internet import reactor
from twisted.internet.serialport import SerialPort

from justrelax.node.protocol import JSONSerialProtocol

from justrelax.common.logging_utils import logger


class Serial:
    def __init__(self, service, port, baud_rate=9600, on_event_callback=None):
        self.service = service

        if on_event_callback is None:
            self.on_event_callback = self.service.process_arduino_event
        else:
            self.on_event_callback = on_event_callback

        self.protocol = JSONSerialProtocol(self.process_event, self.process_parse_exception)
        SerialPort(self.protocol, port, reactor, baudrate=baud_rate)

    def process_event(self, event):
        try:
            self.on_event_callback(event)
        except Exception as e:
            formatted_exception = "{}: {}".format(type(e).__name__, e)
            self.service.factory.protocol.send_log_error("Error while trying to process arduino event={}: {}".format(
                event, formatted_exception))
            logger.error("Error while trying to process arduino event={}".format(event))
            logger.exception()

    def process_parse_exception(self, line, exception):
        formatted_exception = "{}: {}".format(type(exception).__name__, exception)
        self.service.factory.protocol.send_log_error("Error while trying to forward arduino line={}: {}".format(
            line, formatted_exception))
        logger.error("Error while trying to forward arduino line={}".format(line))
        logger.exception()

    def send_event(self, event):
        self.protocol.send_event(event)
