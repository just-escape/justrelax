import random

import board
import neopixel

from twisted.internet import reactor

from justrelax.node.service import JustSockClientService
from justrelax.node.helper import Serial

from justrelax.common.logging_utils import logger


class NiryoController:
    CHRONO_LEDS = 23
    STATUSES = {"chaos", "mute", "playing", "success"}

    def __init__(self, control_panel_service, initial_difficulty, difficulties):
        self.service = control_panel_service

        self.tasks = {}

        self.difficulties = difficulties
        self._difficulty = list(self.difficulties)[0]  # By default. Not reliable.
        self.difficulty = initial_difficulty

        self.chrono_leds = neopixel.NeoPixel(board.D18, self.CHRONO_LEDS, auto_write=False)
        self.chrono_leds.brightness = 0.1
        self._status_leds = ["b"] * 3

        self.current_chrono_led = -1  # -1 <=> game not started
        self.success_sequence = [None, None, None, None, None]
        self.generate_success_sequence()

        self.floppy_readers = [None, None, None, None, None]

        self._status = None
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
            self._difficulty = value

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
        logger.debug("Generating new success sequence")
        new_sequence = []
        available_floppies = self.difficulties[self.difficulty]["available_floppies"]
        if 6 > len(available_floppies):
            # The algorithm below might end up in a deadlock
            logger.error("Please submit at least 6 available floppies: skipping sequence generation")
            return

        for i in range(5):
            valid_choice = False
            while not valid_choice:
                floppy = random.choice(available_floppies)
                if self.success_sequence[i] != floppy and floppy not in new_sequence:
                    new_sequence.append(floppy)
                    valid_choice = True

        self.success_sequence = new_sequence
        logger.info("The new success sequence is {}".format(self.success_sequence))

    def set_status_leds_color(self, first=None, second=None, third=None):
        if first is not None:
            self._status_leds[0] = first
        if second is not None:
            self._status_leds[1] = second
        if third is not None:
            self._status_leds[2] = third
        self.service.set_status_leds_colors(self._status_leds)

    def set_chrono_led_color(self, led_index, r=0, g=0, b=0, commit=True):
        self.chrono_leds[self.CHRONO_LEDS - 1 - led_index] = (r, g, b)
        if commit:
            self.chrono_leds.show()

    def get_ordered_chrono_leds(self):
        return reversed(self.chrono_leds)

    def on_chaos(self):
        self.set_status_leds_color(first="R", second="R", third="R")

        def init_animation(chrono_led=0):
            if chrono_led < 5:
                self.set_chrono_led_color(chrono_led, r=255)
                self.tasks["chaos_animation"] = reactor.callLater(
                    0.1, init_animation, chrono_led + 1)
            else:
                animation_loop(chrono_led=5)

        def animation_loop(chrono_led=5):
            next_chrono_led = (chrono_led + 1) % self.CHRONO_LEDS
            self.tasks["chaos_animation"] = reactor.callLater(
                0.1, animation_loop, next_chrono_led)

            self.set_chrono_led_color((chrono_led - 5) % self.CHRONO_LEDS, r=0, g=0, b=0)
            self.set_chrono_led_color(chrono_led, r=255)

        init_animation()

    def on_mute(self):
        self.chrono_leds.fill((0, 0, 0))
        self.set_status_leds_color(first="r", second="b", third="b")

    def on_playing(self):
        self.current_chrono_led = -1
        self.chrono_leds.fill((0, 0, 0))
        self.chrono_leds.show()

        self.set_status_leds_color(first="g", second="w", third="b")

        self.tic_tac()

    def on_success(self):
        def post_delay():
            starting_chrono_led = 0
            for led_index, led_color in enumerate(self.get_ordered_chrono_leds()):
                if led_color != (0, 255, 0):
                    starting_chrono_led = led_index
                    break

            fill_green_animation(starting_chrono_led)

        def fill_green_animation(chrono_led):
            if chrono_led < self.CHRONO_LEDS:
                self.tasks["success_animation"] = reactor.callLater(
                    0.1, fill_green_animation, chrono_led + 1)
                self.set_chrono_led_color(chrono_led, g=255)
            else:
                self.set_status_leds_color(second="G")

                self.chrono_leds.fill((0, 0, 0))
                init_chaser_animation()

        def init_chaser_animation(chrono_led=0):
            if chrono_led < 5:
                self.set_chrono_led_color(chrono_led, g=255)
                self.tasks["success_animation"] = reactor.callLater(
                    0.1, init_chaser_animation, chrono_led + 1)
            else:
                self.set_status_leds_color(second="g")
                main_chaser_animation(chrono_led=5)

        def main_chaser_animation(chrono_led=5, repeat=4):
            if chrono_led == 0:
                repeat -= 1
                if repeat == 0:
                    finish_chaser_animation(chrono_led=18)
                    return

            self.tasks["success_animation"] = reactor.callLater(
                0.1, main_chaser_animation, (chrono_led + 1) % self.CHRONO_LEDS, repeat)

            self.set_chrono_led_color((chrono_led - 5) % self.CHRONO_LEDS, r=0, g=0, b=0)
            self.set_chrono_led_color(chrono_led, g=255)

        def finish_chaser_animation(chrono_led=18):
            if chrono_led < self.CHRONO_LEDS:
                self.set_chrono_led_color(chrono_led, r=0, g=0, b=0)
                self.tasks["success_animation"] = reactor.callLater(
                    0.1, finish_chaser_animation, chrono_led + 1)
            else:
                post_animation()

        def post_animation():
            self.service.process_success()

        self.tasks["success_animation"] = reactor.callLater(0.5, post_delay)

    def insert_floppy(self, reader_index, floppy):
        logger.info("Insert floppy {} in reader index={}".format(floppy, reader_index))
        self.floppy_readers[reader_index] = floppy

        if self.status != "playing":
            logger.debug("Game is not started yet: nothing to do")
            return

        animation_task = self.tasks.get("animation", None)
        if animation_task and animation_task.active():
            animation_task.cancel()

        # Chrono has not started <=> game is not started
        chrono_task = self.tasks.get("chrono", None)
        if not chrono_task or not chrono_task.active():
            logger.debug("Chrono is not running: updating errors")
            self.display_inserted_floppies_errors_before_restart()

        # The game has started
        else:
            expected_reader_index = 4 - self.floppy_readers.count(None)
            insert_in_expected_reader = reader_index == expected_reader_index
            good_insert = self.floppy_readers[reader_index] == self.success_sequence[reader_index]

            if not insert_in_expected_reader or not good_insert:
                logger.debug("Bad insert: stopping chrono and running bad move animation")
                chrono_task.cancel()
                self.bad_move_failure_animation(reader_index)

            else:
                if expected_reader_index == 4:
                    logger.debug("Good insert in the last reader: victory!")
                    self.status = "success"
                else:
                    logger.debug("Good insert: running good move animation")
                    self.good_move_animation(reader_index)

    def eject_floppy(self, reader_index):
        logger.info("Remove floppy {} from reader index={}".format(
            self.floppy_readers[reader_index], reader_index))
        self.floppy_readers[reader_index] = None

        if self.status != "playing":
            logger.debug("Game is not started yet: nothing to do")
            return

        animation_task = self.tasks.get("animation", None)
        if animation_task and animation_task.active():
            animation_task.cancel()

        chrono_task = self.tasks.get("chrono", None)
        if chrono_task and chrono_task.active():
            logger.debug("Chrono is running: stopping chrono and running bad move animation")
            chrono_task.cancel()
            self.bad_move_failure_animation(reader_index)
        else:
            if all([floppy is None for floppy in self.floppy_readers]):
                logger.debug("All floppies have been removed: restart the game")
                self.restart_game()
            else:
                logger.debug("Some floppies remain inserted: updating errors")
                self.display_inserted_floppies_errors_before_restart()

    def good_move_animation(self, reader_index):
        self.tasks["chrono"].delay(0.01)  # To be sure not to hit race conditions

        # TODO: send the order to the niryo to move
        # TODO: music effects

        starting_chrono_led = 0
        for led_index, led_color in enumerate(self.get_ordered_chrono_leds()):
            if led_color != (0, 255, 0):
                starting_chrono_led = led_index
                break
        target_chrono_led = reader_index * 5 + 3 - 1
        self.current_chrono_led = target_chrono_led

        def animation_loop(chrono_led):
            if chrono_led <= target_chrono_led:
                self.tasks["chrono"].delay(0.1)
                self.tasks["animation"] = reactor.callLater(0.1, animation_loop, chrono_led + 1)
                self.set_chrono_led_color(chrono_led, g=255)
            else:
                post_animation()

        def post_animation():
            # TODO: send the new pattern to the other device
            pass

        animation_loop(starting_chrono_led)

    def display_inserted_floppies_errors_before_restart(self):
        self.set_status_leds_color(second="r")

        self.chrono_leds.fill((0, 0, 0))
        for reader_index, floppy in enumerate(self.floppy_readers):
            if floppy is not None:
                self.set_chrono_led_color(5 * reader_index, r=255, commit=False)
                self.set_chrono_led_color(5 * reader_index + 1, r=255, commit=False)
                self.set_chrono_led_color(5 * reader_index + 2, r=255, commit=False)
            else:
                self.set_chrono_led_color(5 * reader_index, r=0, g=0, b=0, commit=False)
                self.set_chrono_led_color(5 * reader_index + 1, r=0, g=0, b=0, commit=False)
                self.set_chrono_led_color(5 * reader_index + 2, r=0, g=0, b=0, commit=False)
        self.chrono_leds.show()

    def tic_tac(self):
        self.current_chrono_led += 1
        if self.is_it_too_late():
            self.time_elapsed_failure_animation()
        else:
            delay = self.difficulties[self.difficulty]["chrono_leds_frequency"]
            self.tasks["chrono"] = reactor.callLater(delay, self.tic_tac)

            self.set_chrono_led_color(self.current_chrono_led, r=255, g=255, b=255)

    def is_it_too_late(self):
        if self.current_chrono_led >= self.CHRONO_LEDS:
            return True

        checkpoints = {
            3: 0,
            8: 1,
            13: 2,
            18: 3,
        }

        if self.current_chrono_led in checkpoints:
            checkpoint_reader = checkpoints[self.current_chrono_led]
            if self.floppy_readers[checkpoint_reader] != self.success_sequence[checkpoint_reader]:
                return True

        return False

    def time_elapsed_failure_animation(self):
        self.set_status_leds_color(second="r")

        def blink_chrono_leds_red(times=5, toggle=True):
            for led_index in range(self.current_chrono_led):
                self.set_chrono_led_color(led_index, r=255 if toggle else 0, commit=False)
            self.chrono_leds.show()

            times -= 1
            if times > 0:
                self.tasks["animation"] = reactor.callLater(
                    0.1, blink_chrono_leds_red, times, not toggle)
            else:
                self.tasks["animation"] = reactor.callLater(1, post_animation)

        def post_animation():
            if all([floppy is None for floppy in self.floppy_readers]):
                self.restart_game()
            else:
                self.display_inserted_floppies_errors_before_restart()

        blink_chrono_leds_red()

    def bad_move_failure_animation(self, reader_index):
        self.set_status_leds_color(second="R")

        def blink_reader_leds_red(times=5, toggle=True):
            self.set_chrono_led_color(5 * reader_index, r=255 if toggle else 0)
            self.set_chrono_led_color(5 * reader_index + 1, r=255 if toggle else 0)
            self.set_chrono_led_color(5 * reader_index + 2, r=255 if toggle else 0)

            times -= 1
            if times > 0:
                self.tasks["animation"] = reactor.callLater(
                    0.1, blink_reader_leds_red, times, not toggle)
            else:
                self.tasks["animation"] = reactor.callLater(
                    1, self.display_inserted_floppies_errors_before_restart)

        blink_reader_leds_red()

    def restart_game(self):
        self.generate_success_sequence()
        self.current_chrono_led = -1
        self.chrono_leds.fill((0, 0, 0))
        self.chrono_leds.show()
        self.set_status_leds_color(second="w")
        self.tasks["animation"] = reactor.callLater(3, self.tic_tac)

    def reset(self):
        self.status = "chaos"


