from twisted.internet import reactor

from justrelax.core.node import MagicNode, on_event
from justrelax.core.logging_utils import logger


class ArduinoProtocol:
    CATEGORY = 'c'

    SET_TARGET_FREQ = 't'
    SET_FREQ = 'f'
    VALUE = 'v'
    STEP = 's'


class StockLights(MagicNode):
    def __init__(self, *args, **kwargs):
        super(StockLights, self).__init__(*args, **kwargs)

        if self.config['on_by_default']:
            # Init once we are sure the serial port will be able to receive data
            reactor.callLater(3, self.event_high)

    @on_event(filter={'category': 'set_target_freq'})
    def event_set_target_freq(self, value: float, step: float):
        value = min(value, 50.)
        logger.info("Set lights target freq to {}/50 with a step of {}".format(value, step))
        self.send_serial({
            ArduinoProtocol.CATEGORY: ArduinoProtocol.SET_TARGET_FREQ,
            ArduinoProtocol.VALUE: value,
            ArduinoProtocol.STEP: step,
        })

    @on_event(filter={'category': 'set_freq'})
    def event_set_freq(self, value: float):
        value = min(value, 50.)
        logger.info("Set lights freq to {}/50".format(value))
        self.send_serial({
            ArduinoProtocol.CATEGORY: ArduinoProtocol.SET_FREQ,
            ArduinoProtocol.VALUE: value,
        })

    @on_event(filter={'category': 'high'})
    def event_high(self):
        logger.info("Set lights intensity to high")
        self.event_set_target_freq(50., 0.2)

    @on_event(filter={'category': 'low'})
    def event_low(self):
        logger.info("Set lights intensity to low")
        self.event_set_target_freq(1., 0.2)

    @on_event(filter={'category': 'off'})
    def event_off(self):
        logger.info("Set lights off")
        self.event_set_freq(0.,)

    @on_event(filter={'category': 'reset'})
    def event_reset(self):
        logger.info("Reset")
        if self.config['on_by_default']:
            self.event_high()
        else:
            self.event_off()
