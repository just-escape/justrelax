import gpiozero
import neopixel
import board
import time

from twisted.internet.reactor import callLater
from twisted.internet.task import LoopingCall

from justrelax.common.logging_utils import logger
from justrelax.node.service import JustSockClientService, EventCategoryToMethodMixin


class Controller:
    STATUSES = {"inactive", "playing"}

    def __init__(
            self, control_panel_service, led_indexes, electromagnet_pin, jack_pin, manual_mode_jack_port_pin,
            marmitron_mode_jack_port_pin, table_button_pin, table_up_pin, table_down_pin, table_max_amplitude_duration,
            table_up_down_minimum_delay, colors,
    ):
        self.service = control_panel_service

        self._status = None

        self.led_strip = neopixel.NeoPixel(board.D18, 9)
        self.led_tasks = {}
        self.scene_led_indexes = led_indexes["scene"]
        self.manual_mode_led_index = led_indexes["manual_mode"]
        self.lights_status_led_index = led_indexes["lights_status"]
        self.menu_status_led_index = led_indexes["menu_status"]
        self.table_led_index = led_indexes["table"]
        self.electromagnet_led_index = led_indexes["electromagnet"]

        self.electromagnet = gpiozero.OutputDevice(electromagnet_pin)

        self.table_button = gpiozero.Button(table_button_pin)
        # Never have the table_up_pin and table_down_pin active at the same time or electronics might crash
        self.table_motor_up = gpiozero.OutputDevice(table_up_pin)
        self.table_motor_up.off()
        self.table_motor_down = gpiozero.OutputDevice(table_down_pin)
        self.table_motor_down.off()
        self.table_max_amplitude_duration = table_max_amplitude_duration
        self.table_up_down_minimum_delay = table_up_down_minimum_delay
        self.table_stop_motor_task = None
        self.table_led_task = None
        self.table_watch_button_task = LoopingCall(self.check_table_button)

        self.has_manual_mode_been_set_once = False
        self.jack = gpiozero.OutputDevice(jack_pin)
        self.jack.on()
        self.manual_mode_jack_port = gpiozero.InputDevice(manual_mode_jack_port_pin)
        self.marmitron_mode_jack_port = gpiozero.InputDevice(marmitron_mode_jack_port_pin)

        self.colors = colors

        self.status = "inactive"

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if value not in self.STATUSES:
            logger.warning("Status not in {}: skipping".format(value, ", ".join(self.STATUSES)))
            return

        if value == self.status:
            logger.debug("Status is already {}: skipping".format(value))
            return

        logger.debug("Setting status to {}".format(value))
        self._status = value

        if self._status == "inactive":
            self.on_inactive()
        elif self._status == "playing":
            self.on_playing()

        self.service.notify_status(self.status)

    def set_led_color(self, led_index, color):
        predefined_color = self.colors.get(color, {})

        blink_task = self.led_tasks.get(led_index, None)
        if blink_task and blink_task.active():
            blink_task.cancel()

        if isinstance(predefined_color, list):
            self._blink_led(led_index, color)
        else:
            r = predefined_color.get("r", 0)
            g = predefined_color.get("g", 0)
            b = predefined_color.get("b", 0)
            self.led_strip[led_index] = r, g, b

    def _blink_led(self, led_index, color, counter=0):
        current_color = color[counter % len(color)]
        self.led_tasks[led_index] = callLater(
            current_color['duration'],
            self._blink_led, led_index, color, counter=counter+1)
        rgb = self.colors.get(current_color['color'], {})
        self.led_strip[led_index] = rgb['r'], rgb['g'], rgb['b']

    def check_table_button(self):
        if self.table_button.is_active and self.is_table_position_up():
            logger.info("Table button has been pressed")
            self.table_down()
            self.service.notify_table_button_pressed()

    def _cancel_table_tasks(self):
        logger.debug("Cancelling table tasks")
        if self.table_led_task and self.table_led_task.active():
            logger.info("Cancelling table led task")
            self.table_led_task.cancel()

        if self.table_stop_motor_task and self.table_stop_motor_task.active():
            logger.info("Cancelling table stop motor task")
            self.table_stop_motor_task.cancel()

    def table_up(self):
        logger.info("Pulling table up")
        if self.table_motor_down.is_active:
            logger.info("Motor was in down position. Turning off the down position and sleeping for {} seconds".format(
                self.table_up_down_minimum_delay))
            self.table_motor_down.off()
            time.sleep(self.table_up_down_minimum_delay)  # Dirty

        logger.info("Setting the motor in up position")
        self.table_motor_up.on()

        logger.info("Turning off the led")
        self.set_led_color(self.table_led_index, "black")

        self._cancel_table_tasks()

        logger.info("Scheduling the motor to stop after {} seconds".format(self.table_max_amplitude_duration))
        self.table_stop_motor_task = callLater(self.table_max_amplitude_duration, self.table_stop)

    def table_down(self):
        logger.info("Pulling table down")
        if self.table_motor_up.is_active:
            logger.info("Motor was in up position. Turning off the up position and sleeping for {} seconds".format(
                self.table_up_down_minimum_delay))
            self.table_motor_down.off()
            time.sleep(self.table_up_down_minimum_delay)  # Dirty

        logger.info("Setting the motor in down position")
        self.table_motor_down.on()

        logger.info("Blinking the table led green")
        self.set_led_color(self.table_led_index, "green_blink")

        self._cancel_table_tasks()

        logger.info("Scheduling the led to turn on after {} seconds".format(self.table_max_amplitude_duration))
        self.table_led_task = callLater(
            self.table_max_amplitude_duration, self.set_led_color, self.table_led_index, "green")
        logger.info("Scheduling the motor to stop after {} seconds".format(self.table_max_amplitude_duration))
        self.table_stop_motor_task = callLater(self.table_max_amplitude_duration, self.table_stop)
        if self.table_watch_button_task.running:
            logger.info("Stop watching the table button")
            self.table_watch_button_task.stop()

    def table_stop(self):
        logger.info("Stopping the motor")
        self.table_motor_up.off()
        self.table_motor_down.off()

    def is_table_position_down(self):
        return self.table_motor_down.is_active

    def is_table_position_up(self):
        return self.table_motor_up.is_active

    def on_inactive(self):
        self.led_strip.fill((0, 0, 0))

        self.table_up()
        self._cancel_table_tasks()
        logger.info("Scheduling the motor to stop after {} seconds".format(self.table_max_amplitude_duration))
        self.table_stop_motor_task = callLater(self.table_max_amplitude_duration, self.table_stop)

        if self.table_watch_button_task.running:
            self.table_watch_button_task.stop()

        self.has_manual_mode_been_set_once = False

        self.electromagnet.on()
        self.set_led_color(self.electromagnet_led_index, "red")

        # Do not switch on panel leds while the panel is inactive to avoid light from leaking
        # through the panel edges

    def on_playing(self):
        self.led_strip.fill((0, 0, 0))

        self.table_watch_button_task.start(0.01)

        self.electromagnet.off()
        self.set_led_color(self.electromagnet_led_index, "green")

        for led_index in self.scene_led_indexes:
            self.set_led_color(led_index, "white")

        self.set_led_color(self.lights_status_led_index, "red")
        self.set_led_color(self.menu_status_led_index, "red")
        self.set_led_color(self.table_led_index, "table")

    def set_lights_service_status(self, repaired):
        self.set_led_color(self.lights_status_led_index, "green" if repaired else "red")

    def set_menu_service_status(self, repaired):
        self.set_led_color(self.menu_status_led_index, "green" if repaired else "red")

    def reset(self):
        self.status = "inactive"

    def check_jack_ports(self):
        if self.status != "playing":
            return

        if self.marmitron_mode_jack_port.is_active:
            if self.has_manual_mode_been_set_once:
                self.set_led_color(self.marmitron_mode_jack_port, "red_blink")
            else:
                self.set_led_color(self.marmitron_mode_jack_port, "green")
        else:
            self.set_led_color(self.marmitron_mode_jack_port, "red")

        if self.manual_mode_jack_port.is_active:
            if not self.has_manual_mode_been_set_once:
                self.has_manual_mode_been_set_once = True
                self.service.notify_first_manual_mode()

            self.set_led_color(self.manual_mode_led_index, "green")
        else:
            if self.has_manual_mode_been_set_once:
                self.set_led_color(self.manual_mode_led_index, "green")
            else:
                self.set_led_color(self.manual_mode_led_index, "red")


