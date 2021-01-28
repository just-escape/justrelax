from gpiozero import OutputDevice

from twisted.internet.reactor import callLater

from justrelax.common.logging_utils import logger
from justrelax.node.service import JustSockClientService, EventCategoryToMethodMixin


class FogMachine(EventCategoryToMethodMixin, JustSockClientService):
    def __init__(self, *args, **kwargs):
        super(FogMachine, self).__init__(*args, **kwargs)

        self.fan = OutputDevice(self.node_params['fan_pin'])
        self.machine = OutputDevice(self.node_params['machine_pin'])

        if self.node_params['on_by_default']:
            self.event_on()
        else:
            self.event_off()

        self.send_fog_default_duration = self.node_params['send_fog_default_duration']
        self.send_fog_forever_default_frequency = self.node_params['send_fog_forever_default_frequency']
        self.fog_pin = OutputDevice(self.node_params['fog_pin'])
        self.fog_pin.off()

        self.send_fog_task = None
        self.send_fog_forever_task = None

    def event_on(self):
        logger.info("Heating machine and turning on fan")
        self.fan.on()
        self.machine.on()

    def event_off(self):
        logger.info("Stop heating machine and turning off fan")
        self.fan.off()
        self.machine.off()

    def _release_fog_pin(self):
        logger.info("Stop sending fog")
        self.fog_pin.off()

    def event_send_fog(self, duration: int = None):
        delay = duration if duration is not None else self.send_fog_default_duration

        if self.send_fog_task and self.send_fog_task.active():
            logger.info("Fog is already being sent: adding {} seconds to the timer".format(delay))
            self.send_fog_task.delay(delay)

        else:
            logger.info("Sending fog for {} seconds".format(delay))
            self.fog_pin.on()
            self.send_fog_task = callLater(delay, self._release_fog_pin)

    def event_send_fog_forever(self, frequency: int = None, send_duration: int = None):
        if self.send_fog_forever_task and self.send_fog_forever_task.active():
            logger.info("Already sending fog forever: stopping previous task")
            self.send_fog_forever_task.cancel()

        frequency = frequency if frequency is not None else self.send_fog_forever_default_frequency
        logger.info("Scheduling to send fog for {} second(s) every {} second(s)".format(send_duration, frequency))
        self.send_fog_forever_task = callLater(frequency, self.event_send_fog, send_duration)
        self.event_send_fog(send_duration)

    def event_stop_sending_fog_forever(self):
        if self.send_fog_forever_task and self.send_fog_forever_task.active():
            logger.info("Stop sending fog forever task")
            self.send_fog_forever_task.cancel()
        else:
            logger.info("Fog was not already being sent forever: skipping")
