import os
from copy import copy, deepcopy

from twisted.internet import reactor

from justrelax.core.logging_utils import logger
from justrelax.core.node import MagicNode, on_event


class ArduinoProtocol:
    CATEGORY = "c"

    FORWARD = "f"
    BACKWARD = "b"
    GET_SWITCHES_INFO = "gsi"
    STEP_DELAY = "sd"
    MOTOR_INDEX = "i"
    N_PULSES = "n"
    LIMINARY_STEP_DELAY = "lsd"
    LIMINARY_N_PULSES = "ln"
    STOP = "stop"

    LIMIT_REACHED = "lrc"
    LIMIT_RELEASED = "lrl"
    LIMIT_REMAINING_STEPS = "lrs"
    MOVE_COMPLETED = "mc"

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
        for motor in self.motors.values():
            motor['event_callbacks'] = {
                'move_completed': {
                    'timeout': None,
                    'trigger': None,
                    'trigger_kwargs': {},
                },
                'limit_reached': {
                    'timeout': None,
                    'trigger': None,
                    'trigger_kwargs': {},
                },
                'limit_released': {
                    'timeout': None,
                    'trigger': None,
                    'trigger_kwargs': {},
                },
            }
        self.motor_default_step_delay = self.config['motor_default_step_delay']
        self.limit_switches = {
            # Default to True, as if the limit switch was pressed because
            # as long as we don't have the information we might as well prevent
            # any move
            'forward': {
                motor_id: (True if motor_params['forward_limit_switch'] else None)
                for motor_id, motor_params in self.motors.items()
            },
            'backward': {
                motor_id: (True if motor_params['backward_limit_switch'] else None)
                for motor_id, motor_params in self.motors.items()
            },
        }
        self.motors_error_mode = False

        self.light_led = self.config['light_led']

        self.printer_patterns = {}
        self.printer_is_halted = False
        self.printer_gcode_instructions = []
        self.printer_current_action = None
        self.printer_has_homing_been_run = False

        self.load_printer_patterns()

        self.animations = self.config['animations']
        self.animation_tasks = []

        reactor.callLater(3, self.event_reset)

    def on_first_connection(self):
        self.publish_session_data()

    @on_event(filter={'category': 'request_node_session_data'})
    def publish_session_data(self):
        self.publish_motors_error_mode()
        self.publish_motors_limit_switches()
        self.publish_printer_current_action()
        self.publish_printer_has_homing_been_run()

    def publish_motors_error_mode(self):
        self.publish(
            {
                'category': 'set_session_data',
                'key': 'waffle_factory_motors_error_mode',
                'data': self.motors_error_mode,
            }
        )

    def publish_motors_limit_switches(self):
        self.publish(
            {
                'category': 'set_session_data',
                'key': 'waffle_factory_motors_limit_switches',
                'data': self.limit_switches,
            }
        )

    def publish_printer_current_action(self):
        self.publish(
            {
                'category': 'set_session_data',
                'key': 'waffle_factory_printer_current_action',
                'data': self.printer_current_action,
            }
        )

    def publish_printer_has_homing_been_run(self):
        self.publish(
            {
                'category': 'set_session_data',
                'key': 'waffle_factory_printer_has_homing_been_run',
                'data': self.printer_has_homing_been_run,
            }
        )

    @on_event(filter={'category': 'ack_motors_error'})
    def event_ack_motors_error(self):
        self.motors_error_mode = False
        self.publish_motors_error_mode()

    def set_motors_error_mode(self, reason):
        logger.info(f"ERROR reason={reason}")
        self.motors_error_mode = True
        self.event_printer_stop()
        self.event_pause_animation()
        self.publish_motors_error_mode()

    def trigger_callback(
            self,
            motor_id, move_id, move_direction, initial_pulses,
            animation, event, detect_errors,
            **kwargs
    ):
        if detect_errors:
            if event == 'limit_released':
                if kwargs['direction'] == move_direction:
                    self.set_motors_error_mode(
                        reason=(
                            f"unexpected {kwargs['direction']} limit release "
                            f"during {move_direction} move (id={move_id})"
                        )
                    )
                    return

                limit_released_delta_pulses = initial_pulses - kwargs['remaining_pulses']
                max_delta = kwargs.get('max_delta_steps')
                if max_delta:
                    logger.info(f"DELTA = {limit_released_delta_pulses}/{max_delta}")
                    if limit_released_delta_pulses > max_delta:
                        self.set_motors_error_mode(
                            reason=(
                                f"delta pulses too high for limit_released {limit_released_delta_pulses} > {max_delta},"
                                f" move_id={move_id}"
                            )
                        )
                        return

            if event == 'limit_pressed' and kwargs['direction'] != move_direction:
                self.set_motors_error_mode(
                    reason=f"unexpected {kwargs['direction']} limit press during {move_direction} move (id={move_id})"
                )
                return

        # Actually used to cancel timeouts
        self.cancel_motor_callbacks(motor_id, only_event=event)

        if animation:
            self.event_play_animation(animation, detect_errors=detect_errors, check_timeout=False)

    def on_motor_event(self, motor_index, event, **kwargs):
        for motor_id, motor_params in self.motors.items():
            if motor_params['index'] == motor_index:
                if event == 'limit_reached':
                    # We should also check that motor_params[f"{kwargs['direction']}_limit_switch"] is True,
                    # but it will always be if configuration is synchronised
                    self.limit_switches[kwargs['direction']][motor_id] = True
                    self.publish_motors_limit_switches()
                elif event == 'limit_released':
                    # We should also check that motor_params[f"{kwargs['direction']}_limit_switch"] is True,
                    # but it will always be if configuration is synchronised
                    self.limit_switches[kwargs['direction']][motor_id] = False
                    self.publish_motors_limit_switches()

                trigger_cb = motor_params['event_callbacks'][event]['trigger']
                kwargs.update(motor_params['event_callbacks'][event]['trigger_kwargs'])

                if trigger_cb:
                    trigger_cb(
                        motor_id=motor_id,
                        **kwargs
                    )

                break

    @on_event(filter={ArduinoProtocol.CATEGORY: ArduinoProtocol.LIMIT_REACHED})
    def serial_event_limit_reached(self, i: int, ld: str, lrs: int):
        logger.info(f"Limit reached motor={i} dir={ld} hrs={lrs}")
        direction = 'forward' if ld == 'f' else 'backward'
        self.on_motor_event(i, 'limit_reached', direction=direction, remaining_pulses=lrs)

    @on_event(filter={ArduinoProtocol.CATEGORY: ArduinoProtocol.LIMIT_RELEASED})
    def serial_event_limit_released(self, i: int, ld: str, lrs: int):
        logger.info(f"Limit released motor={i} dir={ld} hrs={lrs}")
        direction = 'forward' if ld == 'f' else 'backward'
        self.on_motor_event(i, 'limit_released', direction=direction, remaining_pulses=lrs)

    @on_event(filter={ArduinoProtocol.CATEGORY: ArduinoProtocol.MOVE_COMPLETED})
    def serial_event_move_completed(self, i: int):
        logger.info(f"Move completed motor={i}")
        self.on_motor_event(i, 'move_completed')

    @on_event(filter={ArduinoProtocol.CATEGORY: ArduinoProtocol.GET_SWITCHES_INFO})
    def serial_event_get_switches_info(self, f: list, b: list):
        for motor_id, motor_params in self.motors.items():
            self.limit_switches['forward'][motor_id] = (
                f[motor_params['index']] if motor_params['forward_limit_switch'] else None)
            self.limit_switches['backward'][motor_id] = (
                b[motor_params['index']] if motor_params['backward_limit_switch'] else None)
        logger.info(f"limit_switches={self.limit_switches}")
        self.publish_motors_limit_switches()

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

    @on_event(filter={'category': 'get_switches_info'})
    def event_get_switches_info(self):
        self.send_serial(
            {
                ArduinoProtocol.CATEGORY: ArduinoProtocol.GET_SWITCHES_INFO,
            },
            port='/dev/factory',
        )

    @on_event(filter={'category': 'reset'})
    def event_reset(self):
        logger.info("Reset")
        self.event_basket_led_off()
        for light_led_id, light_led in self.light_led.items():
            if light_led['on_by_default']:
                self.event_light_on(light_led_id)
            else:
                self.event_light_off(light_led_id)
        self.event_get_switches_info()

    @on_event(filter={'category': 'play_animation'})
    def event_play_animation(self, animation: str, detect_errors: bool = True, check_timeout: bool = True):
        logger.info(f"Playing animation {animation}")

        if self.motors_error_mode:
            logger.error("Error mode: aborting")
            return

        for animation_task in self.animation_tasks:
            if animation_task and animation_task.active():
                logger.info("An animation is still going on: aborting")
                return

        if check_timeout:
            for motor_params in self.motors.values():
                for callbacks in motor_params['event_callbacks'].values():
                    if callbacks['timeout'] and callbacks['timeout'].active():
                        logger.info("An animation is still going on (because of a timeout): aborting")
                        return

        self.animation_tasks = []

        animation_instructions = self.animations.get(animation, None)
        if animation_instructions is None:
            logger.info(f"Animation {animation} not found: aborting")
            return

        for instruction_index, instruction_kwargs in enumerate(deepcopy(animation_instructions)):
            instruction_t = instruction_kwargs.pop('t')
            motor_id = instruction_kwargs.pop('motor')
            move_id = f"{animation}_{instruction_index}"
            self.animation_tasks.append(
                reactor.callLater(
                    instruction_t,
                    self.motor_move,
                    motor_id=motor_id,
                    detect_errors=detect_errors,
                    move_id=move_id,
                    **instruction_kwargs
                )
            )

    def cancel_motor_callbacks(self, motor_id, only_event=None):
        for callbacks_event, callbacks in self.motors[motor_id]['event_callbacks'].items():
            if only_event and only_event != callbacks_event:
                continue

            if callbacks['timeout'] and callbacks['timeout'].active():
                callbacks['timeout'].cancel()

            callbacks['trigger'] = None
            callbacks['trigger_kwargs'] = {}

    @on_event(filter={'category': 'pause_animation'})
    def event_pause_animation(self):
        logger.info("Stopping animation: stopping all motors and canceling all animation tasks")
        for motor_id, motor_params in self.motors.items():
            self.event_motor_stop(motor_id)
            self.cancel_motor_callbacks(motor_id)

        for animation_task in self.animation_tasks:
            if animation_task and animation_task.active():
                animation_task.cancel()
        self.animation_tasks = []

    @on_event(filter={'category': 'motor_move'})
    def motor_move(
            self, motor_id: str, direction: str, n_pulses: int, step_delay: int = None,
            liminary_n_pulses: int = 0, liminary_step_delay: int = None,
            move_id: str = None,
            callbacks: dict = None,
            detect_errors: bool = False,
    ):
        logger.info(f"Turning motor {motor_id} {direction} (move_id={move_id}, callbacks={callbacks})")

        if self.motors_error_mode:
            logger.error("Error mode: aborting")
            return

        motor_index = self.motors[motor_id]['index']
        step_delay = step_delay if step_delay is not None else self.motor_default_step_delay
        liminary_step_delay = liminary_step_delay if liminary_step_delay is not None else self.motor_default_step_delay

        logger.info("Step delay={}".format(step_delay))

        self.send_serial(
            {
                ArduinoProtocol.CATEGORY: (
                    ArduinoProtocol.FORWARD if direction == 'forward' else ArduinoProtocol.BACKWARD
                ),
                ArduinoProtocol.MOTOR_INDEX: motor_index,
                ArduinoProtocol.N_PULSES: n_pulses,
                ArduinoProtocol.STEP_DELAY: step_delay,
                ArduinoProtocol.LIMINARY_STEP_DELAY: liminary_step_delay,
                ArduinoProtocol.LIMINARY_N_PULSES: liminary_n_pulses,
            },
            port='/dev/factory',
        )

        self.cancel_motor_callbacks(motor_id)

        _callbacks = callbacks or {}
        for event in ('move_completed', 'limit_reached', 'limit_released',):
            if event not in _callbacks:
                continue

            if detect_errors:
                timeout_t = _callbacks[event].get('timeout')
                if timeout_t is not None:
                    self.motors[motor_id]['event_callbacks'][event]['timeout'] = reactor.callLater(
                        timeout_t, self.set_motors_error_mode, reason=f"timeout {move_id} {event} after {timeout_t}s")

            trigger_animation_name = _callbacks[event].get('trigger')
            self.motors[motor_id]['event_callbacks'][event]['trigger'] = self.trigger_callback
            self.motors[motor_id]['event_callbacks'][event]['trigger_kwargs'] = {
                'move_id': move_id,
                'move_direction': direction,
                'initial_pulses': n_pulses + 2 * liminary_n_pulses,
                'max_delta_steps': _callbacks[event].get('max_delta_steps'),
                'animation': trigger_animation_name,
                'event': event,
                'detect_errors': detect_errors,
            }

    @on_event(filter={'category': 'motor_forward'})
    def event_motor_forward(
            self, motor_id: str, n_pulses: int, step_delay: int = None,
            liminary_n_pulses: int = 0, liminary_step_delay: int = None,
    ):
        self.motor_move(motor_id, 'forward', n_pulses, step_delay, liminary_n_pulses, liminary_step_delay)

    @on_event(filter={'category': 'motor_backward'})
    def event_motor_backward(
            self, motor_id: str, n_pulses: int, step_delay: int = None,
            liminary_n_pulses: int = 0, liminary_step_delay: int = None,
    ):
        self.motor_move(motor_id, 'backward', n_pulses, step_delay, liminary_n_pulses, liminary_step_delay)

    @on_event(filter={'category': 'motor_stop'})
    def event_motor_stop(self, motor_id: str):
        logger.info("Stopping motor {}".format(motor_id))
        motor_index = self.motors[motor_id]['index']
        self.send_serial(
            {
                ArduinoProtocol.CATEGORY: ArduinoProtocol.STOP,
                ArduinoProtocol.MOTOR_INDEX: motor_index,
            },
            port='/dev/factory',
        )
        self.cancel_motor_callbacks(motor_id)

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

        if self.motors_error_mode:
            logger.error("Error mode: aborting")
            self.event_printer_stop()
            return

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
            return
        elif event == "[MSG:Caution: Unlocked]":
            return
        elif event == "[MSG:'$H'|'$X' to unlock]":
            logger.info(f"Received {event} from printer: unlocking")
            self.process_gcode_instructions(['$X'])
            return
        elif event == "ALARM:1":
            return
        elif event == "[MSG:Reset to continue]":
            logger.info(f"Received {event} from printer: resetting")
            self.process_gcode_instruction((24).to_bytes(2, byteorder='big').decode())
            return
        elif event == "[MSG:Pgm End]":
            logger.info(f"Received {event}: command M30 must have been executed properly")
        elif event == "ok":
            logger.info(f"Received {event} from printer: processing next instruction")
        elif event == '':
            return
        else:
            logger.error(f"Unknown serial event '{event}': skipping")
            return

        if not self.printer_gcode_instructions:
            self.printer_current_action = None
            self.publish_printer_current_action()
            return

        self.printer_gcode_instructions.pop(0)  # This instruction is the one being acknowledged by the 'ok'

        if not self.printer_gcode_instructions:
            logger.info("No more gcode instructions: going to idle state")
            self.printer_current_action = None
            self.publish_printer_current_action()
            return

        if self.printer_is_halted:
            logger.info("Printer is halted: waiting to resume")
            return

        next_instruction = self.printer_gcode_instructions[0]
        self.process_gcode_instruction(next_instruction)

    @on_event(filter={'category': 'printer_instruction'})
    def event_printer_instruction(self, instruction: str):
        self.printer_current_action = 'unknown_pattern'
        self.publish_printer_current_action()
        self.process_gcode_instructions([instruction])

    @on_event(filter={'category': 'printer_instructions'})
    def event_printer_instructions(self, instructions: list):
        self.printer_current_action = 'unknown_pattern'
        self.publish_printer_current_action()
        self.process_gcode_instructions(instructions)

    @on_event(filter={'category': 'print_pattern'})
    def event_print_pattern(self, pattern: str):
        instructions = copy(self.printer_patterns.get(pattern))
        if instructions is None:
            logger.info("Unknown pattern '{}'. It must be one of {}: ignoring".format(
                pattern, ",".join(self.printer_patterns)))
            return

        self.printer_current_action = pattern
        self.publish_printer_current_action()
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

    @on_event(filter={'category': 'printer_homing'})
    def event_printer_homing(self, purge: bool = False):
        if self.printer_has_homing_been_run:
            return

        # Note: quick and dirty, because there is no lock
        self.printer_current_action = 'homing'
        self.publish_printer_current_action()
        for instruction in self.config['printer_homing_sequence']:
            reactor.callLater(instruction['t'], self.process_gcode_instruction, instruction['gcode'])

        self.printer_has_homing_been_run = True
        self.publish_printer_has_homing_been_run()

        if purge:
            reactor.callLater(instruction['t'] + 5, self.event_print_pattern, 'purge')
        else:
            def set_printer_current_action_none():
                self.printer_current_action = None
                self.publish_printer_current_action()

            reactor.callLater(instruction['t'], set_printer_current_action_none)

    @on_event(filter={'category': 'printer_stop'})
    def event_printer_stop(self):
        self.printer_gcode_instructions = []

    @on_event(filter={'category': 'oven_turn_on'})
    def event_oven_turn_on(self):
        self.send_serial({ArduinoProtocol.CATEGORY: ArduinoProtocol.OVEN_TURN_ON}, '/dev/factory')

    @on_event(filter={'category': 'oven_turn_off'})
    def event_oven_turn_off(self):
        self.send_serial({ArduinoProtocol.CATEGORY: ArduinoProtocol.OVEN_TURN_OFF}, '/dev/factory')
