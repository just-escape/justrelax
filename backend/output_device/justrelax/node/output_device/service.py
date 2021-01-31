import gpiozero

from justrelax.node.service import JustSockClientService, event
from justrelax.common.logging_utils import logger


class OutputDevice(JustSockClientService):
    def __init__(self, *args, **kwargs):
        super(OutputDevice, self).__init__(*args, **kwargs)

        on_by_default = self.node_params.get("on_by_default", False)

        pin = self.node_params["pin"]
        self.device = gpiozero.OutputDevice(pin)

        if on_by_default:
            self.event_high()
        else:
            self.event_low()

    @event(filter={'category': 'high'})
    def event_high(self):
        logger.debug("Setting device pin to high")
        self.device.on()

    @event(filter={'category': 'low'})
    def event_low(self):
        logger.debug("Setting device pin to low")
        self.device.off()
