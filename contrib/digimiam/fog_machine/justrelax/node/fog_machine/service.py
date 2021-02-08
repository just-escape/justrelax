from gpiozero import OutputDevice

from twisted.internet.reactor import callLater

from justrelax.common.logging_utils import logger
from justrelax.node.service import PublishSubscribeClientService, on_event


class FogMachine(PublishSubscribeClientService):
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

    @on_event(filter={'category': 'on'})
    def event_on(self):
        logger.info("Heating machine and turning on fan")
        self.fan.on()
        self.machine.on()

    @on_event(filter={'category': 'off'})
    def event_off(self):
        logger.info("Stop heating machine and turning off fan")
        self.fan.off()
        self.machine.off()

    def _release_fog_pin(self):
        logger.info("Stop sending fog")
        self.fog_pin.off()

    @on_event(filter={'category': 'send_fog'})
    def event_send_fog(self, duration: int = None):
        delay = duration if duration is not None else self.send_fog_default_duration

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
        self.send_fog_forever_task = callLater(frequency, self.event_send_fog, duration)
        self.event_send_fog(duration)

    @on_event(filter={'category': 'stop_sending_fog_forever'})
    def event_stop_sending_fog_forever(self):
        if self.send_fog_forever_task and self.send_fog_forever_task.active():
            logger.info("Stop sending fog forever task")
            self.send_fog_forever_task.cancel()
        else:
            logger.info("Fog was not already being sent forever: skipping")
