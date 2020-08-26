import gpiozero

from justrelax.node.service import JustSockClientService, EventCategoryToMethodMixin
from justrelax.common.logging_utils import logger


class OutputDevice(EventCategoryToMethodMixin, JustSockClientService):
    def __init__(self, *args, **kwargs):
        super(OutputDevice, self).__init__(*args, **kwargs)

        on_by_default = self.node_params.get("on_by_default", False)
        custom_keywords = self.node_params.get("custom_keywords", {})

        custom_high = custom_keywords.get("high", None)
        if custom_high:
            setattr(
                self,
                "{}{}{}".format(
                    EventCategoryToMethodMixin.METHOD_PREFIX,
                    EventCategoryToMethodMixin.METHOD_SEPARATOR,
                    custom_high
                ),
                self.event_high
            )

        custom_low = custom_keywords.get("low", None)
        if custom_low:
            setattr(
                self,
                "{}{}{}".format(
                    EventCategoryToMethodMixin.METHOD_PREFIX,
                    EventCategoryToMethodMixin.METHOD_SEPARATOR,
                    custom_low
                ),
                self.event_low
            )

        pin = self.node_params["pin"]
        self.device = gpiozero.OutputDevice(pin)

        if on_by_default:
            self.event_high()
        else:
            self.event_low()

    def event_high(self):
        logger.debug("Setting device pin to high")
        self.device.on()

    def event_low(self):
        logger.debug("Setting device pin to low")
        self.device.off()
