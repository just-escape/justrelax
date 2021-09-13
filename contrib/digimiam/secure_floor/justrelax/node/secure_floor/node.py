import time
import uuid
import copy

from twisted.internet import reactor

import busio
import board
import adafruit_amg88xx
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
    def __init__(self, sensor_id, threshold, on_toggle, led_strip):
        self.sensor_id = sensor_id

        self.threshold = threshold
        i2c_bus = busio.I2C(board.SCL, board.SDA)
        self.sensor = adafruit_amg88xx.AMG88XX(i2c_bus)

        self.last_state = False
        self.on_toggle = on_toggle
        self.led_strip = led_strip

        # The initial calibration matrix has 100°C in all cells because room temperature will never be that hot
        # So, before any manual calibration is performed, the computed differential matrix will never trigger any
        # activation.
        self.calibration_matrix = [[100] * 8] * 8
        self.calibration_task = None

        reactor.callLater(0, self.check_myself)

    def check_myself(self):
        reactor.callLater(1, self.check_myself)

        if self.calibration_task and self.calibration_task.active():
            # Nothing to do while calibration is ongoing
            return

        try:
            snapped_matrix = self.sensor.pixels
        except Exception:
            return

        differential_matrix = [[0] * 8] * 8
        for x in range(0, 8):
            for y in range(0, 8):
                differential_matrix[x][y] = snapped_matrix[x][y] - self.calibration_matrix[x][y]

        max_value = max(max(v) for v in differential_matrix)

        is_activated = max_value > self.threshold
        if is_activated is self.last_state:
            return

        logger.debug(f"Differential matrix is {differential_matrix}")
        logger.debug(f"Max value is {max_value}")

        self.last_state = is_activated

        if is_activated:
            logger.info("AMG88XX (led_strip={}) has been activated".format(self.led_strip))
            self.on_toggle(True, self.led_strip, self.sensor_id)
        else:
            logger.info("AMG88XX (led_strip={}) has been deactivated".format(self.led_strip))
            self.on_toggle(False, self.led_strip, self.sensor_id)

    def calibrate(self):
        if self.calibration_task and self.calibration_task.active():
            self.calibration_task.cancel()

        self._calibrate(additive_matrix=[[0] * 8] * 8)

    def _calibrate(self, additive_matrix, remaining_samples=10):
        try:
            snapped_matrix = self.sensor.pixels
        except Exception:
            logger.warning("Unable to snap pixels: skipping this calibration read", exc_info=True)
            self.calibration_task = reactor.callLater(
                1, self._calibrate, additive_matrix, remaining_samples=remaining_samples)
            return

        logger.debug(f"Snapping a calibration matrix {snapped_matrix}")

        new_additive_matrix = [[0] * 8] * 8
        for x in range(0, 8):
            for y in range(0, 8):
                new_additive_matrix[x][y] = additive_matrix[x][y] + snapped_matrix[x][y]
        logger.debug(f"Additive matrix is now {new_additive_matrix}")

        remaining_samples -= 1
        if remaining_samples > 0:
            self.calibration_task = reactor.callLater(
                1, self._calibrate, new_additive_matrix, remaining_samples=remaining_samples)
        else:
            calibration_matrix = [[0] * 8] * 8
            for x in range(0, 8):
                for y in range(0, 8):
                    calibration_matrix[x][y] = new_additive_matrix[x][y] / 10

            self.calibration_matrix = calibration_matrix
            logger.debug(f"Calibration matrix is now {self.calibration_matrix}")

    def __bool__(self):
        return self.last_state

    def __str__(self):
        return 'amg88xx'


class ArduinoProtocol:
    CATEGORY = 'c'

    SET_COLOR_BLACK = 'b'
    SET_COLOR_ORANGE = 'o'
    SET_COLOR_RED = 'r'
    SET_COLOR_WHITE = 'w'
    STRIP_BIT_MASK = 's'


