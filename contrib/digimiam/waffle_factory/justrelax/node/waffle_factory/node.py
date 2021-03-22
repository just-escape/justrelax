import os

import neopixel
import board

from twisted.internet import reactor

from justrelax.core.logging_utils import logger
from justrelax.core.node import MagicNode, on_event


class ArduinoProtocol:
    CATEGORY = "c"

    FORWARD = "f"
    BACKWARD = "b"
    SET_SPEED = "d"
    LOW_PERIOD = "l"
    HIGH_PERIOD = "h"
    CONVEYOR_INDEX = "i"

    MOVE_SERVO = "s"
    SERVO_POSITION = "p"
    SERVO_INDEX = "i"

    SET_LED_TARGET_FREQ = "t"
    SET_LED_FREQ = "q"
    LED_INDEX = "i"
    LED_FREQ_VALUE = "v"
    LED_FREQ_STEP = "s"


class WaffleFactory(MagicNode):
    def __init__(self, *args, **kwargs):
        super(WaffleFactory, self).__init__(*args, **kwargs)

        self.conveyors = self.config['conveyors']
        self.servo_flip_delay = self.config['servo_flip_delay']
        self.servos = self.config['servos']
        self.conveyor_default_clock_period = self.config['conveyor_default_clock_period']

        self.light_led = self.config['light_led']

        self.basket_led_blink_freq = self.config['basket_led_blink_freq']
        self.basket_led_color = (
            self.config['basket_led_color']['r'],
            self.config['basket_led_color']['g'],
            self.config['basket_led_color']['b'],
        )
        self.basket_led_strip = neopixel.NeoPixel(board.D18, 4)
        self.basket_led_blink_task = None

        self.printer_patterns = {}
        self.printer_is_halted = False
        self.printer_gcode_instructions = []

        reactor.callLater(3, self.event_reset)

    def load_printer_patterns(self):
        patterns_directory = self.config['printer_patterns_directory']
        for filename in os.listdir(patterns_directory):
            path = os.path.join(patterns_directory, filename)

            if not os.path.isfile(path):
                logger.warning("{} is not a file: skipping".format(path))
                continue

            with open(path, 'r') as fh:
                logger.info("Adding printer pattern {}".format(filename))
                self.printer_patterns[filename] = fh.readlines()

    @on_event(filter={'category': 'reset'})
    def event_reset(self):
        logger.info("Reset")
        self.event_basket_led_off()
        for light_led_id, light_led in self.light_led.items():
            if light_led['on_by_default']:
                self.event_light_on(light_led_id)
            else:
                self.event_light_off(light_led_id)

    @on_event(filter={'category': 'conveyor_forward'})
    def event_conveyor_forward(self, conveyor_id: str, low_period: int = None, high_period: int = None):
        logger.info("Turning conveyor {} forward".format(conveyor_id))

        conveyor_index = self.conveyors[conveyor_id]['index']
        low_period = low_period if low_period is not None else self.conveyor_default_clock_period
        high_period = high_period if high_period is not None else self.conveyor_default_clock_period

        logger.info("Clock period: low={}, high={}".format(low_period, high_period))

        self.send_serial(
            {
                ArduinoProtocol.CATEGORY: ArduinoProtocol.FORWARD,
                ArduinoProtocol.CONVEYOR_INDEX: conveyor_index,
                ArduinoProtocol.LOW_PERIOD: low_period,
                ArduinoProtocol.HIGH_PERIOD: high_period,
            },
            port='/dev/factory',
        )

    @on_event(filter={'category': 'conveyor_backward'})
    def event_conveyor_backward(self, conveyor_id: str, low_period: int = None, high_period: int = None):
        logger.info("Turning conveyor {} backward".format(conveyor_id))

        conveyor_index = self.conveyors[conveyor_id]['index']
        low_period = low_period if low_period is not None else self.conveyor_default_clock_period
        high_period = high_period if high_period is not None else self.conveyor_default_clock_period

        logger.info("Clock period: low={}, high={}".format(low_period, high_period))

        self.send_serial(
            {
                ArduinoProtocol.CATEGORY: ArduinoProtocol.BACKWARD,
                ArduinoProtocol.CONVEYOR_INDEX: conveyor_index,
                ArduinoProtocol.LOW_PERIOD: low_period,
                ArduinoProtocol.HIGH_PERIOD: high_period,
            },
            port='/dev/factory',
        )

    @on_event(filter={'category': 'conveyor_set_clock'})
    def event_conveyor_set_clock(self, conveyor_id: str, low_period: int = None, high_period: int = None):
        logger.info("Setting conveyor {} clock periods".format(conveyor_id))

        conveyor_index = self.conveyors[conveyor_id]['index']
        low_period = low_period if low_period is not None else self.conveyor_default_clock_period
        high_period = high_period if high_period is not None else self.conveyor_default_clock_period

        logger.info("Clock period: low={}, high={}".format(low_period, high_period))

        self.send_serial(
            {
                ArduinoProtocol.CATEGORY: ArduinoProtocol.SET_SPEED,
                ArduinoProtocol.CONVEYOR_INDEX: conveyor_index,
                ArduinoProtocol.LOW_PERIOD: low_period,
                ArduinoProtocol.HIGH_PERIOD: high_period,
            },
            port='/dev/factory',
        )

    @on_event(filter={'category': 'conveyor_stop'})
    def event_stop_conveyor(self, conveyor_id: str):
        logger.info("Stopping conveyor {})".format(conveyor_id))
        self.event_conveyor_set_clock(conveyor_id, 0, 0)

    @on_event(filter={'category': 'raise_servo'})
    def event_raise_servo(self, servo_id: str):
        logger.info("Raising servo {}".format(servo_id))
        raise_position = self.servos[servo_id]['raise']
        self.event_move_servo(servo_id, raise_position)

    @on_event(filter={'category': 'lower_servo'})
    def event_lower_servo(self, servo_id: str):
        logger.info("Lowering servo {}".format(servo_id))
        lower_position = self.servos[servo_id]['lower']
        self.event_move_servo(servo_id, lower_position)

    @on_event(filter={'category': 'flip_servo'})
    def event_flip_servo(self, servo_id: str):
        logger.info("Flipping servo {}".format(servo_id))
        self.event_lower_servo(servo_id)
        reactor.callLater(self.servo_flip_delay, self.event_raise_servo, servo_id)

    @on_event(filter={'category': 'move_servo'})
    def event_move_servo(self, servo_id: str, position: int):
        logger.info("Setting servo {} position to {}".format(servo_id, position))

        servo_index = self.servos[servo_id]['index']

        self.send_serial(
            {
                ArduinoProtocol.CATEGORY: ArduinoProtocol.MOVE_SERVO,
                ArduinoProtocol.SERVO_INDEX: servo_index,
                ArduinoProtocol.SERVO_POSITION: position,
            },
            port='/dev/factory',
        )

    @on_event(filter={'category': 'light_on'})
    def event_light_on(self, led_id: str):
        logger.info("Light id={} on".format(led_id))
        self.event_light_set_target_freq(led_id, 50.)

    @on_event(filter={'category': 'light_off'})
    def event_light_off(self, led_id: str):
        logger.info("Light id={} off".format(led_id))
        self.event_light_set_freq(led_id, 0.)

    @on_event(filter={'category': 'light_set_freq'})
    def event_light_set_freq(self, led_id: str, value: float):
        value = min(value, 50.)
        logger.info("Set lights id={} freq to {}/50".format(led_id, value))

        led_index = self.light_led[led_id]['index']

        self.send_serial(
            {
                ArduinoProtocol.CATEGORY: ArduinoProtocol.SET_LED_FREQ,
                ArduinoProtocol.LED_INDEX: led_index,
                ArduinoProtocol.LED_FREQ_VALUE: value,
            },
            port='/dev/factory',
        )

    @on_event(filter={'category': 'light_set_target_freq'})
    def event_light_set_target_freq(self, led_id: str, value: float, step: float = 0.2):
        value = min(value, 50.)
        logger.info("Set lights id={} freq to {}/50 with a step of {}".format(led_id, value, step))

        led_index = self.light_led[led_id]['index']

        self.send_serial(
            {
                ArduinoProtocol.CATEGORY: ArduinoProtocol.SET_LED_TARGET_FREQ,
                ArduinoProtocol.LED_INDEX: led_index,
                ArduinoProtocol.LED_FREQ_VALUE: value,
                ArduinoProtocol.LED_FREQ_STEP: step,
            },
            port='/dev/factory',
        )

    @on_event(filter={'category': 'basket_led_on'})
    def event_basket_led_on(self):
        logger.info("Turning basket led on")
        if self.basket_led_blink_task and self.basket_led_blink_task.active():
            logger.info("Basket led were blinking: canceling")
            self.basket_led_blink_task.cancel()
        self.basket_led_strip.fill(self.basket_led_color)

    @on_event(filter={'category': 'basket_led_off'})
    def event_basket_led_off(self):
        logger.info("Turning basket led off")
        if self.basket_led_blink_task and self.basket_led_blink_task.active():
            logger.info("Basket led were blinking: canceling")
            self.basket_led_blink_task.cancel()
        self.basket_led_strip.fill((0, 0, 0))

    @on_event(filter={'category': 'basket_led_blink'})
    def event_basket_led_blink(self, frequency: int = None):
        if self.basket_led_blink_task and self.basket_led_blink_task.active():
            logger.info("Already blinking: skipping")
            return

        freq = frequency or self.basket_led_blink_freq
        logger.info("Blinking basket led (freq={}s)".format(freq))

        def blink_on(freq):
            logger.info("Blink on")
            self.basket_led_strip.fill(self.basket_led_color)
            self.basket_led_blink_task = reactor.callLater(freq, blink_off, freq)

        def blink_off(freq):
            logger.info("Blink off")
            self.basket_led_strip.fill((0, 0, 0))
            self.basket_led_blink_task = reactor.callLater(freq, blink_on, freq)

        blink_on(freq)

    def process_gcode_instruction(self, instruction):
        logger.info("Processing instruction {}".format(instruction))
        self.send_serial(instruction, '/dev/printer')

    def process_gcode_instructions(self, instructions):
        if self.printer_is_halted:
            logger.info("Printer is halted: waiting to resume")
            return

        if self.printer_gcode_instructions:
            logger.info("Some gcode instructions are already queued: ignoring")
            return

        self.printer_gcode_instructions = instructions
        self.process_gcode_instruction(self.printer_gcode_instructions[0])

    @on_event(channel='/dev/printer')
    def printer_serial_event(self, event: str):
        if event != 'Ok':
            logger.error("Unknown serial event '{}': skipping".format(event))
            return

        logger.info("Received Ok from printer: processing next instruction")
        self.printer_gcode_instructions.pop(0)  # This instruction is the one being acknowledged by the 'Ok'

        if not self.printer_gcode_instructions:
            logger.info("No more gcode instructions: going to idle state")
            return

        if self.printer_is_halted:
            logger.info("Printer is halted: waiting to resume")
            return

        next_instruction = self.printer_gcode_instructions[0]
        self.process_gcode_instruction(next_instruction)

    @on_event(filter={'category': 'printer_move'})
    def event_printer_move(self, direction: str):
        instructions = {
            'left': 'l',
            'right': 'ri',
            'front': 'f',
            'rear': 're',
        }

        instruction = instructions.get(direction)
        if instruction is None:
            logger.info("Unknown direction '{}'. It must be one of {}: ignoring".format(
                ",".join(instructions), direction))
            return

        self.process_gcode_instructions([instruction])

    @on_event(filter={'category': 'print_pattern'})
    def event_print_pattern(self, pattern: str):
        instructions = self.printer_patterns.get(pattern)
        if instructions is None:
            logger.info("Unknown pattern '{}'. It must be one of {}: ignoring".format(
                ",".join(self.printer_patterns), pattern))
            return

        self.process_gcode_instructions(instructions)

    @on_event(filter={'category': 'printer_halt'})
    def event_printer_halt(self):
        self.printer_is_halted = True

    @on_event(filter={'category': 'printer_resume'})
    def event_printer_resume(self):
        self.printer_is_halted = False

        if not self.printer_gcode_instructions:
            logger.info("No more instructions: going to idle state")
            return

        next_instruction = self.printer_gcode_instructions[0]
        self.process_gcode_instruction(next_instruction)

    @on_event(filter={'category': 'printer_stop'})
    def event_printer_stop(self):
        self.printer_gcode_instructions = []
