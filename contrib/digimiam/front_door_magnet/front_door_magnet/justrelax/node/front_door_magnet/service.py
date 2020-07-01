import gpiozero

from twisted.internet.task import LoopingCall

from justrelax.node.service import JustSockClientService, EventCategoryToMethodMixin
from justrelax.common.logging_utils import logger


class FrontDoorMagnet(EventCategoryToMethodMixin, JustSockClientService):
    def __init__(self, *args, **kwargs):
        super(FrontDoorMagnet, self).__init__(*args, **kwargs)

        button_pin = self.node_params["emergency_button_pin"]
        self.emergency_button_hold_time = self.node_params["emergency_button_hold_time"]
        self.emergency_button = gpiozero.Button(button_pin, hold_time=self.emergency_button_hold_time)
        self.is_emergency_button_held = False

        self.watch_emergency_button = LoopingCall(self.check_emergency_button)
        self.watch_emergency_button.start(0.01)

        magnet_pin = self.node_params["magnet_pin"]
        self.magnet = gpiozero.OutputDevice(magnet_pin)

    def check_emergency_button(self):
        if self.emergency_button.is_held:
            if not self.is_emergency_button_held:
                logger.info(
                    "The emergency button has been held for {} second(s)".format(self.emergency_button_hold_time))
                self.event_unlock()
        else:
            if self.is_emergency_button_held:
                logger.info("The emergency button has been released")

        self.is_emergency_button_held = self.emergency_button.is_held

    def event_unlock(self):
        logger.info("Unlocking the front door")
        self.magnet.off()

    def event_lock(self):
        logger.info("Locking the front door")
        self.magnet.on()
