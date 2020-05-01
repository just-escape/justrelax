import time
from gpiozero import OutputDevice, InputDevice

from twisted.internet.reactor import callLater
from twisted.internet.task import LoopingCall

from justrelax.common.logging_utils import logger
from justrelax.node.service import JustSockClientService, EventCategoryToMethodMixin


class Motor:
    def __init__(self, up_pin, down_pin, up_down_minimum_delay):
        # Never have those the two pins active at the same time or the electronics might crash
        self.motor_up = OutputDevice(up_pin, active_high=False)
        self.motor_up.off()
        self.motor_down = OutputDevice(down_pin, active_high=False)
        self.motor_down.off()
        self.up_down_minimum_delay = up_down_minimum_delay

    def position_up(self):
        if self.motor_up.is_active:
            logger.info("Motor was in down position. Turning off the down position and sleeping for {} seconds".format(
                self.up_down_minimum_delay))
            self.motor_down.off()
            time.sleep(self.up_down_minimum_delay)

        logger.info("Setting the motor in up position")
        self.motor_up.on()

    def position_down(self):
        if self.motor_up.is_active:
            logger.info("Motor was in up position. Turning off the up position and sleeping for {} seconds".format(
                self.up_down_minimum_delay))
            self.motor_up.off()
            time.sleep(self.up_down_minimum_delay)

        logger.info("Setting the motor in down position")
        self.motor_down.on()

    def stop(self):
        logger.info("Stopping the motor")
        self.motor_up.off()
        self.motor_down.off()

    def is_position_down(self):
        return self.motor_down.is_active

    def is_position_up(self):
        return self.motor_up.is_active


class Table(EventCategoryToMethodMixin, JustSockClientService):
    def __init__(self, *args, **kwargs):
        super(Table, self).__init__(*args, **kwargs)
        self.switch = InputDevice(self.node_params["switch_pin"])
        self.motor = Motor(
            self.node_params["motor_up_pin"],
            self.node_params["motor_down_pin"],
            self.node_params["up_down_minimum_delay"])
        self.led = OutputDevice(self.node_params["led_pin"])
        self.pull_delay = self.node_params["pull_delay"]
        self.led_task = None
        self.stop_motor_task = None
        self.check_switch_task = LoopingCall(self.check_switch)
        self.check_switch_task.start(1 / 25)

    def check_switch(self):
        if self.switch.is_active:
            if not self.motor.is_position_up:
                logger.info("Switch is active and motor is in position up")
                self.event_down()
                self.check_switch_task.stop()

    def cancel_tasks(self):
        logger.debug("Cancelling tasks")
        if self.led_task and self.led_task.active():
            logger.info("Cancelling led task")
            self.led_task.cancel()

        if self.stop_motor_task and self.stop_motor_task.active():
            logger.info("Cancelling stop motor task")
            self.stop_motor_task.cancel()

    def event_reset(self):
        logger.info("Resetting")
        self.motor.position_up()
        logger.info("Turning off the led")
        self.led.off()
        self.cancel_tasks()
        logger.info("Scheduling the motor to stop after {} seconds".format(self.pull_delay))
        self.stop_motor_task = callLater(self.pull_delay, self.motor.stop)
        logger.info("Starting to listen to the switch")
        if not self.check_switch_task.running:
            self.check_switch_task.start(1 / 25)

    def event_up(self):
        logger.info("Pulling table up")
        self.motor.position_up()
        logger.info("Turning off the led")
        self.led.off()
        self.cancel_tasks()
        logger.info("Scheduling the motor to stop after {} seconds".format(self.pull_delay))
        self.stop_motor_task = callLater(self.pull_delay, self.motor.stop)

    def event_down(self):
        logger.info("Pulling table down")
        self.motor.position_down()
        self.cancel_led_task()
        logger.info("Scheduling the led to turn on after {} seconds".format(self.pull_delay))
        self.led_task = callLater(self.pull_delay, self.led.on)
        logger.info("Scheduling the motor to stop after {} seconds".format(self.pull_delay))
        self.stop_motor_task = callLater(self.pull_delay, self.motor.stop)
        logger.info("Stop listening to the switch")
        self.check_switch_task.stop()

    def event_stop(self):
        logger.info("Stopping the table")
        self.motor.stop()
