from gpiozero import InputDevice, OutputDevice

from twisted.internet.reactor import callLater
from twisted.internet.task import LoopingCall

from justrelax.core.logging_utils import logger
from justrelax.core.node import MagicNode, on_event


class ArduinoProtocol:
    CATEGORY = "c"

    ERROR = "e"

    PLAYING = "p"
    SUCCESS = "w"
    CONFIGURE = "c"
    CONFIGURE_PERMA_BLUE_LEDS = "b"
    CONFIGURE_PERMA_ORANGE_LEDS = "o"


class Letter:
    def __init__(self, index, on_plug_callback, on_unplug_callback, reaction_pin, led_pin, success_color):
        self._color = None

        self.index = index
        self.on_plug_callback = on_plug_callback
        self.on_unplug_callback = on_unplug_callback

        self.reaction_pin = InputDevice(reaction_pin, pull_up=True)
        self.is_chopstick_plugged = self.reaction_pin.is_active

        self.led_pin = OutputDevice(led_pin)

        self.success_color = success_color

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value
        if value == 'blue':
            self.led_pin.on()
        else:
            self.led_pin.off()
        logger.info("Letter {}: {}".format(self.index, value))

    def check_chopstick(self):
        if self.reaction_pin.is_active != self.is_chopstick_plugged:
            self.is_chopstick_plugged = self.reaction_pin.is_active
            if self.is_chopstick_plugged:
                self.on_plug_callback(self.index)
            else:
                self.on_unplug_callback(self.index)

    def reaction_do_nothing(self):
        pass

    def reaction_toggle_blue_orange(self):
        if self.color == "blue":
            self.color = "orange"
        elif self.color == "orange":
            self.color = "blue"
        else:
            logger.info("Color is {}: nothing to do".format(self.color))

    def reaction_set_blue(self):
        self.color = "blue"

    def reaction_set_orange(self):
        self.color = "orange"

    def reaction_switch_off(self):
        self.color = "switched_off"

    def __bool__(self):
        return self.color == self.success_color


class Chopsticks(MagicNode):
    def __init__(self, *args, **kwargs):
        self._difficulty = None

        super(Chopsticks, self).__init__(*args, **kwargs)

        self.available_difficulties = self.config['difficulty']['available']
        self.letters_configuration = self.config['letters']

        self.letters = []
        for letter_index, letter_conf in enumerate(self.letters_configuration):
            letter = Letter(
                letter_index, self.on_chopstick_plug, self.on_chopstick_unplug,
                letter_conf['reaction_pin'], letter_conf['led_pin'], letter_conf['led_success_color'])
            self.letters.append(letter)

        self.difficulty = self.config['difficulty']['initial']
        self.success = False

        callLater(3, self.configure)
        self.check_chopsticks_task = LoopingCall(self.check_chopsticks)
        self.check_chopsticks_task.start(0.01)

    @property
    def difficulty(self):
        return self._difficulty

    @difficulty.setter
    def difficulty(self, value):
        if value not in self.available_difficulties:
            logger.error("Unknown difficulty '{}' (must be one of {}): skipping".format(
                value, ", ".join(self.available_difficulties)))

        self._difficulty = value

    def configure(self):
        logger.info("Configuring static led: {} blue, {} orange".format(
            self.config['static_blue'], self.config['static_orange']))

        self.send_serial(
            {
                ArduinoProtocol.CATEGORY: ArduinoProtocol.CONFIGURE,
                ArduinoProtocol.CONFIGURE_PERMA_BLUE_LEDS: self.config['static_blue'],
                ArduinoProtocol.CONFIGURE_PERMA_ORANGE_LEDS: self.config['static_orange'],
            }
        )
        self.event_reset()

    @on_event(filter={'category': 'reset'})
    def event_reset(self):
        logger.info("Reset")
        self.success = False
        self.send_serial({ArduinoProtocol.CATEGORY: ArduinoProtocol.PLAYING})
        for letter in self.letters:
            letter.color = self.letters_configuration[letter.index]['led_initial_color']

    def check_chopsticks(self):
        for letter in self.letters:
            letter.check_chopstick()

        # A letter evaluates to True if its led_color equals to its success_color
        if all(self.letters):
            self.on_success()

    @on_event(filter={'category': 'emulate_chopstick_plug'})
    def on_chopstick_plug(self, letter_index: int):
        logger.info("Letter {} chopstick plugged".format(letter_index))
        reaction = self.letters_configuration[letter_index].get('chopstick_plug_reactions', {}).get(
            self.difficulty, 'do_nothing')
        reaction_callable = getattr(self.letters[letter_index], 'reaction_{}'.format(reaction))
        reaction_callable()

    @on_event(filter={'category': 'emulate_chopstick_unplug'})
    def on_chopstick_unplug(self, letter_index: int):
        logger.info("Letter {} chopstick unplugged".format(letter_index))
        reaction = self.letters_configuration[letter_index].get('chopstick_unplug_reactions', {}).get(
            self.difficulty, 'do_nothing')
        reaction_callable = getattr(self.letters[letter_index], 'reaction_{}'.format(reaction))
        reaction_callable()

    @on_event(filter={'category': 'set_difficulty'})
    def event_set_difficulty(self, difficulty: str):
        self.difficulty = difficulty

    @on_event(filter={'category': 'force_success'})
    def on_success(self):
        if not self.success:
            self.success = True
            logger.info("Success")
            self.publish({"category": "success"})
            self.send_serial({ArduinoProtocol.CATEGORY: ArduinoProtocol.SUCCESS})