class ControlPanel(EventCategoryToMethodMixin, JustSockClientService):
    def __init__(self, *args, **kwargs):
        super(ControlPanel, self).__init__(*args, **kwargs)
        led_indexes = self.node_params["led_indexes"]
        electromagnet_pin = self.node_params["electromagnet_pin"]
        jack_pin = self.node_params["jack_pin"]
        manual_mode_jack_port_pin = self.node_params["manual_mode_jack_port"]
        marmitron_mode_jack_port_pin = self.node_params["marmitron_mode_jack_port"]
        table_button_pin = self.node_params["table"]["button_pin"]
        table_up_pin = self.node_params["table"]["up_pin"]
        table_down_pin = self.node_params["table"]["down_pin"]
        table_max_amplitude_duration = self.node_params["table"]["table_max_amplitude_duration"]
        table_up_down_minimum_delay = self.node_params["table"]["table_up_down_minimum_delay"]
        colors = self.node_params["colors"]

        self.controller = Controller(
            self, led_indexes, electromagnet_pin, jack_pin, manual_mode_jack_port_pin, marmitron_mode_jack_port_pin,
            table_button_pin, table_up_pin, table_down_pin, table_max_amplitude_duration, table_up_down_minimum_delay,
            colors)

    def event_reset(self):
        self.controller.reset()

    def event_set_status(self, status: str):
        self.controller.status = status

    def event_set_lights_service_status(self, repaired: bool):
        self.controller.set_lights_service_status(repaired)

    def event_set_menu_service_status(self, repaired: bool):
        self.controller.set_menu_service_status(repaired)

    def event_table_up(self):
        self.controller.table_up()

    def event_table_down(self):
        self.controller.table_down()

    def event_table_stop(self):
        logger.info("Stopping the table")
        self.controller.table_stop()

    def notify_status(self, status):
        self.send_event({"category": "set_status", "status": status})

    def notify_table_button_pressed(self):
        self.send_event({"category": "table_button_pressed"})

    def notify_mode(self, mode):
        self.send_event({"category": "set_mode", "mode": mode})

    def notify_first_manual_mode(self):
        self.send_event({"category": "first_manual_mode"})
