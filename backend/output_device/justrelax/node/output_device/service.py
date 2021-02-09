import gpiozero

from justrelax.core.node import MagicNode, on_event
from justrelax.core.logging_utils import logger


class OutputDevice(MagicNode):
    def __init__(self, *args, **kwargs):
        super(OutputDevice, self).__init__(*args, **kwargs)

        on_by_default = self.config.get("on_by_default", False)

        pin = self.config["pin"]
        self.device = gpiozero.OutputDevice(pin)

        if on_by_default:
            self.event_high()
        else:
            self.event_low()

    @on_event(filter={'category': 'high'})
    def event_high(self):
        logger.info("Setting device pin to high")
        self.device.on()

    @on_event(filter={'category': 'low'})
    def event_low(self):
        logger.info("Setting device pin to low")
        self.device.off()
