import gpiozero

from twisted.internet import reactor

from justrelax.core.node import MagicNode, on_event
from justrelax.core.logging_utils import logger


class VentsLocker(MagicNode):
    def __init__(self, *args, **kwargs):
        super(VentsLocker, self).__init__(*args, **kwargs)

        pin = self.config["pin"]
        self.pulse_frequency = self.config["pulse_frequency"]
        self.device = gpiozero.OutputDevice(pin)

        self.unlock_pulsating_task = None
        self.unlock_falling_edge_task = None

        self._reset()

    def _reset(self):
        self.event_lock()

    @on_event(filter={'category': 'reset'})
    def event_reset(self):
        logger.info("Reset")
        self._reset()

    def pulse(self):
        logger.info("Triggering unlock pulse (to prevent players from locking by mistake)")
        self.event_unlock()

    def unlock_falling_edge(self):
        logger.info("Unlock falling edge: setting device pin to low")
        self.device.off()

    @on_event(filter={'category': 'unlock'})
    def event_unlock(self):
        logger.info("Unlock rising edge: setting device pin to high")
        self.device.on()

        if not self.unlock_falling_edge_task or not self.unlock_falling_edge_task.active():
            self.unlock_falling_edge_task = reactor.callLater(0.5, self.unlock_falling_edge)

        if not self.unlock_pulsating_task or not self.unlock_pulsating_task.active():
            self.unlock_pulsating_task = reactor.callLater(self.pulse_frequency, self.pulse)

    @on_event(filter={'category': 'lock'})
    def event_lock(self):
        logger.info("Setting device pin to low")
        self.device.off()

        if self.unlock_pulsating_task and self.unlock_pulsating_task.active():
            logger.info("Cancelling unlock pulsating task")
            self.unlock_pulsating_task.cancel()
