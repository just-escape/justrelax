import time

import gpiozero
import neopixel
import board

from twisted.internet.reactor import callLater
from twisted.internet.task import LoopingCall

from justrelax.core.logging_utils import logger
from justrelax.core.node import MagicNode, on_event


class Controller:
    STATUSES = {"inactive", "playing"}

    def __init__(
            self, control_panel_service, led_indexes, electromagnet_pin, jack_pin, manual_mode_jack_port_pin,
            marmitron_mode_jack_port_pin, table_button_pin, table_up_pin, table_down_pin,
            table_up_down_pins_active_high, table_max_amplitude_duration, table_up_down_minimum_delay, colors,
            blinking_clue_delay,
    ):
        self.service = control_panel_service

        self._status = None

        self.led_strip = neopixel.NeoPixel(board.D18, 9)
        self.led_tasks = {}
        self.scene_led_indexes = led_indexes["scene"]
        self.manual_mode_led_index = led_indexes["manual_mode"]
        self.marmitron_mode_led_index = led_indexes["marmitron_mode"]
        self.lights_status_led_index = led_indexes["lights_status"]
        self.menu_status_led_index = led_indexes["menu_status"]
        self.table_led_index = led_indexes["table"]
        self.electromagnet_led_index = led_indexes["electromagnet"]

        self.electromagnet = gpiozero.OutputDevice(electromagnet_pin)

        self.table_button = gpiozero.Button(table_button_pin)
        # Never have the table_up_pin and table_down_pin active at the same time or electronics might crash
        self.table_motor_up = gpiozero.OutputDevice(table_up_pin, active_high=table_up_down_pins_active_high)
        self.table_motor_up.off()
        self.table_motor_down = gpiozero.OutputDevice(table_down_pin, active_high=table_up_down_pins_active_high)
        self.table_motor_down.off()
        self.table_max_amplitude_duration = table_max_amplitude_duration
        self.table_up_down_minimum_delay = table_up_down_minimum_delay
        self.table_stop_motor_task = None
        self.table_led_task = None
        self.table_watch_button_task = LoopingCall(self.check_table_button)
        self.has_table_been_down_once = False
        self.schedule_table_down_task = None
        self.table_blinking_clue_task = None
        self.blinking_clue_delay = blinking_clue_delay

        self.has_manual_mode_been_set_once = False
        self.jack = gpiozero.OutputDevice(jack_pin)
        self.jack.on()
        self.manual_mode_jack_port = gpiozero.InputDevice(manual_mode_jack_port_pin)
        self.marmitron_mode_jack_port = gpiozero.InputDevice(marmitron_mode_jack_port_pin)

        self.colors = colors

        self.check_jack_ports()

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

        if isinstance(predefined_color, list):
            if self.led_tasks.get(led_index, {}).get('last_blink_color', None) != color:
                # Start a new blink cycle only if the blink color (or blink pattern) is a new one

                blink_task = self.led_tasks.get(led_index, {}).get('task', None)
                if blink_task and blink_task.active():
                    blink_task.cancel()

                self.led_tasks[led_index] = {'last_blink_color': color}
                self._blink_led(led_index, color)
        else:
            blink_task = self.led_tasks.get(led_index, {}).get('task', None)
            if blink_task and blink_task.active():
                blink_task.cancel()

            if led_index in self.led_tasks:
                self.led_tasks.pop(led_index)

            r = predefined_color.get("r", 0)
            g = predefined_color.get("g", 0)
            b = predefined_color.get("b", 0)
            self.led_strip[led_index] = r, g, b

    def _blink_led(self, led_index, color, counter=0):
        current_color = self.colors[color][counter % len(self.colors[color])]

        self.led_tasks[led_index]['task'] = callLater(
            current_color['duration'],
            self._blink_led, led_index, color, counter+1)

        rgb = self.colors.get(current_color['color'], {})
        self.led_strip[led_index] = rgb.get('r', 0), rgb.get('g', 0), rgb.get('b', 0)

    def check_table_button(self):
        if self.table_button.is_active:
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
            # Dirty but easy guaranty that the motor won't be activated in both directions
            time.sleep(self.table_up_down_minimum_delay)

        logger.info("Setting the motor in up position")
        self.table_motor_up.on()

        logger.info("Turning off the led")
        self.set_led_color(self.table_led_index, "black")

        self._cancel_table_tasks()

        logger.info("Scheduling the motor to stop after {} seconds".format(self.table_max_amplitude_duration))
        self.table_stop_motor_task = callLater(self.table_max_amplitude_duration, self.table_stop)

    def table_down(self):
        self.has_table_been_down_once = True
        if self.schedule_table_down_task and self.schedule_table_down_task.active():
            self.schedule_table_down_task.cancel()

        if self.table_blinking_clue_task and self.table_blinking_clue_task.active():
            self.table_blinking_clue_task.cancel()

        logger.info("Pulling table down")
        if self.table_motor_up.is_active:
            logger.info("Motor was in up position. Turning off the up position and sleeping for {} seconds".format(
                self.table_up_down_minimum_delay))
            self.table_motor_up.off()
            # Dirty but easy guaranty that the motor won't be activated in both directions
            time.sleep(self.table_up_down_minimum_delay)

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

    def on_inactive(self):
        for blink_task in self.led_tasks.values():
            if blink_task['task'] and blink_task['task'].active():
                blink_task['task'].cancel()
        self.led_tasks = {}

        self.led_strip.fill((0, 0, 0))

        if self.table_watch_button_task.running:
            self.table_watch_button_task.stop()

        self.has_manual_mode_been_set_once = False
        self.has_table_been_down_once = False
        if self.schedule_table_down_task and self.schedule_table_down_task.active():
            self.schedule_table_down_task.cancel()
        if self.table_blinking_clue_task and self.table_blinking_clue_task.active():
            self.table_blinking_clue_task.cancel()

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

        self.table_blinking_clue_task = callLater(
            self.blinking_clue_delay, self.set_led_color, self.table_led_index, "table_clue_blink")

    def set_lights_service_status(self, repaired):
        self.set_led_color(self.lights_status_led_index, "green" if repaired else "red")
        if not self.has_table_been_down_once:
            self.schedule_table_down_task = callLater(15, self.table_down)

    def set_menu_service_status(self, repaired):
        self.set_led_color(self.menu_status_led_index, "green" if repaired else "red")

    def reset(self):
        # Force this value here, even if it is redundant with the on_inactive method. Because when we debug the room
        # it is possible to force the manual mode several times without changing the control panel status. If the
        # control panel status doesn't change, the on_inactive method will not be called.
        self.has_manual_mode_been_set_once = False
        self.has_table_been_down_once = False
        if self.schedule_table_down_task and self.schedule_table_down_task.active():
            self.schedule_table_down_task.cancel()
        self.status = "inactive"

    def check_jack_ports(self):
        callLater(0.1, self.check_jack_ports)

        if self.status != "playing":
            return

        if self.marmitron_mode_jack_port.is_active:
            if self.has_manual_mode_been_set_once:
                self.set_led_color(self.marmitron_mode_led_index, "red_blink")
            else:
                self.set_led_color(self.marmitron_mode_led_index, "green")
        else:
            self.set_led_color(self.marmitron_mode_led_index, "red")

        if self.manual_mode_jack_port.is_active:
            self.on_manual_mode()

            self.set_led_color(self.manual_mode_led_index, "green")
        else:
            if self.has_manual_mode_been_set_once:
                self.set_led_color(self.manual_mode_led_index, "green")
            else:
                self.set_led_color(self.manual_mode_led_index, "red")

    def on_manual_mode(self):
        if not self.has_manual_mode_been_set_once:
            self.has_manual_mode_been_set_once = True
            self.service.notify_first_manual_mode()


