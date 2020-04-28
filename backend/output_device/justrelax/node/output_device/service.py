import gpiozero

from justrelax.node.service import JustSockClientService, EventCategoryToMethodMixin
from justrelax.common.logging_utils import logger


class OutputDevice(EventCategoryToMethodMixin, JustSockClientService):
    def __init__(self, *args, **kwargs):
        super(OutputDevice, self).__init__(*args, **kwargs)

        custom_keywords = self.node_params.get("custom_keywords", {})

        custom_high = custom_keywords.get("high", None)
        if custom_high:
            setattr(self, "process_{}".format(custom_high), self.process_high)

        custom_low = custom_keywords.get("low", None)
        if custom_low:
            setattr(self, "process_{}".format(custom_low), self.process_high)

        pin = self.node_params["pin"]
        self.device = gpiozero.OutputDevice(pin)

    def process_high(self):
        logger.debug("Setting device pin to high")
        self.device.on()

    def process_low(self):
        logger.debug("Setting device pin to low")
        self.device.off()
