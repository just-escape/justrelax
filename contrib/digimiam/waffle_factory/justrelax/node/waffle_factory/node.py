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
    LED_FREQ_VALUE = "v"
    LED_FREQ_STEP = "s"


class WaffleFactory(MagicNode):
    def __init__(self, *args, **kwargs):
        super(WaffleFactory, self).__init__(*args, **kwargs)

        self.conveyors = self.config['conveyors']
        self.servos = self.config['servos']
        self.conveyor_default_clock_period = self.config['conveyor_default_clock_period']

        reactor.callLater(3, self.event_reset)

    @on_event(filter={'category': 'reset'})
    def event_reset(self):
        logger.info("Reset")
        if self.config['led_on_by_default']:
            self.event_led_on()
        else:
            self.event_led_off()

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
            }
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
            }
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
            }
        )

    @on_event(filter={'category': 'conveyor_stop'})
    def event_stop_conveyor(self, conveyor_id: str):
        logger.info("Stopping conveyor {})".format(conveyor_id))
        self.event_conveyor_set_clock(conveyor_id, 0, 0)

    @on_event(filter={'category': 'pull_servo'})
    def event_pull_servo(self, servo_id: str):
        logger.info("Pulling servo {}".format(servo_id))
        pull_position = self.servos[servo_id]['pull']
        self.set_servo_position(servo_id, pull_position)

    @on_event(filter={'category': 'push_servo'})
    def event_push_servo(self, servo_id: str):
        logger.info("Pushing servo {}".format(servo_id))
        push_position = self.servos[servo_id]['push']
        self.set_servo_position(servo_id, push_position)

    @on_event(filter={'category': 'move_servo'})
    def event_move_servo(self, servo_id: str, position: int):
        logger.info("Setting servo {} position to {}".format(servo_id, position))

        servo_index = self.servos[servo_id]['index']

        self.send_serial(
            {
                ArduinoProtocol.CATEGORY: ArduinoProtocol.MOVE_SERVO,
                ArduinoProtocol.SERVO_INDEX: servo_index,
                ArduinoProtocol.SERVO_POSITION: position,
            }
        )

    @on_event(filter={'category': 'led_on'})
    def event_led_on(self):
        logger.info("Led on")
        self.event_led_set_target_freq(50.)

    @on_event(filter={'category': 'led_off'})
    def event_led_off(self):
        logger.info("Led off")
        self.event_led_set_freq(0.)

    @on_event(filter={'category': 'led_set_freq'})
    def event_led_set_freq(self, value: float):
        value = min(value, 50.)
        logger.info("Set lights freq to {}/50".format(value))
        self.send_serial(
            {
                ArduinoProtocol.CATEGORY: ArduinoProtocol.SET_LED_FREQ,
                ArduinoProtocol.LED_FREQ_VALUE: value,
            }
        )

    @on_event(filter={'category': 'led_set_target_freq'})
    def event_led_set_target_freq(self, value: float, step: float = 0.2):
        value = min(value, 50.)
        logger.info("Set lights freq to {}/50 with a step of {}".format(value, step))
        self.send_serial(
            {
                ArduinoProtocol.CATEGORY: ArduinoProtocol.SET_LED_TARGET_FREQ,
                ArduinoProtocol.LED_FREQ_VALUE: value,
                ArduinoProtocol.LED_FREQ_STEP: step,
            }
        )