class ControlPanel(MagicNode):
    def __init__(self, *args, **kwargs):
        super(ControlPanel, self).__init__(*args, **kwargs)
        led_indexes = self.config["led_indexes"]
        electromagnet_pin = self.config["electromagnet_pin"]
        jack_pin = self.config["jack_pin"]
        manual_mode_jack_port_pin = self.config["manual_mode_jack_port_pin"]
        marmitron_mode_jack_port_pin = self.config["marmitron_mode_jack_port_pin"]
        table_button_pin = self.config["table"]["button_pin"]
        table_up_pin = self.config["table"]["up_pin"]
        table_down_pin = self.config["table"]["down_pin"]
        table_up_down_pins_active_high = self.config["table"]["up_down_pins_active_high"]
        table_max_amplitude_duration = self.config["table"]["max_amplitude_duration"]
        table_up_down_minimum_delay = self.config["table"]["up_down_minimum_delay"]
        colors = self.config["colors"]
        blinking_clue_delay = self.config["table"]["blinking_clue_delay"]

        self.controller = Controller(
            self, led_indexes, electromagnet_pin, jack_pin, manual_mode_jack_port_pin, marmitron_mode_jack_port_pin,
            table_button_pin, table_up_pin, table_down_pin, table_up_down_pins_active_high,
            table_max_amplitude_duration, table_up_down_minimum_delay, colors, blinking_clue_delay)

    def on_first_connection(self):
        self.controller.status = "inactive"

    @on_event(filter={'category': 'reset'})
    def event_reset(self):
        self.controller.reset()

    @on_event(filter={'category': 'set_status'})
    def event_set_status(self, status: str):
        self.controller.status = status

    @on_event(filter={'category': 'set_lights_service_status'})
    def event_set_lights_service_status(self, repaired: bool):
        self.controller.set_lights_service_status(repaired)

    @on_event(filter={'category': 'set_menu_service_status'})
    def event_set_menu_service_status(self, repaired: bool):
        self.controller.set_menu_service_status(repaired)

    @on_event(filter={'category': 'table_up'})
    def event_table_up(self):
        self.controller.table_up()

    @on_event(filter={'category': 'table_down'})
    def event_table_down(self):
        self.controller.table_down()

    @on_event(filter={'category': 'table_stop'})
    def event_table_stop(self):
        logger.info("Stopping the table")
        self.controller.table_stop()

    @on_event(filter={'category': 'force_manual_mode'})
    def event_force_manual_mode(self):
        self.controller.on_manual_mode()

    def notify_status(self, status):
        self.publish({"category": "set_status", "status": status})

    def notify_table_button_pressed(self):
        self.publish({"category": "table_button_pressed"})

    def notify_mode(self, mode):
        self.publish({"category": "set_mode", "mode": mode})

    def notify_first_manual_mode(self):
        self.publish({"category": "first_manual_mode"})
