import gpiozero

from justrelax.node.service import JustSockClientService
from justrelax.common.logging_utils import logger


class OutputDevice(JustSockClientService):
    class PROTOCOL:
        ACTION = "action"

        HIGH = "on"
        LOW = "off"

    def __init__(self, *args, **kwargs):
        super(OutputDevice, self).__init__(*args, **kwargs)

        custom_keywords = self.node_params.get("custom_keywords", {})

        custom_high = custom_keywords.get("high", None)
        if custom_high:
            self.PROTOCOL.HIGH = custom_high

        custom_low = custom_keywords.get("low", None)
        if custom_low:
            self.PROTOCOL.LOW = custom_low

        pin = self.node_params["pin"]
        self.device = gpiozero.OutputDevice(pin)

    def process_event(self, event):
        logger.debug("Processing event '{}'".format(event))
        if type(event) is not dict:
            logger.error("Unknown event: skipping")
            return

        if self.PROTOCOL.ACTION not in event:
            logger.error("Event has no action: skipping")
            return

        if event[self.PROTOCOL.ACTION] == self.PROTOCOL.HIGH:
            logger.debug("Setting device pin to high")
            self.device.on()

        elif event[self.PROTOCOL.ACTION] == self.PROTOCOL.LOW:
            logger.debug("Setting device pin to low")
            self.device.off()

        else:
            logger.warning("Unknown action type '{}': skipping".format(
                event[self.PROTOCOL.ACTION]))
