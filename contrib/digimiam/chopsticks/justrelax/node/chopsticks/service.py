from gpiozero import InputDevice
import board
import neopixel

from twisted.internet.reactor import callLater
from twisted.internet.task import LoopingCall

from justrelax.common.logging_utils import logger
from justrelax.node.service import JustSockClientService, event


class Letter:
    """
    A letter on the "control" panel.
    Manage it's color, react to chopstick insertion, and interact with neighboring letters.
    """

    led_strip = None
    letters = []
    colors = {}

    success = False

    def __init__(
            self,
            plug_reactions, unplug_reactions, periodic_reactions,
            reaction_pin, led_index, led_success_color,
    ):
        self._difficulty = None
        self._led_color = None

        self.reaction_pin = InputDevice(reaction_pin)
        self.is_chopstick_plugged = self.reaction_pin.is_active

        self.led_index = led_index
        Letter.led_strip[self.led_index] = (0, 0, 0)

        self.led_success_color = led_success_color

        self.plug_reactions = {}
        for difficulty, reaction_method in plug_reactions.items():
            self.plug_reactions[difficulty] = getattr(
                self, "reaction_{}".format(reaction_method))

        self.unplug_reactions = {}
        for difficulty, reaction_method in unplug_reactions.items():
            self.unplug_reactions[difficulty] = getattr(
                self, "reaction_{}".format(reaction_method))

        self.periodic_reactions = periodic_reactions
        for _, reaction_task in self.periodic_reactions.items():
            # Overwrite from string to actual method to ensure that all those methods exist
            # in order to reduce possible surprises during the game session.
            reaction_task["reaction"] = getattr(self, "reaction_{}".format(reaction_task["reaction"]))
        self.periodic_task = None

        self.delayed_reaction_task = None

        self.update_color_task = LoopingCall(self._update_color)
        self.update_color_task.start(0.2)

    @property
    def difficulty(self):
        return self._difficulty

    @difficulty.setter
    def difficulty(self, value):
        self._difficulty = value

        if self.periodic_task:
            self.periodic_task.stop()

        new_periodic_task = self.periodic_reactions.get(self.difficulty, None)
        if new_periodic_task is None:
            self.periodic_task = None
        else:
            self.periodic_task = LoopingCall(self.execute_periodic_reaction, new_periodic_task["reaction"])
            self.periodic_task.start(new_periodic_task["period"])

    @property
    def led_color(self):
        return self._led_color

    @led_color.setter
    def led_color(self, value):
        self._led_color = value
        logger.debug("Letter {}: {}".format(self.letters.index(self), value))

    def _update_color(self):
        # Get GRB values of given colors from settings
        red = self.colors.get(self.led_color, {}).get("r", 0)
        green = self.colors.get(self.led_color, {}).get("g", 0)
        blue = self.colors.get(self.led_color, {}).get("b", 0)
        Letter.led_strip[self.led_index] = (red, green, blue)

    def check_success(self):
        # A letter evaluates to True if its led_color equals to its success_color
        if all(self.letters) and not Letter.success:
            Letter.success = True
            self.on_success()

    def reaction_do_nothing(self):
        pass

    def reaction_toggle_blue_orange(self):
        if self.led_color == "blue":
            self.led_color = "orange"
        elif self.led_color == "orange":
            self.led_color = "blue"
        else:
            logger.debug("Letter {} color is {}: nothing to do".format(
                self.letters.index(self), self.led_color))

    def reaction_set_blue(self):
        self.led_color = "blue"

    def reaction_set_orange(self):
        self.led_color = "orange"

    def reaction_switch_off(self):
        self.led_color = "switched_off"

    def reaction_toggle_others_blue_orange(self):
        for letter in self.letters:
            if letter != self:
                letter.reaction_toggle_blue_orange()

    # To be called regularly by a twisted looping task. gpiozero's signals enter in conflict
    # with twisted loop so we can't use methods like "when_activated" or "when_deactivated".
    def check_chopstick(self):
        if self.reaction_pin.is_active != self.is_chopstick_plugged:
            self.is_chopstick_plugged = self.reaction_pin.is_active
            if self.is_chopstick_plugged:
                self.on_chopstick_plug()
            else:
                self.on_chopstick_unplug()

    def on_chopstick_plug(self):
        logger.debug("Letter {} chopstick plugged".format(self.letters.index(self)))

        if self.delayed_reaction_task and self.delayed_reaction_task.active():
            logger.debug("Canceling previous reaction task")
            self.delayed_reaction_task.cancel()
        else:
            self.delayed_reaction_task = callLater(0.2, self._on_chopstick_plug)

    def _on_chopstick_plug(self):
        logger.debug("Executing letter {} chopstick plug reaction".format(self.letters.index(self)))
        reaction = self.plug_reactions.get(self.difficulty, self.reaction_do_nothing)
        reaction()
        self.check_success()

    def on_chopstick_unplug(self):
        logger.debug("Letter {} chopstick unplugged".format(self.letters.index(self)))

        if self.delayed_reaction_task and self.delayed_reaction_task.active():
            logger.debug("Canceling previous reaction task")
            self.delayed_reaction_task.cancel()
        else:
            self.delayed_reaction_task = callLater(0.2, self._on_chopstick_unplug)

    def _on_chopstick_unplug(self):
        logger.debug("Executing letter {} chopstick unplug reaction".format(self.letters.index(self)))
        reaction = self.unplug_reactions.get(self.difficulty, self.reaction_do_nothing)
        reaction()
        self.check_success()

    def execute_periodic_reaction(self, reaction):
        logger.debug("Letter {} periodic reaction".format(self.letters.index(self)))
        reaction()
        self.check_success()

    @staticmethod
    def on_success():
        logger.info("Success")

    def __bool__(self):
        return self.led_color == self.led_success_color


