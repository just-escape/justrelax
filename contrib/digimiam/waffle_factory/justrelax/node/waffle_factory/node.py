import os
from copy import copy

from twisted.internet import reactor

from justrelax.core.logging_utils import logger
from justrelax.core.node import MagicNode, on_event


class ArduinoProtocol:
    CATEGORY = "c"

    HOMING = "h"
    FORWARD = "f"
    BACKWARD = "b"
    STEP_DELAY = "sd"
    MOTOR_INDEX = "i"
    N_PULSES = "n"
    LIMINARY_STEP_DELAY = "lsd"
    LIMINARY_N_PULSES = "ln"
    STOP = "stop"

    SET_LED_TARGET_FREQ = "t"
    SET_LED_FREQ = "q"
    LED_INDEX = "i"
    LED_FREQ_VALUE = "v"
    LED_FREQ_STEP = "s"

    BASKET_LED_ON = "kon"
    BASKET_LED_OFF = "koff"
    BASKET_LED_BLINK = "kblink"

    OVEN_TURN_ON = "oon"
    OVEN_TURN_OFF = "ooff"


class WaffleFactory(MagicNode):
    def __init__(self, *args, **kwargs):
        super(WaffleFactory, self).__init__(*args, **kwargs)

        self.motors = self.config['motors']
        self.motor_default_step_delay = self.config['motor_default_step_delay']

        self.light_led = self.config['light_led']

        self.printer_patterns = {}
        self.printer_is_halted = False
        self.printer_gcode_instructions = []

        self.load_printer_patterns()

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
                self.printer_patterns[filename] = [line.strip() for line in fh.readlines()]

    @on_event(filter={'category': 'reset'})
    def event_reset(self):
        logger.info("Reset")
        self.event_basket_led_off()
        for light_led_id, light_led in self.light_led.items():
            if light_led['on_by_default']:
                self.event_light_on(light_led_id)
            else:
                self.event_light_off(light_led_id)

    @on_event(filter={'category': 'motor_homing'})
    def event_motor_homing(
            self, motor_id: str, n_pulses: int, step_delay: int = None,
            liminary_n_pulses: int = 0, liminary_step_delay: int = None,
    ):
        logger.info(f"Starting homing procedure for motor {motor_id}")

        motor_index = self.motors[motor_id]["index"]
        step_delay = step_delay if step_delay is not None else self.motor_default_step_delay
        liminary_step_delay = liminary_step_delay if liminary_step_delay is not None else self.motor_default_step_delay

        logger.info(f"Step delay={step_delay}")

        self.send_serial(
            {
                ArduinoProtocol.CATEGORY: ArduinoProtocol.HOMING,
                ArduinoProtocol.MOTOR_INDEX: motor_index,
                ArduinoProtocol.N_PULSES: n_pulses,
                ArduinoProtocol.STEP_DELAY: step_delay,
                ArduinoProtocol.LIMINARY_STEP_DELAY: liminary_step_delay,
                ArduinoProtocol.LIMINARY_N_PULSES: liminary_n_pulses,
            },
            port='/dev/factory',
        )

    @on_event(filter={'category': 'motor_forward'})
    def event_motor_forward(
            self, motor_id: str, n_pulses: int, step_delay: int = None,
            liminary_n_pulses: int = 0, liminary_step_delay: int = None,
    ):
        logger.info("Turning motor {} forward".format(motor_id))

        motor_index = self.motors[motor_id]['index']
        step_delay = step_delay if step_delay is not None else self.motor_default_step_delay
        liminary_step_delay = liminary_step_delay if liminary_step_delay is not None else self.motor_default_step_delay

        logger.info("Step delay={}".format(step_delay))

        self.send_serial(
            {
                ArduinoProtocol.CATEGORY: ArduinoProtocol.FORWARD,
                ArduinoProtocol.MOTOR_INDEX: motor_index,
                ArduinoProtocol.N_PULSES: n_pulses,
                ArduinoProtocol.STEP_DELAY: step_delay,
                ArduinoProtocol.LIMINARY_STEP_DELAY: liminary_step_delay,
                ArduinoProtocol.LIMINARY_N_PULSES: liminary_n_pulses,
            },
            port='/dev/factory',
        )

    @on_event(filter={'category': 'motor_backward'})
    def event_motor_backward(
            self, motor_id: str, n_pulses: int, step_delay: int = None,
            liminary_n_pulses: int = 0, liminary_step_delay: int = None,
    ):
        logger.info("Turning motor {} backward".format(motor_id))

        motor_index = self.motors[motor_id]['index']
        step_delay = step_delay if step_delay is not None else self.motor_default_step_delay
        liminary_step_delay = liminary_step_delay if liminary_step_delay is not None else self.motor_default_step_delay

        logger.info("Step delay={}".format(step_delay))

        self.send_serial(
            {
                ArduinoProtocol.CATEGORY: ArduinoProtocol.BACKWARD,
                ArduinoProtocol.MOTOR_INDEX: motor_index,
                ArduinoProtocol.N_PULSES: n_pulses,
                ArduinoProtocol.STEP_DELAY: step_delay,
                ArduinoProtocol.LIMINARY_STEP_DELAY: liminary_step_delay,
                ArduinoProtocol.LIMINARY_N_PULSES: liminary_n_pulses,
            },
            port='/dev/factory',
        )

    @on_event(filter={'category': 'motor_stop'})
    def event_stop_motor(self, motor_id: str):
        logger.info("Stopping motor {}".format(motor_id))
        motor_index = self.motors[motor_id]['index']
        self.send_serial(
            {
                ArduinoProtocol.CATEGORY: ArduinoProtocol.STOP,
                ArduinoProtocol.MOTOR_INDEX: motor_index,
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
        self.send_serial({ArduinoProtocol.CATEGORY: ArduinoProtocol.BASKET_LED_ON}, port='/dev/factory')

    @on_event(filter={'category': 'basket_led_off'})
    def event_basket_led_off(self):
        logger.info("Turning basket led off")
        self.send_serial({ArduinoProtocol.CATEGORY: ArduinoProtocol.BASKET_LED_OFF}, port='/dev/factory')

    @on_event(filter={'category': 'basket_led_blink'})
    def event_basket_led_blink(self):
        logger.info("Blinking basket led (freq=1s)")
        self.send_serial({ArduinoProtocol.CATEGORY: ArduinoProtocol.BASKET_LED_BLINK}, port='/dev/factory')

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
        event = event.strip()  # Remove '\r'

        if event == "Grbl 1.1f ['$' for help]":
            # This message is sent after the serial port is connected
            pass
        elif event == "[MSG:Pgm End]":
            logger.info(f"Received {event}: command M30 must have been executed properly")
        elif event != "ok":
            logger.error("Unknown serial event '{}': skipping".format(event))
            return

        logger.info("Received ok from printer: processing next instruction")
        self.printer_gcode_instructions.pop(0)  # This instruction is the one being acknowledged by the 'ok'

        if not self.printer_gcode_instructions:
            logger.info("No more gcode instructions: going to idle state")
            return

        if self.printer_is_halted:
            logger.info("Printer is halted: waiting to resume")
            return

        next_instruction = self.printer_gcode_instructions[0]
        self.process_gcode_instruction(next_instruction)

    @on_event(filter={'category': 'printer_instruction'})
    def event_printer_instruction(self, instruction: str):
        self.process_gcode_instructions([instruction])

    @on_event(filter={'category': 'printer_instructions'})
    def event_printer_instructions(self, instructions: list):
        self.process_gcode_instructions(instructions)

    @on_event(filter={'category': 'print_pattern'})
    def event_print_pattern(self, pattern: str):
        instructions = copy(self.printer_patterns.get(pattern))
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
        if not self.printer_is_halted:
            logger.info("Printer is not halted: skipping")
            return

        self.printer_is_halted = False

        if not self.printer_gcode_instructions:
            logger.info("No more instructions: going to idle state")
            return

        next_instruction = self.printer_gcode_instructions[0]
        self.process_gcode_instruction(next_instruction)

    @on_event(filter={'category': 'printer_stop'})
    def event_printer_stop(self):
        self.printer_gcode_instructions = []

    @on_event(filter={'category': 'oven_turn_on'})
    def event_oven_turn_on(self):
        self.send_serial({ArduinoProtocol.CATEGORY: ArduinoProtocol.OVEN_TURN_ON}, '/dev/factory')

    @on_event(filter={'category': 'oven_turn_off'})
    def event_oven_turn_off(self):
        self.send_serial({ArduinoProtocol.CATEGORY: ArduinoProtocol.OVEN_TURN_OFF}, '/dev/factory')
