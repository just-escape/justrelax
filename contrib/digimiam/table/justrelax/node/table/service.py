from gpiozero import OutputDevice, InputDevice

from twisted.internet.reactor import callLater
from twisted.internet.task import LoopingCall

from justrelax.common.logging_utils import logger
from justrelax.node.service import JustSockClientService, EventCategoryToMethodMixin


class Table(EventCategoryToMethodMixin, JustSockClientService):
    def __init__(self, *args, **kwargs):
        super(Table, self).__init__(*args, **kwargs)
        self.switch = InputDevice(self.node_params["switch_pin"])
        self.motor = OutputDevice(self.node_params["motor_pin"])
        self.led = OutputDevice(self.node_params["led_pin"])
        self.led_delay = self.node_params["led_delay"]
        self.led_task = None
        self.check_switch_task = LoopingCall(self.check_switch)
        self.check_switch_task.start(1 / 25)

    def check_switch(self):
        if self.switch.is_active:
            if not self.motor.is_active:
                logger.info("Switch is active and motor is not active")
                self.process_down()
                self.check_switch_task.stop()

    def cancel_led_task(self):
        if self.led_task and self.led_task.active():
            self.led_task.cancel()

    def process_reset(self):
        logger.info("Resetting node: turning on motor, turning off led and listening to the switch.")
        self.motor.on()
        self.led.off()
        self.cancel_led_task()
        self.check_switch_task.start(1 / 25)

    def process_up(self):
        logger.info("Pulling table up: turning on motor and turning off led. The switch will not be listened.")
        self.motor.on()
        self.led.off()
        self.cancel_led_task()

    def process_down(self):
        logger.info(
            "Pulling table down: turning off motor, scheduling to turn on the led and stop listening to the switch.")
        self.motor.off()
        self.cancel_led_task()
        self.led_task = callLater(self.led_delay, self.led.on)
        self.check_switch_task.stop()
