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

    HOMING = "h"
    FORWARD = "f"
    BACKWARD = "b"
    STEP_DELAY = "sd"
    MOTOR_INDEX = "i"
    N_PULSES = "n"
    LIMINARY_STEP_DELAY = "lsd"
    LIMINARY_N_PULSES = "ln"
    STOP = "stop"

    ELECTROMAGNET = "e"
    MAGNETIZE = "m"


class Niryo(MagicNode):
    def __init__(self, *args, **kwargs):
        super(Niryo, self).__init__(*args, **kwargs)

        self.motors = self.config['motors']
        self.motor_default_step_delay = self.config['motor_default_step_delay']
        self.dynamixels = self.config['dynamixels']

        self.animations = self.config['animations']
        self.animation_tasks = []

        reactor.callLater(3, self.init_arduino)

    def init_arduino(self):
        self.event_electromagnet(False)

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

        self.send_serial({
            ArduinoProtocol.CATEGORY: ArduinoProtocol.HOMING,
            ArduinoProtocol.MOTOR_INDEX: motor_index,
            ArduinoProtocol.N_PULSES: n_pulses,
            ArduinoProtocol.STEP_DELAY: step_delay,
            ArduinoProtocol.LIMINARY_STEP_DELAY: liminary_step_delay,
            ArduinoProtocol.LIMINARY_N_PULSES: liminary_n_pulses,
        })

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

        self.send_serial({
            ArduinoProtocol.CATEGORY: ArduinoProtocol.FORWARD,
            ArduinoProtocol.MOTOR_INDEX: motor_index,
            ArduinoProtocol.N_PULSES: n_pulses,
            ArduinoProtocol.STEP_DELAY: step_delay,
            ArduinoProtocol.LIMINARY_STEP_DELAY: liminary_step_delay,
            ArduinoProtocol.LIMINARY_N_PULSES: liminary_n_pulses,
        })

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

        self.send_serial({
            ArduinoProtocol.CATEGORY: ArduinoProtocol.BACKWARD,
            ArduinoProtocol.MOTOR_INDEX: motor_index,
            ArduinoProtocol.N_PULSES: n_pulses,
            ArduinoProtocol.STEP_DELAY: step_delay,
            ArduinoProtocol.LIMINARY_STEP_DELAY: liminary_step_delay,
            ArduinoProtocol.LIMINARY_N_PULSES: liminary_n_pulses,
        })

    @on_event(filter={'category': 'motor_stop'})
    def event_motor_stop(self, motor_id: str):
        logger.info(f"Stopping motor {motor_id}")
        motor_index = self.motors[motor_id]['index']
        self.send_serial({
            ArduinoProtocol.CATEGORY: ArduinoProtocol.STOP,
            ArduinoProtocol.MOTOR_INDEX: motor_index,
        })

    @on_event(filter={'category': 'play_animation'})
    def event_play_animation(self, animation: str):
        logger.info(f"Playing animation {animation}")

        for animation_task in self.animation_tasks:
            if animation_task and animation_task.active():
                logger.info("An animation is still going on: aborting")
                return
        self.animation_tasks = []

        animation_instructions = self.animations.get(animation, None)
        if animation_instructions is None:
            logger.info(f"Animation {animation} not found: aborting")
            return

        motor_direction_name_to_function_mapping = {
            'forward': self.event_motor_forward,
            'backward': self.event_motor_backward,
            'homing': self.event_motor_homing,
        }

        for instruction_kwargs in deepcopy(animation_instructions):
            instruction_t = instruction_kwargs.pop('t')

            if 'motor' in instruction_kwargs:
                direction = instruction_kwargs.pop('direction')
                motor_id = instruction_kwargs.pop('motor')
                function = motor_direction_name_to_function_mapping.get(direction, None)
                if function is None:
                    logger.warning(f"Unknown direction {direction}: ignoring")
                    continue

                self.animation_tasks.append(reactor.callLater(
                    instruction_t, function, motor_id=motor_id, **instruction_kwargs))

            elif 'dynamixel' in instruction_kwargs:
                self.animation_tasks.append(reactor.callLater(
                    instruction_t, self.event_dxl_move,
                    dxl_id=instruction_kwargs['dynamixel'], position=instruction_kwargs['position']))

            elif 'electromagnet' in instruction_kwargs:
                self.animation_tasks.append(reactor.callLater(
                    instruction_t, self.event_electromagnet, magnetize=instruction_kwargs['electromagnet']))

    @on_event(filter={'category': 'pause_animation'})
    def event_pause_animation(self):
        logger.info("Stopping animation: stopping all motors and canceling all animation tasks")
        for motor_id in self.motors:
            self.event_motor_stop(motor_id)

        for animation_task in self.animation_tasks:
            if animation_task and animation_task.active():
                animation_task.cancel()
        self.animation_tasks = []
