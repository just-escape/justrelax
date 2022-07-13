from copy import deepcopy

from twisted.internet import reactor

from justrelax.core.logging_utils import logger
from justrelax.core.node import MagicNode, on_event


class ArduinoProtocol:
    CATEGORY = "c"

    ERROR = "e"

    PING = "p"
    MOVE = "m"
    DXL_INDEX = "i"

    REBOOT = "r"
    GET_POSITION = "gp"
    SET_PROFILE_VELOCITY = "spv"
    VELOCITY = "v"
    VALUE = "val"
    TORQUE_OFF = "toff"
    TORQUE_ON = "ton"
    LAST_LIB_ERR_CODE = "llec"

    TO = "to"
    FROM = "fr"

    DXL_RADIUS_WRIST = "dxl_radius_wrist"
    DXL_THUMB = "dxl_thumb"

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

    ELECTROMAGNET = "e"
    MAGNETIZE = "m"


class Niryo(MagicNode):
    def __init__(self, *args, **kwargs):
        super(Niryo, self).__init__(*args, **kwargs)

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
        self.dynamixels = self.config['dynamixels']

        self.animations = self.config['animations']
        self.animation_tasks = []

        reactor.callLater(3, self.init_arduino)

    def on_first_connection(self):
        self.publish_session_data()

    @on_event(filter={'category': 'request_node_session_data'})
    def publish_session_data(self):
        self.publish_motors_error_mode()
        self.publish_motors_limit_switches()

    def publish_motors_error_mode(self):
        self.publish(
            {
                'category': 'set_session_data',
                'key': 'niryo_motors_error_mode',
                'data': self.motors_error_mode,
            }
        )

    def publish_motors_limit_switches(self):
        self.publish(
            {
                'category': 'set_session_data',
                'key': 'niryo_motors_limit_switches',
                'data': self.limit_switches,
            }
        )

    @on_event(filter={'category': 'ack_motors_error'})
    def event_ack_motors_error(self):
        self.motors_error_mode = False
        self.publish_motors_error_mode()

    def set_motors_error_mode(self, reason):
        logger.info(f"ERROR reason={reason}")
        self.motors_error_mode = True
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

    def init_arduino(self):
        self.event_electromagnet(False)
        self.event_get_switches_info()

    @on_event(filter={'category': 'get_switches_info'})
    def event_get_switches_info(self):
        self.send_serial(
            {
                ArduinoProtocol.CATEGORY: ArduinoProtocol.GET_SWITCHES_INFO,
            },
        )

    @on_event(filter={'category': 'reset'})
    def event_reset(self):
        self.init_arduino()

    @on_event(filter={'category': 'electromagnet'})
    def event_electromagnet(self, magnetize: bool):
        self.send_serial({
            ArduinoProtocol.CATEGORY: ArduinoProtocol.ELECTROMAGNET,
            ArduinoProtocol.MAGNETIZE: magnetize,
        })
        for dxl_index, dxl_id in enumerate(self.dynamixels):
            reactor.callLater(
                dxl_index + 1, self.event_dxl_set_profile_velocity, dxl_id, self.dynamixels[dxl_id]['velocity'])

    @on_event(filter={'category': 'dxl_torque_on'})
    def event_dxl_torque_on(self, dxl_id: str):
        dxl_index = self.dynamixels[dxl_id]["index"]
        dxl_to = self.dynamixels[dxl_id]["to"]
        self.send_serial({
            ArduinoProtocol.CATEGORY: ArduinoProtocol.TORQUE_ON,
            ArduinoProtocol.TO: dxl_to,
            ArduinoProtocol.DXL_INDEX: dxl_index,
        })

    @on_event(filter={'category': 'dxl_torque_off'})
    def event_dxl_torque_off(self, dxl_id: str):
        dxl_index = self.dynamixels[dxl_id]["index"]
        dxl_to = self.dynamixels[dxl_id]["to"]
        self.send_serial({
            ArduinoProtocol.CATEGORY: ArduinoProtocol.TORQUE_OFF,
            ArduinoProtocol.TO: dxl_to,
            ArduinoProtocol.DXL_INDEX: dxl_index,
        })

    @on_event(filter={'category': 'dxl_get_position'})
    def event_dxl_get_position(self, dxl_id: str):
        dxl_index = self.dynamixels[dxl_id]["index"]
        dxl_to = self.dynamixels[dxl_id]["to"]
        self.send_serial({
            ArduinoProtocol.CATEGORY: ArduinoProtocol.GET_POSITION,
            ArduinoProtocol.TO: dxl_to,
            ArduinoProtocol.DXL_INDEX: dxl_index,
        })

    @on_event(filter={'category': 'dxl_set_profile_velocity'})
    def event_dxl_set_profile_velocity(self, dxl_id: str, velocity: int):
        dxl_index = self.dynamixels[dxl_id]["index"]
        dxl_to = self.dynamixels[dxl_id]["to"]
        self.send_serial({
            ArduinoProtocol.CATEGORY: ArduinoProtocol.SET_PROFILE_VELOCITY,
            ArduinoProtocol.TO: dxl_to,
            ArduinoProtocol.DXL_INDEX: dxl_index,
            ArduinoProtocol.VELOCITY: velocity,
        })

    @on_event(filter={'category': 'dxl_reboot'})
    def event_dxl_reboot(self, dxl_id: str):
        dxl_index = self.dynamixels[dxl_id]["index"]
        dxl_to = self.dynamixels[dxl_id]["to"]
        self.send_serial({
            ArduinoProtocol.CATEGORY: ArduinoProtocol.REBOOT,
            ArduinoProtocol.TO: dxl_to,
            ArduinoProtocol.DXL_INDEX: dxl_index,
        })

    @on_event(filter={ArduinoProtocol.FROM: ArduinoProtocol.DXL_RADIUS_WRIST})
    def event_dxl_radius_wrist_response(self, llec: int):
        if llec != 0:
            logger.error("LLEC!=0")

    @on_event(filter={ArduinoProtocol.FROM: ArduinoProtocol.DXL_THUMB})
    def event_dxl_thumb_response(self, llec: int):
        if llec != 0:
            logger.error("LLEC!=0")

    @on_event(filter={'category': 'dxl_move'})
    def event_dxl_move(self, dxl_id: str, position: int):
        dxl_index = self.dynamixels[dxl_id]["index"]
        dxl_to = self.dynamixels[dxl_id]["to"]
        self.send_serial({
            ArduinoProtocol.CATEGORY: ArduinoProtocol.MOVE,
            ArduinoProtocol.TO: dxl_to,
            ArduinoProtocol.DXL_INDEX: dxl_index,
            ArduinoProtocol.VALUE: position,
        })

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
        logger.info(f"Stopping motor {motor_id}")
        motor_index = self.motors[motor_id]['index']
        self.send_serial({
            ArduinoProtocol.CATEGORY: ArduinoProtocol.STOP,
            ArduinoProtocol.MOTOR_INDEX: motor_index,
        })
        self.cancel_motor_callbacks(motor_id)

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

            if 'motor' in instruction_kwargs:
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

            elif 'dynamixel' in instruction_kwargs:
                self.animation_tasks.append(reactor.callLater(
                    instruction_t, self.event_dxl_move,
                    dxl_id=instruction_kwargs['dynamixel'], position=instruction_kwargs['position']))

            elif 'electromagnet' in instruction_kwargs:
                self.animation_tasks.append(reactor.callLater(
                    instruction_t, self.event_electromagnet, magnetize=instruction_kwargs['electromagnet']))

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
