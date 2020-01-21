try:
    from RPi import GPIO
except RuntimeError:
    from mock import MagicMock
    GPIO = MagicMock()

from justrelax.node.service import JustSockClientService
from justrelax.common.logging_utils import logger


class Led(JustSockClientService):
    PIN = None

    class PROTOCOL:
        LED_ON = "on"
        LED_OFF = "off"

    def start(self):
        self.PIN = self.node_params.get('pin', None)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.PIN, GPIO.OUT)
        GPIO.output(self.PIN, False)

    def stop(self):
        GPIO.cleanup()

    def process_event(self, event):
        logger.debug("Processing event '{}'".format(event))
        if event == self.PROTOCOL.LED_ON:
            GPIO.output(self.PIN, True)
        elif event == self.PROTOCOL.LED_OFF:
            GPIO.output(self.PIN, False)
        else:
            logger.debug("Unknown event: skipping")
