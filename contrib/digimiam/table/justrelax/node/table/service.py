import time
from gpiozero import OutputDevice, InputDevice

from twisted.internet.reactor import callLater
from twisted.internet.task import LoopingCall

from justrelax.common.logging_utils import logger
from justrelax.node.service import JustSockClientService, EventCategoryToMethodMixin


class Motor:
    def __init__(self, up_pin, down_pin):
        # Never have those the two pins active at the same time or the electronics might crash
        self.motor_up = OutputDevice(up_pin, active_high=False)
        self.motor_up.off()
        self.motor_down = OutputDevice(down_pin, active_high=False)
        self.motor_down.off()

    def position_up(self):
        self.motor_down.off()
        time.sleep(0.1)
        self.motor_up.on()

    def position_down(self):
        self.motor_up.off()
        time.sleep(0.1)
        self.motor_down.on()

    def is_position_down(self):
        return self.motor_down.is_active

    def is_position_up(self):
        return self.motor_up.is_active


class Table(EventCategoryToMethodMixin, JustSockClientService):
    def __init__(self, *args, **kwargs):
        super(Table, self).__init__(*args, **kwargs)
        self.switch = InputDevice(self.node_params["switch_pin"])
        self.motor = Motor(self.node_params["motor_up_pin"], self.node_params["motor_down_pin"])
        self.led = OutputDevice(self.node_params["led_pin"])
        self.led_delay = self.node_params["led_delay"]
        self.led_task = None
        self.check_switch_task = LoopingCall(self.check_switch)
        self.check_switch_task.start(1 / 25)

    def check_switch(self):
        if self.switch.is_active:
            if not self.motor.is_position_up:
                logger.info("Switch is active and motor is in position up")
                self.event_down()
                self.check_switch_task.stop()

    def cancel_led_task(self):
        if self.led_task and self.led_task.active():
            self.led_task.cancel()

    def event_reset(self):
        logger.info("Resetting: setting the motor in up position, turning off the led and listening to the switch.")
        self.motor.position_up()
        self.led.off()
        self.cancel_led_task()
        if not self.check_switch_task.running:
            self.check_switch_task.start(1 / 25)

    def event_up(self):
        logger.info(
            "Pulling table up: setting the motor in up position and turning off the led. Don't listen to the switch.")
        self.motor.position_up()
        self.led.off()
        self.cancel_led_task()

    def event_down(self):
        logger.info(
            "Pulling table down: setting the motor in down position, scheduling to turn on the led and stop listening "
            "to the switch.")
        self.motor.position_down()
        self.cancel_led_task()
        self.led_task = callLater(self.led_delay, self.led.on)
        self.check_switch_task.stop()
