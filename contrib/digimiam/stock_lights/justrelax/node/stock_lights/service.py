from twisted.internet import reactor

from justrelax.node.service import JustSockClientService, orchestrator_event
from justrelax.node.helper import BufferedSerial
from justrelax.common.logging_utils import logger


class ArduinoProtocol:
    CATEGORY = 'c'

    SET_TARGET_FREQ = 't'
    SET_FREQ = 'f'
    VALUE = 'v'
    STEP = 's'


class StockLights(JustSockClientService):
    def __init__(self, *args, **kwargs):
        super(StockLights, self).__init__(*args, **kwargs)

        port = self.node_params['arduino']['port']
        baud_rate = self.node_params['arduino']['baud_rate']

        self.serial = BufferedSerial(self, port, baud_rate)
        self.serial.process_event = self.process_serial_event

        if self.node_params['on_by_default']:
            # Init once we are sure the serial port will be able to receive data
            reactor.callLater(3, self.event_high)

    @staticmethod
    def process_serial_event(event):
        # Error by default because events should not be received from the arduino
        logger.error(event)

    @orchestrator_event(filter={'category': 'set_target_freq'})
    def event_set_target_freq(self, value: float, step: float):
        value = min(value, 50.)
        logger.info("Set lights target freq to {}/50 with a step of {}".format(value, step))
        self.serial.send_event({
            ArduinoProtocol.CATEGORY: ArduinoProtocol.SET_TARGET_FREQ,
            ArduinoProtocol.VALUE: value,
            ArduinoProtocol.STEP: step,
        })

    @orchestrator_event(filter={'category': 'set_freq'})
    def event_set_freq(self, value: float):
        value = min(value, 50.)
        logger.info("Set lights freq to {}/50".format(value))
        self.serial.send_event({
            ArduinoProtocol.CATEGORY: ArduinoProtocol.SET_FREQ,
            ArduinoProtocol.VALUE: value,
        })

    @orchestrator_event(filter={'category': 'high'})
    def event_high(self):
        logger.info("Set lights intensity to high")
        self.event_set_target_freq(50., 0.2)

    @orchestrator_event(filter={'category': 'low'})
    def event_low(self):
        logger.info("Set lights intensity to low")
        self.event_set_target_freq(1., 0.2)

    @orchestrator_event(filter={'category': 'off'})
    def event_off(self):
        logger.info("Set lights off")
        self.event_set_freq(0.,)
