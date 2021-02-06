from twisted.internet import reactor

from justrelax.node.helper import BufferedSerial, serial_event

from justrelax.common.logging_utils import logger
from justrelax.node.service import JustSockClientService, orchestrator_event


class ArduinoProtocol:
    CATEGORY = "c"

    ERROR = "e"
    AUTHENTICATE = "a"
    CANCEL_AUTHENTICATION = "c"

    PLAYING = "p"
    DISABLED = "d"
    SUCCESS = "w"


class HumanAuthenticator(JustSockClientService):
    STATUSES = {'playing', 'disabled', 'success'}

    def __init__(self, *args, **kwargs):
        self._status = None

        super(HumanAuthenticator, self).__init__(*args, **kwargs)

        self.authenticators = {}
        for authenticator_index, authenticator in enumerate(self.node_params['authenticators']):
            port = authenticator['port']
            baud_rate = authenticator['baud_rate']
            buffering_interval = authenticator['buffering_interval']

            serial = BufferedSerial(self, port, baud_rate, buffering_interval)

            self.authenticators[port] = {'arduino': serial, 'authenticated': False}

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
            category = ArduinoProtocol.PLAYING
            self.on_playing()
        elif self.status == 'success':
            category = ArduinoProtocol.SUCCESS
            self.on_success()
        else:
            # status is disabled
            category = ArduinoProtocol.DISABLED

        for authenticator in self.authenticators.values():
            authenticator['arduino'].send_event({ArduinoProtocol.CATEGORY: category})

    def on_playing(self):
        for authenticator in self.authenticators.values():
            authenticator["authenticated"] = False

    def on_success(self):
        logger.info("Success")
        self.send_event({"category": "success"})

    @orchestrator_event(filter={"category": "set_status"})
    def event_set_status(self, status: str):
        logger.info("Setting status to {}".format(status))
        self.status = status

    @orchestrator_event(filter={"category": "reset"})
    def event_reset(self):
        logger.info("Resetting")
        self.status = "playing"

    @serial_event(filter={ArduinoProtocol.CATEGORY: ArduinoProtocol.CANCEL_AUTHENTICATION})
    def cancel_authentication(self, port):
        self.authenticators[port]['authenticated'] = False

    @serial_event(filter={ArduinoProtocol.CATEGORY: ArduinoProtocol.AUTHENTICATE})
    def authenticate(self, port):
        self.authenticators[port]['authenticated'] = True

        if all(authenticator['authenticated'] for authenticator in self.authenticators.values()):
            self.status = "success"
