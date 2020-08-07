from twisted.internet import reactor
from twisted.internet.serialport import SerialPort

from justrelax.node.protocol import JSONSerialProtocol

from justrelax.common.logging_utils import logger


class Serial:
    def __init__(self, service, port, baud_rate=9600, on_event_callback=None, *cb_args, **cb_kwargs):
        self.service = service
        self.port = port
        self.baud_rate = baud_rate

        self.cb_args = cb_args
        self.cb_kwargs = cb_kwargs

        if on_event_callback is None:
            self.on_event_callback = self.service.process_serial_event
        else:
            self.on_event_callback = on_event_callback

        self.reconnection_delay = 10

        self.protocol = None
        self.connect()

    def connect(self):
        try:
            self.protocol = JSONSerialProtocol(self.process_event, self.process_parse_exception, self.connection_lost)
            SerialPort(self.protocol, self.port, reactor, baudrate=self.baud_rate)
        except Exception as e:
            reactor.callLater(self.reconnection_delay, self.connect)
            formatted_exception = "{}: {}".format(type(e).__name__, e)
            try:
                self.service.factory.protocol.send_log_error(
                    "Error while trying to connect to serial on port {} ({})".format(self.port, formatted_exception))
            except Exception:
                pass
            logger.error("Error while trying to connect to serial on port {} ({})".format(
                self.port, formatted_exception))

    def connection_lost(self, reason):
        try:
            self.service.factory.protocol.send_log_error("Connection lost with port {} (reason={})".format(
                self.port, reason))
        except Exception:
            pass
        logger.error("Connection lost with port {} (reason={})".format(self.port, reason))

        self.protocol = None
        reactor.callLater(self.reconnection_delay, self.connect)

    def process_event(self, event):
        try:
            self.on_event_callback(event, *self.cb_args, **self.cb_kwargs)
        except Exception as e:
            formatted_exception = "{}: {}".format(type(e).__name__, e)
            try:
                self.service.factory.protocol.send_log_error(
                    "Error while trying to process arduino event={} ({})".format(event, formatted_exception))
            except Exception:
                pass
            logger.error("Error while trying to process arduino event={} ({})".format(event, formatted_exception))

    def process_parse_exception(self, line, exception):
        formatted_exception = "{}: {}".format(type(exception).__name__, exception)
        try:
            self.service.factory.protocol.send_log_error("Error while trying to forward arduino line={} ({})".format(
                line, formatted_exception))
        except Exception:
            pass
        logger.error("Error while trying to forward arduino line={} ({})".format(line, formatted_exception))

    def send_event(self, event):
        if self.protocol:
            self.protocol.send_event(event)
        else:
            try:
                self.service.factory.protocol.send_log_error(
                    "Cannot send event {} to {} because the connection is not established: skipping".format(
                        self.port, event))
            except Exception:
                pass
            logger.error("Cannot send event {} to {} because the connection is not established: skipping".format(
                self.port, event))
