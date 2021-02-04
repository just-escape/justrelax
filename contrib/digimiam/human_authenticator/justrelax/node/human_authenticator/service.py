from twisted.internet import reactor

from justrelax.node.helper import Serial

from justrelax.common.logging_utils import logger
from justrelax.node.service import JustSockClientService, event


class SerialEventBuffer:
    def __init__(self, serial, interval):
        self.queue = []

        self.serial = serial
        self.interval = interval

        self.delay_task = None

    def _send_event(self, event):
        self.serial.send_event(event)
        self.delay_task = reactor.callLater(self.interval, self.pop_event)

    def send_event(self, event):
        if self.delay_task and self.delay_task.active():
            self.queue.append(event)

        else:
            self._send_event(event)

    def pop_event(self):
        if not self.queue:
            return

        event = self.queue.pop(0)
        self._send_event(event)


class HumanAuthenticator(JustSockClientService):
    STATUSES = {'playing', 'disabled', 'success'}

    class ARDUINO_PROTOCOL:
        CATEGORY = "c"

        ERROR = "e"
        AUTHENTICATE = "a"
        CANCEL_AUTHENTICATION = "c"

        PLAYING = "p"
        DISABLED = "d"
        SUCCESS = "w"

    def __init__(self, *args, **kwargs):
        self._status = None

        super(HumanAuthenticator, self).__init__(*args, **kwargs)

        self.authenticators = []
        for authenticator_index, authenticator in enumerate(self.node_params['authenticators']):
            port = authenticator['port']
            baud_rate = authenticator['baud_rate']
            buffering_interval = authenticator['buffering_interval']

            serial = Serial(self, port, baud_rate, self.process_serial_event, authenticator_index)
            buffer = SerialEventBuffer(serial, buffering_interval)

            self.authenticators.append({'arduino': buffer, 'authenticated': False})

        reactor.callLater(3, self.event_reset)

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if value not in self.STATUSES:
            logger.error("Unknown status {} (must be one of {}): skipping".format(
                value, ", ".join(self.STATUSES)
            ))
            return

        if self.status == value:
            logger.info("Status is already {}: skipping".format(value))
            return

        self._status = value

        if self.status == 'playing':
            category = self.ARDUINO_PROTOCOL.PLAYING
            self.on_playing()
        elif self.status == 'success':
            category = self.ARDUINO_PROTOCOL.SUCCESS
            self.on_success()
        else:
            # status is disabled
            category = self.ARDUINO_PROTOCOL.DISABLED

        for authenticator in self.authenticators:
            authenticator['arduino'].send_event({self.ARDUINO_PROTOCOL.CATEGORY: category})

    def on_playing(self):
        for authenticator in self.authenticators:
            authenticator["authenticated"] = False

    def on_success(self):
        logger.info("Success")
        self.send_event({"category": "success"})

    @event(filter={"category": "set_status"})
    def event_set_status(self, status: str):
        logger.info("Setting status to {}".format(status))
        self.status = status

    @event(filter={"category": "reset"})
    def event_reset(self):
        logger.info("Resetting")
        self.status = "playing"

    def process_serial_event(self, event, authenticator_index):
        logger.debug("Processing event '{}' (from authenticator index={})".format(event, authenticator_index))

        if self.ARDUINO_PROTOCOL.CATEGORY not in event:
            logger.error("Event has not category: skipping")
            return

        if event[self.ARDUINO_PROTOCOL.CATEGORY] == self.ARDUINO_PROTOCOL.AUTHENTICATE:
            self.authenticate(authenticator_index)

        elif event[self.ARDUINO_PROTOCOL.CATEGORY] == self.ARDUINO_PROTOCOL.CANCEL_AUTHENTICATION:
            self.cancel_authentication(authenticator_index)

        else:
            logger.error("Unknown event category '{}': skipping".format(event[self.ARDUINO_PROTOCOL.CATEGORY]))

    def cancel_authentication(self, authenticator_index):
        self.authenticators[authenticator_index]['authenticated'] = False

    def authenticate(self, authenticator_index):
        self.authenticators[authenticator_index]['authenticated'] = True

        if all(authenticator['authenticated'] for authenticator in self.authenticators):
            self.status = "success"
