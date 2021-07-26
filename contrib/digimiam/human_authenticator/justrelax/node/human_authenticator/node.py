from twisted.internet import reactor

from justrelax.core.logging_utils import logger
from justrelax.core.node import MagicNode, on_event


class ArduinoProtocol:
    CATEGORY = "c"

    ERROR = "e"
    AUTHENTICATE = "a"
    CANCEL_AUTHENTICATION = "c"

    PLAYING = "p"
    DISABLED = "d"
    SUCCESS = "w"


class HumanAuthenticator(MagicNode):
    STATUSES = {'playing', 'disabled', 'success'}

    def __init__(self, *args, **kwargs):
        self._status = None

        super(HumanAuthenticator, self).__init__(*args, **kwargs)

        self.authenticators = {}
        for serial in self.config['serials']:
            port = serial['port']
            self.authenticators[port] = False

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

        for port in self.authenticators.keys():
            self.send_serial({ArduinoProtocol.CATEGORY: category}, port)

    def on_playing(self):
        for authenticator in self.authenticators:
            self.authenticators[authenticator] = False

    def on_success(self):
        logger.info("Success")
        self.publish({"category": "success"})

    @on_event(filter={"category": "set_status"})
    def event_set_status(self, status: str):
        logger.info("Setting status to {}".format(status))
        self.status = status

    @on_event(filter={"category": "reset"})
    def event_reset(self):
        logger.info("Resetting")
        self.status = "playing"

    @on_event(filter={ArduinoProtocol.CATEGORY: ArduinoProtocol.CANCEL_AUTHENTICATION})
    def cancel_authentication(self, port, /, t):
        logger.info(f"{port} has canceled authentication with tag {t}")
        self.authenticators[port] = False

    @on_event(filter={ArduinoProtocol.CATEGORY: ArduinoProtocol.AUTHENTICATE})
    def authenticate(self, port, /, t):
        logger.info(f"{port} has authenticated with tag {t}")

        if t == 0:  # False positive
            logger.info("False positive detected: skipping")
            return

        self.authenticators[port] = True

        if all(is_authenticated for is_authenticated in self.authenticators.values()):
            self.status = "success"
