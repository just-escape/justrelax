from twisted.internet import reactor

from justrelax.node.service import JustSockClientService, EventCategoryToMethodMixin
from justrelax.node.helper import Serial
from justrelax.common.logging_utils import logger


class StockLights(EventCategoryToMethodMixin, JustSockClientService):
    class ARDUINO_PROTOCOL:
        CATEGORY = 'c'

        WHITE_HIGH = 'h'
        WHITE_LOW = 'l'
        WHITE_OFF = 'o'

    def __init__(self, *args, **kwargs):
        super(StockLights, self).__init__(*args, **kwargs)

        port = self.node_params['arduino']['port']
        baud_rate = self.node_params['arduino']['baud_rate']

        self.serial = Serial(self, port, baud_rate)

        # Init once we are sure the serial port will be able to receive data
        reactor.callLater(3, self.event_high)

    def process_serial_event(self, event):
        # Error by default because events should not be received from the arduino
        logger.error(event)
        self.send_event(event)

    def event_high(self):
        logger.info("Set lights intensity to high")
        self.serial.send_event({
            self.ARDUINO_PROTOCOL.CATEGORY: self.ARDUINO_PROTOCOL.WHITE_HIGH
        })

    def event_low(self):
        logger.info("Set lights intensity to low")
        self.serial.send_event({
            self.ARDUINO_PROTOCOL.CATEGORY: self.ARDUINO_PROTOCOL.WHITE_LOW
        })

    def event_off(self):
        logger.info("Set lights off")
        self.serial.send_event({
            self.ARDUINO_PROTOCOL.CATEGORY: self.ARDUINO_PROTOCOL.WHITE_OFF
        })
