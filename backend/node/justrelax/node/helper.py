from twisted.internet import reactor
from twisted.internet.serialport import SerialPort

from justrelax.node.protocol import SimpleSerialProtocol

from justrelax.common.logging_utils import logger


class SerialBuffer:
    def __init__(self, interval):
        self.queue = []

        self.interval = interval

        self.delay_task = None

    def send_event(self, event):
        if self.delay_task and self.delay_task.active():
            self.queue.append(event)

        else:
            self._send_event(event)
            self.delay_task = reactor.callLater(self.interval, self.pop_event)

    def pop_event(self):
        if not self.queue:
            return

        event = self.queue.pop(0)
        self._send_event(event)
        self.delay_task = reactor.callLater(self.interval, self.pop_event)


def serial_event(f=None, filter=None):
    def wrapper(f_):
        f_.serial_event_filter = filter if type(filter) is dict else {}
        return f_

    if f is None:
        return wrapper
    else:
        return wrapper(f)


class Serial:
    def __init__(self, service, port, baud_rate=9600):
        self.service = service
        self.port = port
        self.baud_rate = baud_rate

        self.reconnection_delay = 10

        self.event_callbacks = []
        self._gather_event_callbacks()

        self.protocol = None
        self.connect()

    def error(self, message):
        try:
            self.service.factory.protocol.send_log_error(message)
        except Exception:
            pass
        logger.error(message)

    def connect(self):
        try:
            self.protocol = SimpleSerialProtocol(self._process_event, self.connection_lost)
            SerialPort(self.protocol, self.port, reactor, baudrate=self.baud_rate)
        except Exception as e:
            reactor.callLater(self.reconnection_delay, self.connect)
            formatted_exception = "{}: {}".format(type(e).__name__, e)
            self.error("Error while trying to connect to serial on port {} ({})".format(self.port, formatted_exception))

    def connection_lost(self, reason):
        self.error("Connection lost with port {} (reason={})".format(self.port, reason))

        self.protocol = None
        reactor.callLater(self.reconnection_delay, self.connect)

    def _gather_event_callbacks(self):
        for attribute_name in dir(self):
            attribute = getattr(self, attribute_name)
            if not callable(attribute):
                continue

            # attribute is a method

            if hasattr(attribute, 'serial_event_filter'):
                self.event_callbacks.append({'callback': attribute, 'filter': attribute.filter})

    def _get_callbacks(self, event):
        callbacks = []

        for callback in self.event_callbacks:
            for key, value in callback['filter'].items():
                if key not in event or event[key] != value:
                    break
            else:
                callbacks.append(callback['callback'])

        return callbacks

    @staticmethod
    def _check_arguments(event, callback):
        callback_arguments = inspect.signature(callback).parameters
        for arg in callback_arguments.values():
            if arg.default is arg.empty:
                # No default value: a value must be defined in the event
                if arg.name not in event:
                    logger.error("Event has no {} field for {}: ignoring".format(arg.name, callback.__name__))
                    return False

                if arg.annotation is not arg.empty:
                    if type(event[arg.name]) is not arg.annotation:
                        logger.error("Event field {} type is not {} (received {}) for {}: ignoring".format(
                            arg.name, arg.annotation, type(event[arg.name]), callback.__name__))
                        return False

        return True

    @staticmethod
    def _get_trimmed_version_for_callback(event, callback):
        copied_event = deepcopy(event)

        for filter_key in callback.filter.keys():
            copied_event.pop(filter_key)

        # This inspection is not 100% proof. Positional only arguments or *args / **kwargs can mess
        # with this logic, but at least it covers a lot of cases.
        callback_arguments = inspect.signature(callback).parameters

        # Cast as a list so that the entire list is defined before we might pop fields.
        # Otherwise we would raise RuntimeError ("dictionary changed size during iteration").
        for field in list(copied_event.keys()):
            if field not in callback_arguments:
                copied_event.pop(field)

        return copied_event

    def _process_event(self, event):
        try:
            logger.debug("Processing serial event '{}' (from port {})".format(event, self.port))

            decoded_event = event.decode('ascii', 'replace')

            try:
                dict_event = json.loads(decoded_event)
            except Exception as e:
                # Event cannot be parsed as JSON. We won't be able to automatically dispatch it. It is possible that
                # the event sent was a plain string, which could be a legitimate case. So we just fail silently here.
                pass
            else:
                # Add an extra field to this event: the serial port it comes from, allowing to filter on it or receive
                # it in the callback parameters. Only add this field if it not already set.
                if 'port' not in dict_event:
                    dict_event['port'] = self.port

                callbacks = self._get_callbacks(dict_event)

                for callback in callbacks:
                    if not self._check_arguments(dict_event, callback):
                        continue
                    trimmed_event = self._get_trimmed_version_for_callback(dict_event, callback)

                    callback(**trimmed_event)

            self.process_event(event)

        except Exception as e:
            formatted_exception = "{}: {}".format(type(e).__name__, e)
            self.error("Error while trying to process arduino event={} ({})".format(event, formatted_exception))

    def process_event(self, event):
        """ Event is still raw (bytes, undecoded) """
        pass

    def process_parse_exception(self, line, exception):
        formatted_exception = "{}: {}".format(type(exception).__name__, exception)
        self.error("Error while trying to forward arduino line={} ({})".format(line, formatted_exception))

    def send_event(self, event):
        self._send_event()

    def _send_event(self, event):
        """
        Event can be of any type. It will be dumped as JSON if it is a dict or as a string otherwise.
        """

        if not self.protocol:
            self.error("Cannot send event '{}' to {} because the connection is not established: skipping".format(
                event, self.port))
            return

        if isinstance(event, dict):
            try:
                formatted_event = json.dumps(event, separators=(',', ':'))
            except TypeError as e:
                formatted_exception = "{}: {}".format(type(e).__name__, e)
                self.error("Error while trying to convert {} as json ({}): skipping".format(event, formatted_exception))
                return

        else:
            # .format ensures the string type for any object
            formatted_event = "{}".format(event)

        # If some characters cannot be encoded, they are replaced by '?' (thanks to 'replace')
        encoded_event = "{}".format(event).encode('ascii', 'replace')

        logger.debug("Sending {}".format(encoded_event))
        self.protocol.sendLine(encoded_event)


class BufferedSerial(SerialBuffer, Serial):
    def __init__(self, service, port, baud_rate=9600, buffering_interval=0.1):
        SerialBuffer.__init__(self, buffering_interval)
        Serial.__init__(self, service, port, baud_rate)
