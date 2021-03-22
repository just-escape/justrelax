from copy import copy
from random import shuffle

from twisted.internet import reactor

from justrelax.core.logging_utils import logger
from justrelax.core.node import MagicNode, on_event


class ArduinoProtocol:
    CATEGORY = "c"

    ERROR = "e"
    AUTHENTICATE = "a"
    CANCEL_AUTHENTICATION = "c"
    TAG = "t"

    PLAYING = "p"
    DISABLED = "d"


class PaymentModule(MagicNode):
    STATUSES = {'playing', 'disabled'}

    def __init__(self, *args, **kwargs):
        self._status = None

        super(PaymentModule, self).__init__(*args, **kwargs)

        self.credits = self.config['credits']
        self.credits_filo = []
        self.tag_credits = {}

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

        category = ArduinoProtocol.PLAYING if self.status == 'playing' else ArduinoProtocol.DISABLED
        self.send_serial({ArduinoProtocol.CATEGORY: category})

    @on_event(filter={"category": "set_status"})
    def event_set_status(self, status: str):
        logger.info("Setting status to {}".format(status))
        self.status = status

    @on_event(filter={"category": "reset"})
    def event_reset(self):
        logger.info("Resetting")
        self.status = "playing"

        shuffle(self.credits)
        self.credits_filo = copy(self.config['credits'])
        self.tag_credits = {}

    @on_event(filter={ArduinoProtocol.CATEGORY: ArduinoProtocol.CANCEL_AUTHENTICATION})
    def cancel_authentication(self):
        self.publish({"category": "set_credits", "value": 0})

    @on_event(filter={ArduinoProtocol.CATEGORY: ArduinoProtocol.AUTHENTICATE})
    def authenticate(self, tag):
        if tag not in self.tag_credits:
            if not self.credits_filo:
                # Should not happen because sessions are supposed to be limited to 4 players but just in case a fifth
                # slips in...
                shuffle(self.credits)
                self.credits_filo = copy(self.config['credits'])

            self.tag_credits[tag] = self.credits_filo.pop()

        self.publish({"category": "set_credits", "value": self.tag_credits[tag]})
