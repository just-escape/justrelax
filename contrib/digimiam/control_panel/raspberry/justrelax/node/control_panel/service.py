import random

from twisted.internet import reactor

from justrelax.node.service import JustSockClientService
from justrelax.node.helper import Serial

from justrelax.common.logging_utils import logger


class NiryoController:
    STATUSES = {"chaos", "mute", "playing", "success"}

    def __init__(self, control_panel_service, chrono_leds, status_leds, initial_difficulty, difficulties):
        self.service = control_panel_service
        self.chrono_leds = chrono_leds
        self.status_leds = status_leds

        self.tasks = {}

        self.difficulties = difficulties
        self._difficulty = list(self.difficulties)[0]  # By default. Not reliable.
        self.difficulty = initial_difficulty

        self.current_chrono_led = 0
        self.success_sequence = [None, None, None, None, None]
        self.generate_success_sequence()

        self.floppy_readers = [None, None, None, None, None]

        self.status = "chaos"

    @property
    def difficulty(self):
        return self._difficulty

    @difficulty.setter
    def difficulty(self, value):
        if value not in self.difficulties:
            logger.warning("Difficulty {} not in {}: skipping".format(value, ", ".join(self.difficulties)))
        else:
            logger.debug("Setting difficulty to {}".format(value))
            self.difficulty = value

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if value not in self.STATUSES:
            logger.warning("Status {} not in {}: skipping".format(value, ", ".join(self.STATUSES)))
            return

        if value == self.status:
            logger.debug("Status is already {}: skipping".format(value))
            return

        logger.debug("Setting status to {}".format(value))
        self._status = value

        for task_name, task in self.tasks.items():
            if task.active():
                task.cancel()
        self.tasks = {}

        if self._status == "chaos":
            self.on_chaos()
        elif self._status == "mute":
            self.on_mute()
        elif self._status == "playing":
            self.on_playing()
        elif self._status == "success":
            self.on_success()

    def generate_success_sequence(self):
        new_sequence = []
        available_floppies = self.difficulties[self.difficulty]["available_floppies"]
        if 6 > len(available_floppies):
            # The algorithm below might end up in a deadlock
            logger.error("Please submit at least 6 available floppies: skipping sequence generation")
            return

        for i in range(5):
            floppy = random.choice(available_floppies)
            if self.success_sequence[i] != floppy and floppy not in new_sequence:
                new_sequence.append(floppy)

        self.success_sequence = new_sequence

    def on_chaos(self):
        for led_index in range(self.chrono_leds["strip_length"]):
            self.set_chrono_led_random_colors(led_index)

        for led_index in range(self.status_leds["strip_length"]):
            self.set_status_led_random_colors(led_index)

    def set_chrono_led_random_colors(self, led_index):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        self.set_chrono_led_color(led_index, r, g, b, commit=True)

        delay = min(random.normalvariate(25, 5), 0.4)
        self.tasks["chrono-{}".format(led_index)] = reactor.callLater(
            delay, self.set_chrono_led_random_colors, led_index)

    def set_status_led_random_colors(self, led_index):
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        self.set_chrono_led_color(led_index, r, g, b, commit=True)

        delay = min(random.normalvariate(25, 5), 0.4)
        self.tasks["chrono-{}".format(led_index)] = reactor.callLater(
            delay, self.set_status_led_random_colors, led_index)

    def on_mute(self):
        # Reset LEDs
        for led_index in range(self.chrono_leds["strip_length"]):
            self.set_chrono_led_color(led_index, 0, 0, 0)

        self.set_status_led_color(0, 255, 0, 0)
        self.set_status_led_color(1, 255, 0, 0)
        self.set_status_led_color(2, 255, 0, 0, commit=True)

    def on_playing(self):
        self.current_chrono_led = 0
        self.set_status_led_color(0, 0, 255, 0)
        self.set_status_led_color(1, 0, 0, 255, commit=True)

    def on_success(self):
        self.tasks["success_animation"] = reactor.callLater(
            1, self.success_animation_step_1)

    def success_animation_step_1(self):
        # Turn all white chrono leds to green
        for led_index in range(self.current_chrono_led):
            self.set_chrono_led_color(led_index, 0, 255, 0)

        if self.current_chrono_led > 0:
            self.set_chrono_led_color(0, 0, 255, 0, commit=True)

        self.tasks["success_animation"] = reactor.callLater(
            0.3, self.success_animation_step_2)

    def success_animation_step_2(self):
        # Set next chrono led to green
        self.set_chrono_led_color(self.current_chrono_led, 0, 255, 0, commit=True)

        if self.current_chrono_led < self.chrono_leds["strip_length"]:
            self.current_chrono_led += 1
            self.tasks["success_animation"] = reactor.callLater(
                0.3, self.success_animation_step_2)
        else:
            self.tasks["success_animation"] = reactor.callLater(
                2, self.success_animation_step_3)

    def success_animation_step_3(self):
        self.set_status_led_color(1, 0, 255, 0)
        self.tasks["success_animation"] = reactor.callLater(
            3, self.success_animation_step_4)

    def success_animation_step_4(self):
        self.set_status_led_color(2, 0, 255, 0, commit=True)

        self.service.process_success()

    def insert_floppy(self, reader_index, tag):
        if self.status != "playing":
            return

        self.floppy_readers[reader_index] = tag

        animation_task = self.tasks.get("animation", None)
        if animation_task and animation_task.active():
            return

        # Chrono has not started <=> game is not started
        if self.current_chrono_led == 0:
            # If the game is not started, it cannot be right to insert a floppy in an other reader
            if reader_index != 0:
                self.show_error_and_restart_game(reader_index)
            elif self.floppy_readers[0] != self.success_sequence[0]:
                self.show_error_and_restart_game(0)
            else:
                # The first floppy is the good one
                for reader_index, tag in enumerate(self.floppy_readers[1:]):
                    # Make sure that all other readers are empty
                    if tag is not None:
                        # +1 because the enumerate starts at the index 1
                        self.show_error_and_restart_game(reader_index + 1)
                        return
                """Good insert"""
                self.tic_tac()

        # The game has started
        else:
            expected_reader_index = 4 - self.floppy_readers.count(None)
            if reader_index != expected_reader_index:
                # We don't need to check the content of the insert, a reader must have been skipped
                self.show_error_and_restart_game(reader_index)
                return

            if self.floppy_readers[reader_index] != self.success_sequence[reader_index]:
                self.show_error_and_restart_game(reader_index)
            else:
                """Good insert"""

    def eject_floppy(self, reader_index):
        if self.status != "playing":
            return

        self.floppy_readers[reader_index] = None

        animation_task = self.tasks.get("animation", None)
        if animation_task and animation_task.active():
            return

        if self.current_chrono_led != 0:
            self.show_error_and_restart_game(reader_index)

    def tic_tac(self):
        if self.current_chrono_led >= self.chrono_leds["strip_length"]:
            self.set_chrono_led_color(self.current_chrono_led, 255, 255, 255)
            self.current_chrono_led += 1
            delay = self.difficulties[self.difficulty]["chrono_led_frequency"]
            self.tasks["chrono"] = reactor.callLater(delay, self.tic_tac)
        else:
            self.tasks["animation"] = reactor.callLater(0.1, self.time_elapsed_animation_step_1)

    def time_elapsed_animation_step_1(self):
        for led_index in range(self.chrono_leds["strip_length"]):
            self.set_chrono_led_color(led_index, 255, 0, 0)
        self.tasks["animation"] = reactor.callLater(1, self.time_elapsed_animation_step_2)

    def time_elapsed_animation_step_2(self):
        for led_index in range(self.chrono_leds["strip_length"]):
            self.set_chrono_led_color(led_index, 0, 0, 0)
        self.tasks["animation"] = reactor.callLater(1, self.time_elapsed_animation_step_3)

    def time_elapsed_animation_step_3(self):
        for led_index in range(self.chrono_leds["strip_length"]):
            self.set_chrono_led_color(led_index, 255, 0, 0)
        self.tasks["animation"] = reactor.callLater(1, self.time_elapsed_animation_step_4)

    def time_elapsed_animation_step_4(self):
        for led_index in range(self.chrono_leds["strip_length"]):
            self.set_chrono_led_color(led_index, 0, 0, 0)

        self.restart_game()

    def show_error_and_restart_game(self, reader_index):
        chrono_task = self.tasks.get("chrono", None)
        if chrono_task and chrono_task.active():
            chrono_task.cancel()

        self.tasks["animation"] = reactor.callLater(0.1, self.error_animation_step_1, reader_index)

    def error_animation_step_1(self, reader_index):
        self.set_chrono_led_color(reader_index * 5 + 0, 255, 0, 0)
        self.set_chrono_led_color(reader_index * 5 + 1, 255, 0, 0)
        self.set_chrono_led_color(reader_index * 5 + 2, 255, 0, 0, commit=True)
        self.tasks["animation"] = reactor.callLater(1, self.error_animation_step_2, reader_index)

    def error_animation_step_2(self, reader_index):
        self.set_chrono_led_color(reader_index * 5 + 0, 0, 0, 0)
        self.set_chrono_led_color(reader_index * 5 + 1, 0, 0, 0)
        self.set_chrono_led_color(reader_index * 5 + 2, 0, 0, 0, commit=True)
        self.tasks["animation"] = reactor.callLater(1, self.error_animation_step_3, reader_index)

    def error_animation_step_3(self, reader_index):
        self.set_chrono_led_color(reader_index * 5 + 0, 255, 0, 0)
        self.set_chrono_led_color(reader_index * 5 + 1, 255, 0, 0)
        self.set_chrono_led_color(reader_index * 5 + 2, 255, 0, 0, commit=True)
        self.tasks["animation"] = reactor.callLater(1, self.error_animation_step_4, reader_index)

    def error_animation_step_4(self, reader_index):
        self.set_chrono_led_color(reader_index * 5 + 0, 0, 0, 0)
        self.set_chrono_led_color(reader_index * 5 + 1, 0, 0, 0)
        self.set_chrono_led_color(reader_index * 5 + 2, 0, 0, 0, commit=True)

        self.restart_game()

    def restart_game(self):
        self.current_chrono_led = 0
        self.generate_success_sequence()

    def reset(self):
        self.status = "chaos"

    def set_status_led_color(self, led_index, r, g, b, commit=False):
        if self.status_leds["reverse_pins"]:
            computed_led_index = self.status_leds["strip_length"] - led_index
        else:
            computed_led_index = led_index

        self.service.set_led_color(self.status_leds["strip"], computed_led_index, r, g, b, commit=commit)

    def set_chrono_led_color(self, led_index, r, g, b, commit=False):
        if self.chrono_leds["reverse_pins"]:
            computed_led_index = self.chrono_leds["strip_length"] - led_index
        else:
            computed_led_index = led_index

        self.service.set_led_color(self.chrono_leds["strip"], computed_led_index, r, g, b, commit=commit)


