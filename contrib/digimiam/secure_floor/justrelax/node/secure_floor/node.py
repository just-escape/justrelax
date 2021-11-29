import time
import uuid

from twisted.internet import reactor

from gpiozero import OutputDevice, InputDevice

from justrelax.core.logging_utils import logger
from justrelax.core.node import MagicNode, on_event


class Cell:
    def __init__(self, sensor_id, pin, on_toggle, led_strip):
        self.sensor_id = sensor_id
        self.pin = pin
        self.device = InputDevice(pin)
        self.last_state = False

        self.on_toggle = on_toggle
        self.led_strip = led_strip

        reactor.callLater(0, self.check_myself)

    def check_myself(self):
        reactor.callLater(0, self.check_myself)

        is_activated = bool(self.device.value)
        if is_activated is self.last_state:
            return

        self.last_state = is_activated

        if is_activated:
            logger.info("Cell (pin={}, led_strip={}) has been activated".format(self.pin, self.led_strip))
            self.on_toggle(True, self.led_strip, self.sensor_id)
        else:
            logger.info("Cell (pin={}, led_strip={}) has been deactivated".format(self.pin, self.led_strip))
            self.on_toggle(False, self.led_strip, self.sensor_id)

    def calibrate(self):
        # Nothing to do here, this is just for interface purposes. A common pin to all cells has to be activated.
        pass

    def __bool__(self):
        return self.last_state

    def __str__(self):
        return str(self.pin)


class AMG88XX:
    def __init__(self, sensor_id, threshold, on_toggle, led_strip, clear_alarm_delay):
        self.sensor_id = sensor_id

        self.threshold = threshold

        self.last_state = False
        self.on_toggle = on_toggle
        self.led_strip = led_strip

        self.last_five_values = [0, 0, 0, 0, 0]

        self.watcher_task_delay = clear_alarm_delay
        self.watcher_task = None

    def force_deactivation(self):
        logger.info(f"AMG has not sent any values for {self.watcher_task_delay} seconds")
        if self.last_state is True:
            logger.warning("Forcing deactivation")
            self.last_state = False

            logger.info("AMG88XX (led_strip={}) has been deactivated".format(self.led_strip))
            self.on_toggle(False, self.led_strip, self.sensor_id)

    def new_max(self, value):
        if self.watcher_task and self.watcher_task.active():
            self.watcher_task.cancel()
        self.watcher_task = reactor.callLater(self.watcher_task_delay, self.force_deactivation)

        self.last_five_values.append(value)
        self.last_five_values = self.last_five_values[-5:]

        if len(self.last_five_values) == self.last_five_values.count(self.last_five_values[0]):
            logger.info(
                "AMG last five values max values are identical. There might be a connectivity issue.")
            if self.last_state is True:
                logger.warning("Forcing deactivation")
            is_activated = False
        else:
            is_activated = value > self.threshold

        if is_activated is self.last_state:
            return

        self.last_state = is_activated

        if is_activated:
            logger.info("AMG88XX (led_strip={}) has been activated".format(self.led_strip))
            self.on_toggle(True, self.led_strip, self.sensor_id)
        else:
            logger.info("AMG88XX (led_strip={}) has been deactivated".format(self.led_strip))
            self.on_toggle(False, self.led_strip, self.sensor_id)

    def __bool__(self):
        return self.last_state

    def __str__(self):
        return 'amg88xx'


class ArduinoProtocolFloor:
    CATEGORY = 'c'

    SET_COLOR_BLACK = 'b'
    SET_COLOR_ORANGE = 'o'
    SET_COLOR_RED = 'r'
    SET_COLOR_WHITE = 'w'
    SET_COLOR_WHITE_TO_RED = 'w2r'
    STRIP_BIT_MASK = 's'


class ArduinoProtocolAMG88XX:
    CATEGORY = "c"

    ERROR = "e"
    MAX = "m"

    CALIBRATE = "c"
    CALIBRATION_SAMPLES = "s"
    CALIBRATION_DELAY = "d"

    SET_ACQUISITION_PARAMS = "ap"
    ACQUISITION_SAMPLES = "as"
    ACQUISITION_DELAY = "ad"
    INTER_ACQUISITION_DELAY = "iad"