class Chopsticks(JustSockClientService):
    def __init__(self, *args, **kwargs):
        super(Chopsticks, self).__init__(*args, **kwargs)

        self.initial_difficulty = self.node_params['difficulty']['initial']
        self.available_difficulties = self.node_params['difficulty']['available']
        self.colors = self.node_params['colors']
        self.letters_configuration = self.node_params['letters']

        self.led_strip = neopixel.NeoPixel(board.D18, self.node_params['n_led'])

        for led in self.node_params['static_blue']:
            self.led_strip[led] = self.color('blue')
        for led in self.node_params['static_orange']:
            self.led_strip[led] = self.color('orange')

        self.letters = []
        self.init_letters()

        self.watch_chopsticks = LoopingCall(self.check_chopsticks)
        self.watch_chopsticks.start(1 / self.node_params['watcher_frequency'])

    def init_letters(self):
        Letter.led_strip = self.led_strip
        Letter.letters = self.letters
        Letter.colors = self.colors
        Letter.on_success = self.notify_success

        for letter_conf in self.letters_configuration:
            letter = Letter(
                letter_conf.get('chopstick_plug_reactions', {}),
                letter_conf.get('chopstick_unplug_reactions', {}),
                letter_conf.get('periodic_reactions', {}),
                letter_conf['reaction_pin'],
                letter_conf['led_index'],
                letter_conf['led_success_color'],
            )
            self.letters.append(letter)

        self.event_reset()

    def check_chopsticks(self):
        for letter in self.letters:
            letter.check_chopstick()

    def notify_success(self):
        self.send_event({"category": "success"})

    def set_difficulty(self, difficulty):
        if difficulty not in self.available_difficulties:
            logger.error("Unknown difficulty '{}' (must be one of {}): skipping".format(
                difficulty, ", ".join(self.available_difficulties)
            ))
            return

        for letter in self.letters:
            letter.difficulty = difficulty

    @event(filter={'category': 'reset'})
    def event_reset(self):
        Letter.success = False

        for letter_index, letter in enumerate(self.letters):
            letter.difficulty = self.initial_difficulty
            letter.led_color = self.letters_configuration[letter_index]['led_initial_color']

    @event(filter={'category': 'emulate_chopstick_plug'})
    def event_emulate_chopstick_plug(self, letter_index: int):
        self.letters[letter_index].on_chopstick_plug()

    @event(filter={'category': 'emulate_chopstick_unplug'})
    def event_emulate_chopstick_unplug(self, letter_index: int):
        self.letters[letter_index].on_chopstick_unplug()

    @event(filter={'category': 'force_success'})
    def event_force_success(self):
        self.letters[0].on_success()

    @event(filter={'category': 'set_difficulty'})
    def event_set_difficulty(self, difficulty: str):
        self.set_difficulty(difficulty)
    
    def color(self, value):
        red = self.colors.get(value, {}).get("r", 0)
        green = self.colors.get(value, {}).get("g", 0)
        blue = self.colors.get(value, {}).get("b", 0)
        return red, green, blue
