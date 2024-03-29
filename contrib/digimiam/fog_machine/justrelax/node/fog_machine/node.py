from gpiozero import OutputDevice

from twisted.internet.reactor import callLater

from justrelax.core.logging_utils import logger
from justrelax.core.node import MagicNode, on_event


class FogMachine(MagicNode):
    def __init__(self, *args, **kwargs):
        super(FogMachine, self).__init__(*args, **kwargs)

        self.machine = OutputDevice(self.config['machine_pin'])

        if self.config['on_by_default']:
            self.event_on()
        else:
            self.event_off()

        self.send_fog_default_duration = self.config['send_fog_default_duration']
        self.send_fog_forever_default_frequency = self.config['send_fog_forever_default_frequency']
        self.fog_pin = OutputDevice(self.config['fog_pin'])
        self.fog_pin.off()

        self.send_fog_task = None
        self.send_fog_forever_task = None

    @on_event(filter={'category': 'on'})
    def event_on(self):
        logger.info("Heating machine")
        self.machine.on()

    @on_event(filter={'category': 'off'})
    def event_off(self):
        logger.info("Stop heating machine")
        self.machine.off()

    def _release_fog_pin(self):
        logger.info("Stop sending fog")
        self.fog_pin.off()

    @on_event(filter={'category': 'send_fog'})
    def event_send_fog(self, duration: int = None, forever: bool = False, forever_frequency: int = 15):
        delay = duration if duration is not None else self.send_fog_default_duration

        if forever:
            if not self.send_fog_forever_task or not self.send_fog_forever_task.active():
                self.send_fog_forever_task = callLater(forever_frequency, self.event_send_fog, duration, True)

        if self.send_fog_task and self.send_fog_task.active():
            logger.info("Fog is already being sent: adding {} seconds to the timer".format(delay))
            self.send_fog_task.delay(delay)

        else:
            logger.info("Sending fog for {} seconds".format(delay))
            self.fog_pin.on()
            self.send_fog_task = callLater(delay, self._release_fog_pin)

    @on_event(filter={'category': 'send_fog_forever'})
    def event_send_fog_forever(self, frequency: int = None, send_duration: int = None):
        if self.send_fog_forever_task and self.send_fog_forever_task.active():
            logger.info("Already sending fog forever: stopping previous task")
            self.send_fog_forever_task.cancel()

        frequency = frequency if frequency is not None else self.send_fog_forever_default_frequency
        duration = send_duration if send_duration is not None else self.send_fog_default_duration
        logger.info("Scheduling to send fog for {} second(s) every {} second(s)".format(duration, frequency))
        self.send_fog_forever_task = callLater(frequency, self.event_send_fog, duration, True)
        self.event_send_fog(duration)

    @on_event(filter={'category': 'stop_sending_fog_forever'})
    def event_stop_sending_fog_forever(self):
        if self.send_fog_forever_task and self.send_fog_forever_task.active():
            logger.info("Stop sending fog forever task")
            self.send_fog_forever_task.cancel()
        else:
            logger.info("Fog was not already being sent forever: skipping")

    @on_event(filter={'category': 'reset'})
    def event_reset(self):
        logger.info("Resetting")
        if self.send_fog_task and self.send_fog_task.active():
            self.send_fog_task.cancel()

        if self.send_fog_forever_task and self.send_fog_forever_task.active():
            self.send_fog_forever_task.cancel()

        self._release_fog_pin()
        self.event_off()