class SecureFloor(MagicNode):
    STATUSES = {'not_playing', 'playing', 'alarm'}

    def __init__(self, *args, **kwargs):
        super(SecureFloor, self).__init__(*args, **kwargs)

        self.status = 'not_playing'
        self.success = False

        self.clear_alarm_delay = self.config['clear_alarm_delay']
        self.clear_alarm_task = None

        self.calibration = OutputDevice(self.config['calibration_pin'])
        self.calibration.off()

        self.amg88xx = None
        self.leds = {}
        self.sensors = []
        self.toggle_tasks = {}
        for sensor in self.config['sensors']:
            sensor_id = str(uuid.uuid4())
            if sensor['type'] == 'load_cell':
                self.sensors.append(Cell(sensor_id, sensor['pin'], self.on_sensor_toggle, sensor['led_strip']))
            elif sensor['type'] == 'amg88xx':
                amg88xx = AMG88XX(
                    sensor_id, sensor['threshold'], self.on_sensor_toggle, sensor['led_strip'], self.clear_alarm_delay)
                self.sensors.append(amg88xx)
                self.amg88xx = amg88xx
            else:
                continue

            self.toggle_tasks[sensor_id] = None

            if sensor['led_strip']:
                self.leds[sensor['led_strip']] = 'black'

        # Init once we are sure the serial port will be able to receive data
        reactor.callLater(3, self.set_led_color, "black", sum(self.leds.keys()))

    def set_led_color(self, color, bit_mask):
        logger.info("Setting led bit_mask={} color={}".format(bit_mask, color))

        color_mapping = {
            'orange': ArduinoProtocolFloor.SET_COLOR_ORANGE,
            'red': ArduinoProtocolFloor.SET_COLOR_RED,
            'white': ArduinoProtocolFloor.SET_COLOR_WHITE,
            'white_to_red': ArduinoProtocolFloor.SET_COLOR_WHITE_TO_RED,
        }

        event_color = color_mapping.get(color, ArduinoProtocolFloor.SET_COLOR_BLACK)

        for led_index in self.leds.keys():
            if led_index & bit_mask:
                self.leds[led_index] = color

        self.send_serial(
            {
                ArduinoProtocolFloor.CATEGORY: event_color,
                ArduinoProtocolFloor.STRIP_BIT_MASK: bit_mask,
            },
            '/dev/floor'
        )

    @on_event(filter={'category': 'set_led_color'})
    def event_set_led_color(self, color: str, bit_mask: int):
        self.set_led_color(color, bit_mask)

    @on_event(filter={'category': 'set_all_leds_color'})
    def event_set_all_leds_color(self, color: str):
        self.set_led_color(color, sum(self.leds.keys()))

    @on_event(channel='/dev/amg88xx', filter={ArduinoProtocolAMG88XX.CATEGORY: ArduinoProtocolAMG88XX.MAX})
    def serial_event_amg88xx_new_matrix(self, m):
        self.amg88xx.new_max(m)

    @on_event(filter={'category': 'set_amg88xx_acquisition_params'})
    def event_set_acquisition_params(self, samples: int = 1, delay: int = 0, inter_acquisition_delay: int = 1000):
        logger.info(f"Setting acquisition params (samples={samples}), (delay={delay}), iad={inter_acquisition_delay}")
        self.send_serial(
            {
                ArduinoProtocolAMG88XX.CATEGORY: ArduinoProtocolAMG88XX.SET_ACQUISITION_PARAMS,
                ArduinoProtocolAMG88XX.ACQUISITION_SAMPLES: samples,
                ArduinoProtocolAMG88XX.ACQUISITION_DELAY: delay,
                ArduinoProtocolAMG88XX.INTER_ACQUISITION_DELAY: inter_acquisition_delay,
            },
            '/dev/amg88xx'
        )

    @on_event(filter={'category': 'calibrate'})
    def event_calibrate(self):
        logger.info("Calibration sensors")

        if self.amg88xx is not None:
            self.send_serial(
                {
                    ArduinoProtocolAMG88XX.CATEGORY: ArduinoProtocolAMG88XX.CALIBRATE,
                    ArduinoProtocolAMG88XX.CALIBRATION_SAMPLES: 10,
                    ArduinoProtocolAMG88XX.CALIBRATION_DELAY: 100,
                },
                '/dev/amg88xx'
            )

        logger.info("Triggering calibration rising edge...")
        self.calibration.on()

        # Blocking sleep (no reactor.callLater), because load cell pins will not behave deterministically during this
        # operation. It has not a huge impact on the whole system, and this way, in the hypothetical case in which
        # players toggle cells states (on/off), it should be transparent after the sleep.
        time.sleep(5)

        logger.info("Triggering calibration falling edge...")
        self.calibration.off()

    @on_event(filter={'category': 'reset'})
    def event_reset(self):
        logger.info("Resetting node")

        if self.clear_alarm_task and self.clear_alarm_task.active():
            self.clear_alarm_task.cancel()

        for _, task in self.toggle_tasks.items():
            if task and task.active():
                task.cancel()

        self.success = False
        self.event_calibrate()
        self.event_set_status('not_playing')

        # Should be handled by set_status, but we ensure it is done here because if status is already not_playing
        # it won't work
        self.event_set_led_color('black', sum(self.leds.keys()))

    @on_event(filter={'category': 'set_status'})
    def event_set_status(self, status: str):
        if self.success is False:
            if status in self.STATUSES:
                if self.status == status:
                    logger.info(f"Status is already {self.status} : skipping")
                    return

                if status == 'alarm':
                    self.event_set_led_color('red', sum(self.leds.keys()))

                    # If all sensors are deactivated while an alarm has been raised. This case should not happen because
                    # players are supposed to be walking on the floor to raise an alarm. But there might be corner cases
                    # where a player extends their hand, is on a cell with no load sensor or if this event has been
                    # triggered from the admin interface...
                    if all(not c for c in self.sensors):
                        self.clear_alarm_task = reactor.callLater(
                            self.clear_alarm_delay, self.event_set_status, "playing")

                elif status == 'playing':
                    if self.status == 'alarm':  # checking old status. If old status is not_playing, nothing to do
                        self.event_set_led_color('orange', sum(self.leds.keys()))
                        self.notify_clear()

                elif status == 'not_playing':
                    self.event_set_led_color('black', sum(self.leds.keys()))

                self.status = status
                logger.info("Status is now '{}'".format(status))

            else:
                logger.warning("Unknown status '{}': skipping".format(status))
        else:
            logger.warning("Node is in success mode: ignoring set status to '{}'".format(status))

    @on_event(filter={'category': 'forced_alarm'})
    def event_forced_alarm(self):
        self.event_set_all_leds_color('white_to_red')

    @on_event(filter={'category': 'success'})
    def event_success(self):
        if self.success is False:
            logger.info("Setting node in success mode")
            self.success = True
            self.event_set_all_leds_color('white')

    def notify_clear(self):
        self.publish({'category': 'clear'})

    def on_sensor_toggle(self, activated, led_strip, sensor_id):
        if self.success:
            return

        self.toggle_tasks[sensor_id] = reactor.callLater(0.5, self._on_sensor_toggle, activated, led_strip)

    def _on_sensor_toggle(self, activated, led_strip):
        if self.status == 'playing':
            if activated and led_strip and self.leds[led_strip] == 'black':
                self.event_set_led_color('orange', led_strip)

        if self.status == 'alarm':
            if activated:
                if self.clear_alarm_task and self.clear_alarm_task.active():
                    self.clear_alarm_task.cancel()
            else:
                if not self.clear_alarm_task or not self.clear_alarm_task.active():
                    if all(not c for c in self.sensors):  # If all sensors are deactivated
                        self.clear_alarm_task = reactor.callLater(
                            self.clear_alarm_delay, self.event_set_status, "playing")
