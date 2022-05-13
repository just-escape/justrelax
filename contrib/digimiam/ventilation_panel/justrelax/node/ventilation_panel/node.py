import time

import gpiozero
import neopixel
import board

from twisted.internet.reactor import callLater

from justrelax.core.logging_utils import logger
from justrelax.core.node import MagicNode, on_event


class AirSource:
    def __init__(self, name, jack_port_pin):
        self.name = name
        self.jack_port = gpiozero.InputDevice(jack_port_pin)

    def is_active(self):
        return self.jack_port.is_active

    def __str__(self):
        return self.name


class AirDuct:
    def __init__(self, name, air_duct_controller, fan_pin, jack_pin, led_index):
        self.name = name
        self.ad_controller = air_duct_controller
        self.fan = gpiozero.OutputDevice(fan_pin)
        self.jack = gpiozero.OutputDevice(jack_pin)
        self.led_index = led_index
        self.connected_source = None
        self.last_connected_sources = []

    def set_color(self, color):
        r, g, b = self.ad_controller.get_color_rgb(color)
        self.ad_controller.led_strip[self.led_index] = (r, g, b)

    def check_connection(self):
        connection_found = False
        self.jack.on()
        for as_ in self.ad_controller.air_sources.values():
            if as_.is_active():
                if self.connected_source is not as_:
                    self.connected_source = as_
                    self.ad_controller.on_connect(self, as_)
                connection_found = True
                break

        if not connection_found:
            if self.connected_source is not None:
                self.connected_source = None
                self.ad_controller.on_disconnect(self)
        self.jack.off()

    def __str__(self):
        return self.name


