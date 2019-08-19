try:
    from RPi import GPIO
except RuntimeError:
    from mock import MagicMock
    GPIO = MagicMock()

from justrelax.node.service import JustSockNodeClientService
from justrelax.common.logging import logger


class LEDNode(JustSockNodeClientService):
    PIN = None

    class COMMANDS:
        LED_ON = "on"
        LED_OFF = "off"

    def __init__(self, *args, **kwargs):
        super(LEDNode, self).__init__(*args, **kwargs)

    def start(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.PIN, GPIO.OUT)
        GPIO.output(self.PIN, False)

    def stop(self):
        GPIO.cleanup()

    def process_message(self, message):
        logger.debug("Processing message '{}'".format(message))
        if message == self.COMMANDS.LED_ON:
            GPIO.output(self.PIN, True)
        elif message == self.COMMANDS.LED_OFF:
            GPIO.output(self.PIN, False)
        else:
            logger.debug("Unknown message: skipping")


class LEDNodePin4(LEDNode):
    PIN = 4


class LEDNodePin14(LEDNode):
    PIN = 14