class ControlPanel(JustSockClientService):
    class ARDUINO_PROTOCOL:
        EVENT_TYPE = "e"

        RESET = "r"

        MODE_MANUAL = "m"

        FLOPPY_READ = "f"
        READER = "r"
        TAG = "t"

        PROTOCOL_SET_COLORS = "s"
        PROTOCOL_COLORS = "c"

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

        port = self.node_params['arduino']['port']
        baud_rate = self.node_params['arduino']['baud_rate']
        self.serial = Serial(self, port, baud_rate)

        initial_difficulty = self.node_params["initial_difficulty"]
        difficulties = self.node_params["difficulties"]
        self.niryo_controller = NiryoController(self, initial_difficulty, difficulties)

    def process_serial_event(self, event):
        logger.debug("Processing event '{}'".format(event))

        if self.ARDUINO_PROTOCOL.EVENT_TYPE not in event:
            logger.error("Event has no event_type: skipping")
            return

        if event[self.ARDUINO_PROTOCOL.EVENT_TYPE] == self.ARDUINO_PROTOCOL.FLOPPY_READ:
            if self.ARDUINO_PROTOCOL.READER not in event:
                logger.error("Event has no reader: skipping")
                return

            if self.ARDUINO_PROTOCOL.TAG not in event:
                logger.error("Event has no value: skipping")
                return

            reader = event[self.ARDUINO_PROTOCOL.READER]
            tag = event[self.ARDUINO_PROTOCOL.TAG]
            self.on_rfid_read(reader, tag)

        elif event[self.ARDUINO_PROTOCOL.EVENT_TYPE] == self.ARDUINO_PROTOCOL.MODE_MANUAL:
            self.process_manual_mode()

    def process_event(self, event):
        logger.debug("Processing event '{}'".format(event))

        if self.PROTOCOL.EVENT_TYPE not in event:
            logger.error("Event has no event_type: skipping")
            return

        if event[self.PROTOCOL.EVENT_TYPE] == self.PROTOCOL.RESET:
            self.niryo_controller.reset()
            self.serial.send_event({self.ARDUINO_PROTOCOL.EVENT_TYPE: self.ARDUINO_PROTOCOL.RESET})

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
        else:
            serialized_tag = "-".join([str(byte) for byte in tag])

            for floppy_name, floppy in self.floppies.items():
                if floppy["tag"] == serialized_tag:
                    self.niryo_controller.insert_floppy(reader, floppy_name)
                    break

    def set_status_leds_colors(self, status_leds):
        colors = "".join(status_leds)

        event = {
            self.ARDUINO_PROTOCOL.EVENT_TYPE: self.ARDUINO_PROTOCOL.PROTOCOL_SET_COLORS,
            self.ARDUINO_PROTOCOL.PROTOCOL_COLORS: colors,
        }
        self.serial.send_event(event)

    def process_manual_mode(self):
        self.send_event({"manual_mode": True})

    def process_success(self):
        self.send_event({"success": True})
