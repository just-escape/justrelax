import gpiozero

from twisted.internet import reactor

from justrelax.core.node import MagicNode, on_event
from justrelax.core.logging_utils import logger


class VentsLocker(MagicNode):
    def __init__(self, *args, **kwargs):
        super(VentsLocker, self).__init__(*args, **kwargs)

        power_pin = self.config["power_pin"]
        limit_switch_pin = self.config["limit_switch_pin"]
        self.unlock_frequency = self.config["unlock_frequency"]
        self.unlock_falling_edge_delay = self.config["unlock_falling_edge_delay"]
        self.device = gpiozero.OutputDevice(power_pin)
        self.limit_switch_power = gpiozero.OutputDevice(self.config["limit_switch_power_pin"])
        self.limit_switch_power.on()
        self.limit_switch = gpiozero.InputDevice(limit_switch_pin)

        self.locked = self.config["locked_by_default"]

        self.check_lock_mistake()

    @on_event(filter={'category': 'reset'})
    def event_reset(self):
        logger.info("Reset")
        self.locked = self.config["locked_by_default"]

    def check_lock_mistake(self):
        reactor.callLater(self.unlock_frequency, self.check_lock_mistake)
        logger.debug("Checking that locker is not locked (to prevent players from locking by mistake)")

        if not self.locked and self.limit_switch.value:
            logger.info("Locker was locked while it should not have been: unlocking")
            self.event_unlock()

    @on_event(filter={'category': 'unlock'})
    def event_unlock(self):
        self.locked = False
        logger.info("Unlock rising edge: setting device pin to high")
        self.device.on()

        def unlock_falling_edge():
            logger.info("Unlock falling edge: setting device pin to low")
            self.device.off()

        reactor.callLater(self.unlock_falling_edge_delay, unlock_falling_edge)

    @on_event(filter={'category': 'lock'})
    def event_lock(self):
        logger.info("Locking")
        self.locked = True