class SecureFloor(MagicNode):
    STATUSES = {'playing', 'alarm'}

    def __init__(self, *args, **kwargs):
        super(SecureFloor, self).__init__(*args, **kwargs)

        self.status = 'playing'
        self.success = False

        self.clear_alarm_delay = self.config['clear_alarm_delay']
        self.clear_alarm_task = None

        self.calibration = OutputDevice(self.config['calibration_pin'])
        self.calibration.off()

        self.leds = {}
        self.sensors = []
        self.toggle_tasks = {}
        for sensor in self.config['sensors']:
            sensor_id = str(uuid.uuid4())
            if sensor['type'] == 'load_cell':
                self.sensors.append(Cell(sensor_id, sensor['pin'], self.on_sensor_toggle, sensor['led_strip']))
            elif sensor['type'] == 'amg88xx':
                amg88xx = AMG88XX(sensor_id, sensor['threshold'], self.on_sensor_toggle, sensor['led_strip'])
                reactor.callLater(5, amg88xx.calibrate)  # Let AMG88XX the time to initialize
                self.sensors.append(amg88xx)
            else:
                continue

            self.toggle_tasks[sensor_id] = None

            if sensor['led_strip']:
                self.leds[sensor['led_strip']] = 'black'

        self.sleep_mode_task = None

        # Init once we are sure the serial port will be able to receive data
        reactor.callLater(3, self.set_led_color, "black", sum(self.leds.keys()))

    def set_led_color(self, color, bit_mask):
        logger.info("Setting led bit_mask={} color={}".format(bit_mask, color))

        color_mapping = {
            'orange': ArduinoProtocol.SET_COLOR_ORANGE,
            'red': ArduinoProtocol.SET_COLOR_RED,
            'white': ArduinoProtocol.SET_COLOR_WHITE,
        }

        event_color = color_mapping.get(color, ArduinoProtocol.SET_COLOR_BLACK)

        for led_index in self.leds.keys():
            if led_index & bit_mask:
                self.leds[led_index] = color

        self.send_serial({
            ArduinoProtocol.CATEGORY: event_color,
            ArduinoProtocol.STRIP_BIT_MASK: bit_mask,
        })

    def sleep_mode(self):
        logger.info("900 seconds with no activity detected: turning off led")
        self.event_set_all_leds_color('black')

    @on_event(filter={'category': 'set_led_color'})
    def event_set_led_color(self, color: str, bit_mask: int):
        self.set_led_color(color, bit_mask)

        if self.sleep_mode_task and self.sleep_mode_task.active():
            self.sleep_mode_task.cancel()

        if color != 'black':
            self.sleep_mode_task = reactor.callLater(900, self.sleep_mode)

    @on_event(filter={'category': 'set_all_leds_color'})
    def event_set_all_leds_color(self, color: str):
        self.set_led_color(color, sum(self.leds.keys()))

    @on_event(filter={'category': 'calibrate'})
    def event_calibrate(self):
        logger.info("Calibration sensors")
        for sensor in self.sensors:
            sensor.calibrate()

        logger.info("Triggering calibration rising edge...")
        self.calibration.on()

        # Blocking sleep (no reactor.callLater), because load cell pins will not behave deterministically during this
        # operation. It has not a huge impact on the whole system, and this way, in the hypothetical case in which
        # players toggle cells states (on/off), it should be transparent after the sleep.
        time.sleep(0.5)

        logger.info("Triggering calibration falling edge...")
        self.calibration.off()

    @on_event(filter={'category': 'reset'})
    def event_reset(self):
        logger.info("Resetting node")

        if self.clear_alarm_task and self.clear_alarm_task.active():
            self.clear_alarm_task.cancel()

        if self.sleep_mode_task and self.sleep_mode_task.active():
            self.sleep_mode_task.cancel()

        for _, task in self.toggle_tasks.items():
            if task and task.active():
                task.cancel()

        self.success = False
        self.set_led_color("black", sum(self.leds.keys()))
        self.event_calibrate()
        self.event_set_status('playing')

    @on_event(filter={'category': 'set_status'})
    def event_set_status(self, status: str):
        if self.success is False:
            if status in self.STATUSES:
                if self.status == status:
                    logger.info(f"Status is already {self.status} : skipping")
                    return

                logger.info("Setting status to '{}'".format(status))
                self.status = status
                if status == 'alarm':
                    self.event_set_led_color(
                        'red',
                        sum(led_strip for led_strip, led_color in self.leds.items() if led_color != 'black'))

                    # If all sensors are deactivated while an alarm has been raised. This case should not happen because
                    # players are supposed to be walking on the floor to raise an alarm. But there might be corner cases
                    # where a player extends their hand, is on a cell with no load sensor or if this event has been
                    # triggered from the admin interface...
                    if all(not c for c in self.sensors):
                        self.clear_alarm_task = reactor.callLater(
                            self.clear_alarm_delay, self.event_set_status, "playing")

                elif status == 'playing':
                    self.event_set_led_color(
                        'orange',
                        sum(led_strip for led_strip, led_color in self.leds.items() if led_color != 'black'))
                    self.notify_clear()

            else:
                logger.warning("Unknown status '{}': skipping".format(status))
        else:
            logger.warning("Node is in success mode: ignoring set status to '{}'".format(status))

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
        if self.sleep_mode_task and self.sleep_mode_task.active():
            self.sleep_mode_task.cancel()

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