class ControlPanel(JustSockClientService):
    class ARDUINO_PROTOCOL:
        EVENT_TYPE = "event_type"

        RFID_READ = "rfid_read"
        READER = "reader"
        TAG = "value"

    class PROTOCOL:
        EVENT_TYPE = "event_type"

        RESET = "reset"

        SET_STATUS = "set_status"
        STATUS = "status"

        SET_DIFFICULTY = "set_difficulty"
        DIFFICULTY = "difficulty"

    def __init__(self, *args, **kwargs):
        super(ControlPanel, self).__init__(*args, **kwargs)

        self.floppies = self.node_params["floppies"]

        chrono_leds = self.node_params["chrono_leds"]
        status_leds = self.node_params["status_leds"]
        initial_difficulty = self.node_params["initial_difficulty"]
        difficulties = self.node_params["difficulties"]
        self.niryo_controller = NiryoController(self, chrono_leds, status_leds, initial_difficulty, difficulties)

        port = self.node_params['arduino']['port']
        baud_rate = self.node_params['arduino']['baud_rate']
        self.serial = Serial(self, port, baud_rate)

    def process_serial_event(self, event):
        logger.debug("Processing event '{}'".format(event))

        if self.ARDUINO_PROTOCOL.EVENT_TYPE not in event:
            logger.error("Event has no event_type: skipping")
            return

        if event[self.ARDUINO_PROTOCOL.EVENT_TYPE] == self.ARDUINO_PROTOCOL.RFID_READ:
            if self.ARDUINO_PROTOCOL.READER not in event:
                logger.error("Event has no reader: skipping")
                return

            if self.ARDUINO_PROTOCOL.TAG not in event:
                logger.error("Event has no value: skipping")
                return

            reader = event[self.ARDUINO_PROTOCOL.READER]
            tag = event[self.ARDUINO_PROTOCOL.TAG]
            self.on_rfid_read(reader, tag)

    def process_event(self, event):
        logger.debug("Processing event '{}'".format(event))

        if self.PROTOCOL.EVENT_TYPE not in event:
            logger.error("Event has no event_type: skipping")
            return

        if event[self.PROTOCOL.EVENT_TYPE] == self.PROTOCOL.RESET:
            self.niryo_controller.reset()

        elif event[self.PROTOCOL.EVENT_TYPE] == self.PROTOCOL.SET_STATUS:
            if self.PROTOCOL.STATUS not in event:
                logger.error("Event has no status: skipping")
                return

            status = event[self.PROTOCOL.STATUS]
            self.niryo_controller.status = status

        elif event[self.PROTOCOL.EVENT_TYPE] == self.PROTOCOL.SET_DIFFICULTY:
            if self.PROTOCOL.DIFFICULTY not in event:
                logger.error("Event has no difficulty: skipping")
                return

            difficulty = event[self.PROTOCOL.DIFFICULTY]
            self.niryo_controller.difficulty = difficulty

    def on_rfid_read(self, reader, tag):
        if not tag:
            self.niryo_controller.eject_floppy(reader)

        serialized_tag = "-".join(tag)

        for floppy in self.floppies:
            if floppy["tag"] == serialized_tag:
                self.niryo_controller.insert_floppy(reader, tag)
                break

    def set_led_color(self, strip, led, r, g, b, commit=False):
        self.serial.send_event(
            {
                "event_type": "led",
                "strip": strip,
                "led": led,
                "r": r,
                "g": g,
                "b": b,
                "commit": commit,
            }
        )

    def process_success(self):
        self.send_event({"success": True})