class VentilationPanel(MagicNode):
    STATUSES = {"inactive", "playing", "success"}

    def __init__(self, *args, **kwargs):
        self._status = None

        super(VentilationPanel, self).__init__(*args, **kwargs)

        self.instructions = {}
        for round_n, round_instruction_sets in self.config["instructions"].items():
            transformed_round_instruction_sets = []
            for difficulty_instruction_sets in round_instruction_sets:
                transformed_difficulty_instruction_sets = []
                for raw_sequence in difficulty_instruction_sets:
                    elements = [e.strip() for e in raw_sequence.split(",")]
                    sequence = []
                    for element in elements:
                        ad, _, color = element.partition('>')
                        ad = ad.strip()
                        color = color.strip()

                        assert ad in self.config["air_ducts"], "{} is not declared as an air duct: aborting".format(ad)
                        assert color in self.config["colors"], "{} is not declared as a color: aborting".format(color)

                        sequence.append({"air_duct": ad, "color": color})
                    transformed_difficulty_instruction_sets.append(sequence)

                transformed_round_instruction_sets.append(transformed_difficulty_instruction_sets)

            self.instructions[round_n] = transformed_round_instruction_sets

        self.electromagnet = gpiozero.OutputDevice(self.config["lock"]["electromagnet_pin"])
        self.electromagnet_led_index = self.config["lock"]["led_index"]

        self.difficulties = self.config['difficulties']
        self.instruction_set_indexes = self.config['first_instructions']

        self.round_leds = self.config["round_leds"]

        self.led_strip = neopixel.NeoPixel(board.D18, 7)

        self.try_counters = {}  # keys are round indexes, values are counters
        self.sequence_cursor = -1  # -1 <=> game is not running
        self.success_sequence = []
        self.is_sequence_being_displayed = False
        self.round = 0

        self.air_sources = {}
        for as_name, as_ in self.config["air_sources"].items():
            self.air_sources[as_name] = AirSource(as_name, as_["jack_port_pin"])

        self.air_ducts = {}
        for ad_name, ad in self.config["air_ducts"].items():
            self.air_ducts[ad_name] = AirDuct(
                ad_name, self, ad["fan_pin"], ad["jack_pin"], ad["led_index"])

        self.colors = self.config["colors"]

        self.check_jacks_task = callLater(1, self.check_jacks)
        self.animation_tasks = {}
        self.unskippable_animation_task = None

    @on_event(filter={'category': 'request_node_session_data'})
    def publish_session_data(self):
        self.publish_status()
        self.publish_instructions()
        self.publish_difficulties()
        self.publish_instruction_set_indexes()
        self.notify_start_new_round(None if self.status == "inactive" else self.round)
        self.publish_try_counters()
        self.publish_sequence_cursor()
        self.publish_success_sequence()
        self.publish_is_sequence_being_displayed()
        self.publish_air_ducts()

    def publish_status(self):
        self.publish(
            {
                'category': 'set_session_data',
                'key': 'ventilation_panel_status',
                'data': self.status,
            }
        )

    def publish_instructions(self):
        self.publish(
            {
                'category': 'set_session_data',
                'key': 'ventilation_panel_instructions',
                'data': self.instructions,
            }
        )

    def publish_difficulties(self):
        self.publish(
            {
                'category': 'set_session_data',
                'key': 'ventilation_panel_difficulties',
                'data': self.difficulties,
            }
        )

    def publish_instruction_set_indexes(self):
        self.publish(
            {
                'category': 'set_session_data',
                'key': 'ventilation_panel_instruction_set_indexes',
                'data': self.instruction_set_indexes,
            }
        )

    def publish_try_counters(self):
        self.publish(
            {
                'category': 'set_session_data',
                'key': 'ventilation_panel_try_counters',
                'data': self.try_counters,
            }
        )

    def publish_sequence_cursor(self):
        self.publish(
            {
                'category': 'set_session_data',
                'key': 'ventilation_panel_sequence_cursor',
                'data': self.sequence_cursor,
            }
        )

    def publish_success_sequence(self):
        self.publish(
            {
                'category': 'set_session_data',
                'key': 'ventilation_panel_success_sequence',
                'data': self.success_sequence,
            }
        )

    def publish_is_sequence_being_displayed(self):
        self.publish(
            {
                'category': 'set_session_data',
                'key': 'ventilation_panel_is_sequence_being_displayed',
                'data': self.is_sequence_being_displayed,
            }
        )

    def publish_air_ducts(self):
        self.publish(
            {
                'category': 'set_session_data',
                'key': 'ventilation_panel_air_ducts',
                'data': {
                    as_.name: as_.connected_source.name
                    if as_.connected_source else None
                    for as_ in self.air_ducts.values()
                },
            }
        )

    def on_first_connection(self):
        self.status = "inactive"
        self.publish_session_data()

    @on_event(filter={'category': 'set_status'})
    def event_set_status(self, status: str):
        self.status = status

    @on_event(filter={'category': 'set_round_difficulty'})
    def event_set_round_difficulty(self, round_: int, difficulty_index: int, instruction_set_index: int):
        if round_ not in [0, 1, 2]:
            logger.error("round_ is not 0, 1 or 2")
            return

        safe_difficulty_index = max(
            0,
            min(
                len(self.instructions[f"round{round_}"]) - 1,
                difficulty_index
            )
        )
        safe_cycle_index = max(
            0,
            min(
                len(self.instructions[f"round{round_}"][safe_difficulty_index]) - 1,
                instruction_set_index
            )
        )

        self.difficulties[round_] = safe_difficulty_index
        self.instruction_set_indexes[round_] = safe_cycle_index
        self.publish_difficulties()
        self.publish_instruction_set_indexes()

    def good_connection(self, sequence_cursor):
        self.publish({'category': 'good_connection', 'sequence_cursor': sequence_cursor})

    def bad_move(self):
        self.publish({'category': 'bad_move'})

    def notify_status(self, status):
        self.publish({"category": "set_status", "status": status})
        self.publish_status()

    def notify_start_new_round(self, round_):
        self.publish({"category": "start_new_round", "round": round_})

    def notify_round_complete(self, round_):
        # Local rounds are 0, 1, 2. Documentation rounds are 1, 2, 3
        self.publish({"category": "round_complete", "round": round_ + 1})

    def notify_instruction(self, instruction):
        self.publish({"category": "notify_instruction", "instruction": instruction})

    def notify_success(self):
        self.publish({"category": "success"})

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        if value not in self.STATUSES:
            logger.warning("Status {} not in {}: skipping".format(value, ", ".join(self.STATUSES)))
            return

        if value == self.status:
            logger.info("Status is already {}: skipping".format(value))
            return

        logger.info("Setting status to {}".format(value))
        self._status = value

        if self._status == "inactive":
            self.skip_skippable_animations()

            if self.unskippable_animation_task and self.unskippable_animation_task.active():
                self.unskippable_animation_task.cancel()
            self.on_inactive()

        elif self._status == "playing":
            self.skip_skippable_animations()

            if self.unskippable_animation_task and self.unskippable_animation_task.active():
                self.unskippable_animation_task.cancel()
            self.on_playing()

        elif self._status == "success":
            self.on_success()

        self.notify_status(self.status)

    def skip_skippable_animations(self):
        for ad in self.air_ducts.values():
            self.led_strip[ad.led_index] = (0, 0, 0)
        for task in self.animation_tasks.values():
            if task.active():
                task.cancel()

    def get_color_rgb(self, color):
        predefined_color = self.colors.get(color, {})
        r = predefined_color.get("r", 0)
        g = predefined_color.get("g", 0)
        b = predefined_color.get("b", 0)
        return r, g, b

    def on_inactive(self):
        for ad in self.air_ducts.values():
            ad.fan.off()
        self.led_strip.fill((0, 0, 0))

        self.success_sequence = []
        self.try_counters = {}
        self.electromagnet.on()
        self.led_strip[self.electromagnet_led_index] = self.get_color_rgb("light_red")
        self.notify_start_new_round(None)

    def on_playing(self):
        self.led_strip.fill((0, 0, 0))

        self.electromagnet.off()
        self.led_strip[self.electromagnet_led_index] = self.get_color_rgb("light_green")

        self.sequence_cursor = -1
        self.publish_sequence_cursor()
        self.round = 0
        self.try_counters = {}
        self.publish_try_counters()
        # Force players to take an action before the game restarts
        self.display_connected_air_ducts_before_restart()
        self.notify_start_new_round(self.round)

    def on_success(self):
        self.notify_success()

    def on_connect(self, air_duct, air_source):
        logger.info("{} is connected to {}".format(air_duct, air_source))
        self.publish_air_ducts()

        if self.status != "playing":
            logger.info("Game is not started yet: nothing to do")
            return

        if self.sequence_cursor != -1:  # Game is running
            if self.is_sequence_being_displayed:
                logger.info("Sequence has not been entirely displayed: considering as an error")
                self.sequence_cursor = -1
                self.publish_sequence_cursor()
                self.is_sequence_being_displayed = False
                self.publish_is_sequence_being_displayed()
                self.bad_move_failure_animation()
                self.notify_instruction("wait_until_sequence_complete")

            elif self.success_sequence[self.sequence_cursor]["air_duct"] != air_duct.name:
                try:
                    for instruction_index, instruction in enumerate(self.success_sequence[self.sequence_cursor:]):
                        expected_air_sources = self.get_expected_sources(self.sequence_cursor + instruction_index)
                        if instruction["air_duct"] == air_duct.name and air_source in expected_air_sources:
                            self.notify_instruction("order_matters")
                except Exception:
                    pass

                logger.info("Expecting {} to be connected".format(
                    self.success_sequence[self.sequence_cursor]["air_duct"]))
                self.sequence_cursor = -1
                self.publish_sequence_cursor()
                self.bad_move_failure_animation()

            else:
                try:
                    expected_air_sources = self.get_expected_sources(self.sequence_cursor)
                except Exception:
                    expected_air_sources = set()
                    good_connection = True
                else:
                    good_connection = air_source in expected_air_sources

                if not good_connection:
                    logger.info("Expecting connection with {}".format(
                        " or ".join([str(s) for s in expected_air_sources])))
                    self.sequence_cursor = -1
                    self.publish_sequence_cursor()
                    self.bad_move_failure_animation()

                else:
                    self.good_connection(self.sequence_cursor)
                    logger.info("Good connection")
                    air_duct.fan.on()
                    air_duct.last_connected_sources.append(air_source)  # Keep track of the good history
                    if self.sequence_cursor == len(self.success_sequence) - 1:
                        self.sequence_cursor = -1
                        self.publish_sequence_cursor()
                        self.on_round_complete()
                    else:
                        self.sequence_cursor += 1
                        self.publish_sequence_cursor()
                        logger.info("Expecting element {} (cursor is {})".format(
                            self.success_sequence[self.sequence_cursor], self.sequence_cursor))
                        self.good_move_animation()

        else:  # Game is not running
            logger.info("Game is not running: updating errors")
            self.display_connected_air_ducts_before_restart()

    def on_disconnect(self, air_duct):
        logger.info("{} is not connected to any air source".format(air_duct))
        self.publish_air_ducts()

        if self.status != "playing":
            logger.info("Game is not started yet: nothing to do")
            return

        if self.sequence_cursor != -1:  # Game is running
            air_duct.fan.off()
            if self.success_sequence[self.sequence_cursor]["air_duct"] != air_duct.name:
                logger.info("It was not necessary to disconnect this air duct: considering as an error")
                self.sequence_cursor = -1
                self.publish_sequence_cursor()
                self.bad_move_failure_animation()
        else:  # Game is not running
            self.display_connected_air_ducts_before_restart()

    def on_round_complete(self):
        logger.info("Round {} complete".format(self.round))

        def step1():
            self.notify_round_complete(self.round)
            self.good_move_animation()
            self.unskippable_animation_task = callLater(1.3, step2)

        def step2():
            self.good_move_animation_reversed()
            self.unskippable_animation_task = callLater(1.3, step3)

        def step3():
            self.blink(self.round_leds[self.round], "light_green", 5)
            for ad in self.air_ducts.values():
                ad.fan.off()
            self.unskippable_animation_task = callLater(1.3, step4)

        def step4():
            if self.round < 2:
                logger.info("Going to next round".format(self.round))

                self.round += 1

                self.notify_start_new_round(self.round)
                self.display_connected_air_ducts_before_restart()

            else:
                logger.info("All rounds have been completed: victory!")
                self.notify_instruction(["all_sequences_are_correct", "digimiam_ducts_can_now_be_used"])
                self.success_animation(step5)

        def step5():
            self.status = "success"

        step1()

    def new_success_sequence(self):
        logger.info("Loading a new success sequence (try counter={})".format(self.try_counters[self.round]))

        self.success_sequence = self.instructions[
            f"round{self.round}"][self.difficulties[self.round]][self.instruction_set_indexes[self.round]]
        self.publish_success_sequence()

        logger.info("The new success sequence is {}".format(self.success_sequence))

    def display_sequence(self):
        logger.info("Displaying sequence")

        self.skip_skippable_animations()

        self.is_sequence_being_displayed = True
        self.publish_is_sequence_being_displayed()

        def display_element(index=0):
            if index < len(self.success_sequence):
                # For the last element of the sequence, this code saves a task in the unskippable_animation_task,
                # ensuring that the animation time lasts until the last led has turned black again.
                self.animation_tasks['display_sequence'] = callLater(2, display_element, index + 1)
                element = self.success_sequence[index]

                self.air_ducts[element["air_duct"]].fan.on()
                self.animation_tasks["fan"] = callLater(1.4, self.air_ducts[element["air_duct"]].fan.off)

                self.fluid_to_color(
                    self.air_ducts[element["air_duct"]].led_index,
                    element["color"],
                    1,
                    "display_element",
                    self.fluid_to_color,
                    self.air_ducts[element["air_duct"]].led_index,
                    "black",
                    1,
                    "display_element",
                )
            else:
                self.is_sequence_being_displayed = False
                self.publish_is_sequence_being_displayed()

        self.animation_tasks['display_sequence'] = callLater(0.5, display_element)

    def get_expected_sources(self, cursor):
        displayed_color = self.success_sequence[cursor]["color"]

        if displayed_color == "pink":
            return self.get_expected_sources(cursor - 1)

        elif displayed_color == "purple":
            return self.get_expected_sources(cursor + 1)

        elif displayed_color == "white":
            return {self.air_sources["as0"]}

        elif displayed_color == "yellow":
            return {self.air_sources["as1"]}

        elif displayed_color == "orange":
            return {self.air_sources["as2"]}

        elif displayed_color == "blue":
            duct = self.air_ducts[self.success_sequence[cursor]["air_duct"]]

            if len(duct.last_connected_sources) < 1:
                raise ValueError(
                    "Blue cannot be the first color given to an air duct (in the sequence {})".format(
                        self.success_sequence))

            last_source = duct.last_connected_sources[-1]

            if last_source.name == "as2":
                return {self.air_sources["as0"], self.air_sources["as1"]}
            elif last_source.name == "as1":
                return {self.air_sources["as0"]}
            else:
                raise ValueError(
                    "Blue cannot be given to an air duct after it is connected to as0 (in the sequence {})".format(
                        self.success_sequence))

        else:
            # Should never happen
            raise NotImplementedError(
                "Color {} is not known to the sequence checker: aborting".format(displayed_color))

    def blink(self, led_index, color, times, cb=None, *cb_args, **cb_kwargs):
        def blink_loop(iteration=times, toggle=True):
            self.led_strip[led_index] = self.get_color_rgb(color if toggle else "black")

            iteration -= 1
            if iteration > 0:
                self.unskippable_animation_task = callLater(
                    0.1, blink_loop, iteration, not toggle)
            else:
                if cb:
                    cb(*cb_args, **cb_kwargs)
        blink_loop()

    def fluid_to_color(self, led_index, color, duration, task_id="fluid_to_color", cb=None, *cb_args, **cb_kwargs):
        t_initial = time.monotonic()
        target_r, target_g, target_b = self.get_color_rgb(color)
        initial_r, initial_g, initial_b = self.led_strip[led_index]

        def animation(t_start, t_last_call):
            now = time.monotonic()
            percentage = (t_last_call - t_start) / duration

            if percentage > 1:
                self.led_strip[led_index] = (
                    target_r,
                    target_g,
                    target_b,
                )
                if cb:
                    cb(*cb_args, **cb_kwargs)
            else:
                self.animation_tasks[task_id] = callLater(
                    0, animation, t_start, now)

                if initial_r > target_r:
                    new_r = int(initial_r - (initial_r - target_r) * percentage)
                else:
                    new_r = int(initial_r + (target_r - initial_r) * percentage)
                if initial_g > target_g:
                    new_g = int(initial_g - (initial_g - target_g) * percentage)
                else:
                    new_g = int(initial_g + (target_g - initial_g) * percentage)
                if initial_b > target_b:
                    new_b = int(initial_b - (initial_b - target_b) * percentage)
                else:
                    new_b = int(initial_b + (target_b - initial_b) * percentage)

                self.led_strip[led_index] = (
                    new_r,
                    new_g,
                    new_b,
                )

        animation(t_initial, t_initial)

    def success_animation(self, callback):
        logger.info("Running success animation")

        def step1():
            self.led_strip[0] = self.get_color_rgb("black")
            self.led_strip[1] = self.get_color_rgb("black")
            self.led_strip[2] = self.get_color_rgb("black")
            self.unskippable_animation_task = callLater(0.1, step2)

        def step2():
            self.led_strip[0] = self.get_color_rgb("light_green")
            self.unskippable_animation_task = callLater(0.1, step3)

        def step3():
            self.led_strip[1] = self.get_color_rgb("light_green")
            self.unskippable_animation_task = callLater(0.1, step4)

        def step4():
            self.led_strip[2] = self.get_color_rgb("light_green")
            self.unskippable_animation_task = callLater(0.1, step5)

        def step5():
            self.led_strip[3] = self.get_color_rgb("light_green")
            self.unskippable_animation_task = callLater(0.1, step6)

        def step6():
            self.led_strip[0] = self.get_color_rgb("black")
            self.unskippable_animation_task = callLater(0.1, step7)

        def step7():
            self.led_strip[1] = self.get_color_rgb("black")
            self.unskippable_animation_task = callLater(0.1, step8)

        def step8():
            self.led_strip[2] = self.get_color_rgb("black")
            self.unskippable_animation_task = callLater(0.1, step9)

        def step9():
            self.led_strip[0] = self.get_color_rgb("light_green")
            self.led_strip[1] = self.get_color_rgb("light_green")
            self.led_strip[2] = self.get_color_rgb("light_green")
            self.unskippable_animation_task = callLater(1, callback)

        step1()

    def good_move_animation(self):
        logger.info("Running good move animation")

        self.skip_skippable_animations()

        self.animation_tasks["blink1"] = callLater(
            0,
            self.fluid_to_color, self.air_ducts["ad0"].led_index, "green", 0.35, "blink1",
            self.fluid_to_color, self.air_ducts["ad0"].led_index, "black", 0.35, "blink1",
        )
        self.animation_tasks["blink2"] = callLater(
            0.3,
            self.fluid_to_color, self.air_ducts["ad1"].led_index, "green", 0.35, "blink2",
            self.fluid_to_color, self.air_ducts["ad1"].led_index, "black", 0.35, "blink2",
        )
        self.animation_tasks["blink2"] = callLater(
            0.6,
            self.fluid_to_color, self.air_ducts["ad2"].led_index, "green", 0.35, "blink3",
            self.fluid_to_color, self.air_ducts["ad2"].led_index, "black", 0.35, "blink3",
        )

    def good_move_animation_reversed(self):
        logger.info("Running reversed good move animation")

        self.skip_skippable_animations()

        self.animation_tasks["blink1"] = callLater(
            0,
            self.fluid_to_color, self.air_ducts["ad2"].led_index, "green", 0.35, "blink1",
            self.fluid_to_color, self.air_ducts["ad2"].led_index, "black", 0.35, "blink1",
        )
        self.animation_tasks["blink2"] = callLater(
            0.3,
            self.fluid_to_color, self.air_ducts["ad1"].led_index, "green", 0.35, "blink2",
            self.fluid_to_color, self.air_ducts["ad1"].led_index, "black", 0.35, "blink2",
        )
        self.animation_tasks["blink2"] = callLater(
            0.6,
            self.fluid_to_color, self.air_ducts["ad0"].led_index, "green", 0.35, "blink3",
            self.fluid_to_color, self.air_ducts["ad0"].led_index, "black", 0.35, "blink3",
        )

    def bad_move_failure_animation(self):
        logger.info("Running bad move failure animation")

        self.bad_move()

        self.skip_skippable_animations()

        for ad in self.air_ducts.values():
            ad.fan.off()

        def wait_and_display_connected_air_ducts_before_restart():
            self.animation_tasks["wait"] = callLater(
                0.3, self.display_connected_air_ducts_before_restart)

        self.animation_tasks["blink1"] = callLater(
            0,
            self.fluid_to_color, self.air_ducts["ad2"].led_index, "red", 0.35, "blink1",
            self.fluid_to_color, self.air_ducts["ad2"].led_index, "black", 0.35, "blink1",
        )
        self.animation_tasks["blink2"] = callLater(
            0.3,
            self.fluid_to_color, self.air_ducts["ad1"].led_index, "red", 0.35, "blink2",
            self.fluid_to_color, self.air_ducts["ad1"].led_index, "black", 0.35, "blink2",
        )
        self.animation_tasks["blink3"] = callLater(
            0.6,
            self.fluid_to_color, self.air_ducts["ad0"].led_index, "red", 0.35, "blink3",
            self.fluid_to_color, self.air_ducts["ad0"].led_index, "black", 0.35, "blink3",
            wait_and_display_connected_air_ducts_before_restart,
        )

    def display_connected_air_ducts_before_restart(self):
        logger.info("Displaying connected air ducts in red before restart")

        for ad_name, ad in self.air_ducts.items():
            if ad.connected_source is None:
                ad.set_color("black")
            else:
                ad.set_color("red")

    @on_event(filter={'category': 'restart_round'})
    def restart_round(self):
        if self.status != "playing":
            logger.info("Game is not started yet: nothing to restart")
            return

        if not all([ad.connected_source is None for ad in self.air_ducts.values()]):
            logger.info("Cannot restart round for some ducts remain plugged")
            self.notify_instruction('unplug_before_intervention')
            return

        if self.is_sequence_being_displayed:
            logger.info("A sequence is still being displayed: aborting")
            return

        if self.unskippable_animation_task and self.unskippable_animation_task.active():
            logger.info("Some unskippable animation task is running: aborting")
            return

        logger.info("Restarting round")
        self.notify_instruction('')
        for ad in self.air_ducts.values():
            ad.set_color("black")
            ad.last_connected_sources = []

        if self.round in self.try_counters:
            self.try_counters[self.round] += 1
            self.publish_try_counters()

            if (
                len(self.instructions[f"round{self.round}"][self.difficulties[self.round]]) - 1 >
                self.instruction_set_indexes[self.round]
            ):
                # +1 only on second try, because first try is supposed to happen on the first instruction set
                self.instruction_set_indexes[self.round] += 1
                self.publish_instruction_set_indexes()

        else:
            self.try_counters[self.round] = 1
            self.publish_try_counters()

        self.new_success_sequence()
        self.sequence_cursor = 0
        self.publish_sequence_cursor()

        self.animation_tasks['display_sequence'] = callLater(0.5, self.display_sequence)

    @on_event(filter={'category': 'reset'})
    def reset(self):
        self.status = "inactive"
        self.difficulties = self.config['difficulties']
        self.instruction_set_indexes = self.config['first_instructions']
        self.publish_session_data()

    def check_jacks(self):
        self.check_jacks_task = callLater(0.1, self.check_jacks)
        if not (self.unskippable_animation_task and self.unskippable_animation_task.active()):
            for ad in self.air_ducts.values():
                ad.check_connection()
