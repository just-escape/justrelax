import gpiozero

from twisted.internet.reactor import callLater
from twisted.internet.task import LoopingCall

from justrelax.core.node import MagicNode, on_event
from justrelax.core.logging_utils import logger


class EmergencyExit(MagicNode):
    def __init__(self, *args, **kwargs):
        super(EmergencyExit, self).__init__(*args, **kwargs)

        button_pin = self.config["emergency_button_pin"]
        self.emergency_button_hold_time = self.config["emergency_button_hold_time"]
        self.emergency_button = gpiozero.Button(button_pin, hold_time=self.emergency_button_hold_time)
        self.is_emergency_button_held = False

        self.watch_emergency_button = LoopingCall(self.check_emergency_button)
        self.watch_emergency_button.start(0.01)

        self.emergency_magnets = self.config["emergency_magnets"]

        self.magnets = {}
        for magnet_id, magnet_pin in self.config["magnet_pins"].items():
            self.magnets[magnet_id] = gpiozero.OutputDevice(magnet_pin)

        self.lock_task = None
        self.relock_delay = self.config["relock_delay"]

        self.event_lock()

    def check_emergency_button(self):
        if self.emergency_button.is_held:
            if not self.is_emergency_button_held:
                logger.info(
                    "The emergency button has been held for {} second(s)".format(self.emergency_button_hold_time))
                self.event_unlock(relock=True)
        else:
            if self.is_emergency_button_held:
                logger.info("The emergency button has been released")

        self.is_emergency_button_held = self.emergency_button.is_held

    @on_event(filter={'category': 'unlock'})
    def event_unlock(self, magnet_id: str = None, relock: bool = False):
        if magnet_id is None:
            logger.info("Unlocking all emergency magnets ({})".format(", ".join(self.emergency_magnets)))
            for magnet in self.emergency_magnets:
                self.magnets[magnet].off()
        else:
            magnet = self.magnets.get(magnet_id, None)
            if magnet is None:
                logger.info("Magnet id={} not found: skipping".format(magnet_id))
                return
            logger.info("Unlocking magnet id={}".format(magnet_id))
            magnet.off()

        if relock:
            logger.info("Scheduling a lock in {} seconds".format(self.relock_delay))
            if self.lock_task and self.lock_task.active():
                self.lock_task.cancel()
            self.lock_task = callLater(self.relock_delay, self.event_lock, magnet_id)

    @on_event(filter={'category': 'lock'})
    def event_lock(self, magnet_id: str = None):
        if magnet_id is None:
            logger.info("Locking all magnets ({})".format(", ".join(self.magnets.keys())))
            for magnet in self.magnets.values():
                magnet.on()

        else:
            magnet = self.magnets.get(magnet_id, None)
            if magnet is None:
                logger.info("Magnet id={} not found: skipping".format(magnet_id))
                return
            logger.info("Locking magnet id={}".format(magnet_id))
            magnet.on()

    @on_event(filter={'category': 'reset'})
    def event_reset(self):
        logger.info("Resetting")
        self.event_lock()
