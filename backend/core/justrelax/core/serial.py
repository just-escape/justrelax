import json

from twisted.internet import reactor

from twisted.protocols.basic import LineOnlyReceiver
from twisted.internet.serialport import SerialPort

from justrelax.core.logging_utils import logger


class SimpleSerialProtocol(LineOnlyReceiver):
    delimiter = b'\n'


class Serial:
    def __init__(self, port, baud_rate=9600, buffering_interval=0.1):
        self.port = port
        self.baud_rate = baud_rate

        self.reconnection_delay = 10

        self.buffering_queue = []
        self.buffering_interval = buffering_interval
        self.buffering_task = None

        self.protocol = None
        self.connect()

    def connect(self):
        try:
            self.protocol = SimpleSerialProtocol()
            self.protocol.lineReceived = self.process_serial_event
            self.protocol.connectionLost = self.connection_lost

            SerialPort(self.protocol, self.port, reactor, baudrate=self.baud_rate)
            logger.info("Connected to serial port {} ({} bauds, {}s buffering interval)".format(
                self.port, self.baud_rate, self.buffering_interval))
        except Exception as e:
            reactor.callLater(self.reconnection_delay, self.connect)
            logger.error(
                "Error while trying to connect to serial port {}: retrying after {} seconds".format(
                    self.port, self.reconnection_delay),
                exc_info=True)

    def connection_lost(self, reason):
        logger.error("Serial port {} disconnected (reason={})".format(self.port, reason))

        self.protocol = None
        reactor.callLater(self.reconnection_delay, self.connect)

    def process_serial_event(self, event):
        decoded_event = event.decode('ascii', 'replace')

        try:
            try:
                dict_event = json.loads(decoded_event)
            except Exception as e:
                # Event cannot be parsed as JSON. We won't be able to automatically call decorated callbacks. It is possible
                # that the event sent was a plain string, which could be a legitimate case. So we just fail silently here.
                event_to_process = decoded_event
            else:
                event_to_process = dict_event

            # port is passed as argument to mimic the pub/sub channel behaviour and have the same interface as
            # the node service process_event method. It allows as well to use the same callback for several serial ports
            self.process_event(event_to_process, self.port)

        except Exception:
            logger.error("Error while trying to process arduino event={}".format(event), exc_info=True)

    def process_event(self, event, port):
        pass

    def send_event(self, event):
        if self.buffering_task and self.buffering_task.active():
            self.buffering_queue.append(event)

        else:
            self._send_event(event)

    def pop_event(self):
        if not self.buffering_queue:
            return

        event = self.buffering_queue.pop(0)
        self._send_event(event)

    def _send_event(self, event):
        """
        Event can be of any type. It will be dumped as JSON if it is a dict or formatted as a string otherwise.
        """

        self.buffering_task = reactor.callLater(self.buffering_interval, self.pop_event)

        if not self.protocol:
            logger.error(
                "Cannot send event '{}' to {} because the connection is not established: skipping".format(
                    event, self.port))
            return

        if isinstance(event, dict):
            try:
                formatted_event = json.dumps(event, separators=(',', ':'))
            except TypeError:
                logger.error(
                    "Error while trying to convert {} as json: skipping".format(event), exc_info=True)
                return

        else:
            # .format ensures the string type for any object
            formatted_event = "{}".format(event)

        # If some characters cannot be encoded, they are replaced by '?' (thanks to 'replace')
        encoded_event = "{}".format(formatted_event).encode('ascii', 'replace')

        logger.info("{} <<< {}".format(self.port, encoded_event))
        self.protocol.sendLine(encoded_event)
