from twisted.internet import reactor

from justrelax.core.logging_utils import logger
from justrelax.core.node import MagicNode, on_event


class ArduinoProtocol:
    CATEGORY = "c"

    ERROR = "e"
    ALARM = "a"
    ALARM_LASER_INDEX = "i"

    LASER_ON = "l"
    LASER_ON_BITMASK = "b"
    DYNAMIC_LASER_ON_BITMASK = "d"
    DYNAMIC_LASER_UPTIME = "p"
    DYNAMIC_LASER_DOWNTIME = "n"
    DYNAMIC_LASER_INCREMENTAL_OFFSET = "o"
    SAMPLE_DELAY = "y"
    STOP_PLAYING = "s"
    SET_SUCCESS = "w"
    SET_SUCCESS_VALUE = "v"
    SET_SAMPLE_DELAY = "ssd"


class LaserMaze(MagicNode):
    STATUSES = {'not_playing', 'playing', 'success', 'auto_control'}

    def __init__(self, *args, **kwargs):
        super(LaserMaze, self).__init__(*args, **kwargs)

        self.status = 'not_playing'

        self.laser_prefix = self.config['laser_prefix']

        self.check_sensors_delay_default = self.config['check_sensors_delay']
        self.check_sensors_delay = self.check_sensors_delay_default

        self.failures_to_auto_deactivate_min = self.config['failures_to_auto_deactivate']['min']
        self.failures_to_auto_deactivate_default = self.config['failures_to_auto_deactivate']['default']
        self.failures_to_auto_deactivate_max = self.config['failures_to_auto_deactivate']['max']
        self.failures_to_auto_deactivate = self.failures_to_auto_deactivate_default

        self.lasers = self.config['lasers']
        self.dynamic_lasers = self.config['dynamic_lasers']
        self.dynamic_lasers_timings = self.config['dynamic_lasers_timings']
        self.dynamic_lasers_default_difficulty = self.config['dynamic_lasers_default_difficulty']
        self.dynamic_lasers_difficulty = self.dynamic_lasers_default_difficulty

        self.auto_control_timeout = self.config['auto_control']['timeout']
        self.auto_control_failures_to_set_broken = self.config['auto_control']['failures_to_set_broken']
        self.auto_control_reactivate_delay = self.config['auto_control']['reactivate_delay']
        self.broken_lasers = set()
        self.auto_control_alarm_counters = {}
        self.auto_control_timeout_task = None
        self.auto_control_reactivate_task = None

        self.deactivated_lasers = set()
        self.laser_alarm_counters = {}

        reactor.callLater(3, self.event_reset)

    def on_first_connection(self):
        self.publish_session_data()

    @on_event(filter={'category': 'request_node_session_data'})
    def publish_session_data(self):
        self.publish_status()
        self.publish_dynamic_lasers_difficulty()
        self.publish_deactivated_lasers()
        self.publish_broken_lasers()
        self.publish_laser_alarm_counters()
        self.publish_failures_to_auto_deactivate()
        self.publish_failures_to_auto_deactivate_min()
        self.publish_failures_to_auto_deactivate_max()
        self.publish_check_sensors_delay()

    def publish_status(self):
        self.publish(
            {
                'category': 'set_session_data',
                'key': f'laser_status_{self.laser_prefix}',
                'data': self.status,
            }
        )

    def publish_dynamic_lasers_difficulty(self):
        self.publish(
            {
                'category': 'set_session_data',
                'key': f'laser_dynamic_difficulty_{self.laser_prefix}',
                'data': self.dynamic_lasers_difficulty,
            }
        )

    def publish_deactivated_lasers(self):
        self.publish(
            {
                'category': 'set_session_data',
                'key': f"deactivated_lasers_{self.laser_prefix}",
                'data': list(self.deactivated_lasers),
            }
        )

    def publish_broken_lasers(self):
        self.publish(
            {
                'category': 'set_session_data',
                'key': f"broken_lasers_{self.laser_prefix}",
                'data': list(self.broken_lasers),
            }
        )

    def publish_laser_alarm_counters(self):
        self.publish(
            {
                'category': 'set_session_data',
                'key': f"laser_alarm_counters_{self.laser_prefix}",
                'data': self.laser_alarm_counters,
            }
        )

    def publish_failures_to_auto_deactivate(self):
        self.publish(
            {
                'category': 'set_session_data',
                'key': f'laser_failures_to_auto_deactivate_{self.laser_prefix}',
                'data': self.failures_to_auto_deactivate,
            }
        )

    def publish_failures_to_auto_deactivate_min(self):
        self.publish(
            {
                'category': 'set_session_data',
                'key': f'laser_failures_to_auto_deactivate_min_{self.laser_prefix}',
                'data': self.failures_to_auto_deactivate_min,
            }
        )

    def publish_failures_to_auto_deactivate_max(self):
        self.publish(
            {
                'category': 'set_session_data',
                'key': f'laser_failures_to_auto_deactivate_max_{self.laser_prefix}',
                'data': self.failures_to_auto_deactivate_max,
            }
        )

    def publish_check_sensors_delay(self):
        self.publish(
            {
                'category': 'set_session_data',
                'key': f'laser_check_sensors_delay_{self.laser_prefix}',
                'data': self.check_sensors_delay,
            }
        )

    @on_event(filter={'category': 'set_dynamic_lasers_difficulty'})
    def event_set_dynamic_lasers_difficulty(self, difficulty: str):
        logger.info(f"Setting dynamic lasers difficulty to {difficulty}")

        if difficulty not in self.dynamic_lasers_timings:
            logger.error("Unknown difficulty: aborting")
            return

        self.dynamic_lasers_difficulty = difficulty
        self.publish_dynamic_lasers_difficulty()

    @on_event(filter={'category': 'set_failures_to_auto_deactivate'})
    def event_set_failures_to_auto_deactivate(self, n: int):
        new_failures_to_auto_deactivate = max(
            self.failures_to_auto_deactivate_min, min(self.failures_to_auto_deactivate_max, n))
        if self.failures_to_auto_deactivate != new_failures_to_auto_deactivate:
            self.failures_to_auto_deactivate = new_failures_to_auto_deactivate
            self.publish_failures_to_auto_deactivate()

    @staticmethod
    def get_bitmask(lasers, deactivated_lasers):
        bitmask = 0
        for bit_of_mask in lasers:
            if bit_of_mask not in deactivated_lasers:
                bitmask += 2 ** bit_of_mask
        return bitmask

    @on_event(filter={'category': 'set_activated'})
    def event_set_activated(self, index: int, activated: bool):
        if activated:
            logger.info("Reactivating laser index={}".format(index))
            self.deactivated_lasers.discard(index)
        else:
            logger.info("Deactivating laser index={}".format(index))
            self.deactivated_lasers.add(index)

        self.publish_deactivated_lasers()

    @on_event(filter={ArduinoProtocol.CATEGORY: ArduinoProtocol.ALARM})
    def serial_event_alarm(self, i: int):
        laser_index = i

        logger.info("Alarm from laser index={}".format(laser_index))

        if laser_index not in self.laser_alarm_counters:
            self.laser_alarm_counters[laser_index] = 0
        self.laser_alarm_counters[laser_index] += 1

        if self.status == 'auto_control':
            if self.auto_control_timeout_task and self.auto_control_timeout_task.active():
                self.auto_control_timeout_task.cancel()

            if self.laser_alarm_counters[laser_index] >= self.auto_control_failures_to_set_broken:
                self.broken_lasers.add(laser_index)
                self.publish_broken_lasers()

            self.auto_control_reactivate_task = reactor.callLater(
                self.auto_control_reactivate_delay, self.auto_control_laser_on)

        else:
            self.publish({"category": "laser_alarm", "laser": "{}{}".format(self.laser_prefix, laser_index)})

            if self.laser_alarm_counters[laser_index] >= self.failures_to_auto_deactivate:
                self.event_set_activated(laser_index, False)

        self.publish_laser_alarm_counters()

    def event_laser_on(
            self, bitmask: int = 0, dynamic_bitmask: int = 0, dynamic_downtime: int = 0,
            dynamic_uptime: int = 0, dynamic_incremental_offset: int = 0, sample_delay: int = 10,
    ):
        logger.info("Set bitmask={}".format(bitmask))
        self.send_serial(
            {
                ArduinoProtocol.CATEGORY: ArduinoProtocol.LASER_ON,
                ArduinoProtocol.LASER_ON_BITMASK: bitmask,
                ArduinoProtocol.DYNAMIC_LASER_ON_BITMASK: dynamic_bitmask,
                ArduinoProtocol.DYNAMIC_LASER_DOWNTIME: dynamic_downtime,
                ArduinoProtocol.DYNAMIC_LASER_UPTIME: dynamic_uptime,
                ArduinoProtocol.DYNAMIC_LASER_INCREMENTAL_OFFSET: dynamic_incremental_offset,
                ArduinoProtocol.SAMPLE_DELAY: sample_delay,
            }
        )

    def set_success(self, value: bool):
        logger.info("Setting success={}".format(value))
        self.send_serial(
            {
                ArduinoProtocol.CATEGORY: ArduinoProtocol.SET_SUCCESS,
                ArduinoProtocol.SET_SUCCESS_VALUE: value,
            }
        )

    @on_event(filter={'category': 'set_sensors_delay'})
    def event_set_sensors_delay(self, value: int):
        logger.info("Setting sensors delay={}".format(value))
        self.check_sensors_delay = value
        self.send_serial(
            {
                ArduinoProtocol.CATEGORY: ArduinoProtocol.SET_SAMPLE_DELAY,
                ArduinoProtocol.SAMPLE_DELAY: value,
            }
        )
        self.publish_check_sensors_delay()

    @on_event(filter={'category': 'set_status'})
    def event_set_status(self, status: str):
        if status not in self.STATUSES:
            logger.warning(f"Unknown status '{status}': skipping")
            return

        logger.info(f"Set status to={status}")

        if self.auto_control_timeout_task and self.auto_control_timeout_task.active():
            self.auto_control_timeout_task.cancel()

        if self.auto_control_reactivate_task and self.auto_control_reactivate_task.active():
            self.auto_control_reactivate_task.cancel()

        if status == 'not_playing':
            logger.info("Stop playing")
            self.send_serial(
                {
                    ArduinoProtocol.CATEGORY: ArduinoProtocol.STOP_PLAYING,
                }
            )

        elif status == 'playing':
            bitmask = self.get_bitmask(self.lasers, self.deactivated_lasers)
            dynamic_bitmask = self.get_bitmask(self.dynamic_lasers, self.deactivated_lasers)
            dynamic_downtime = self.dynamic_lasers_timings[self.dynamic_lasers_difficulty]['downtime']
            dynamic_uptime = self.dynamic_lasers_timings[self.dynamic_lasers_difficulty]['uptime']
            dynamic_incremental_offset = self.dynamic_lasers_timings[self.dynamic_lasers_difficulty][
                'incremental_offset']
            self.set_success(False)
            self.event_laser_on(
                bitmask, dynamic_bitmask, dynamic_downtime, dynamic_uptime, dynamic_incremental_offset,
                self.check_sensors_delay)

        elif status == 'success':
            self.set_success(True)

        elif status == 'auto_control':
            self.set_success(False)
            self.broken_lasers = set()
            self.laser_alarm_counters = {}
            self.publish_broken_lasers()
            self.publish_laser_alarm_counters()
            self.auto_control_laser_on()

        self.status = status
        self.publish_status()

    def auto_control_laser_on(self):
        bitmask = self.get_bitmask(self.lasers, self.broken_lasers)
        self.event_laser_on(bitmask, 0, 0, 10000, 0, self.check_sensors_delay_default)

        self.auto_control_timeout_task = reactor.callLater(
            self.auto_control_timeout, self.end_of_auto_control)

    def end_of_auto_control(self):
        logger.info("End of auto control")

        self.laser_alarm_counters = {}
        self.deactivated_lasers = self.broken_lasers
        self.event_set_status('not_playing')

        self.publish_laser_alarm_counters()
        self.publish_deactivated_lasers()

    @on_event(filter={'category': 'reset'})
    def event_reset(self):
        logger.info("Resetting")

        self.laser_alarm_counters = {}
        self.failures_to_auto_deactivate = self.failures_to_auto_deactivate_default
        self.check_sensors_delay = self.check_sensors_delay_default
        self.dynamic_lasers_difficulty = self.dynamic_lasers_default_difficulty

        self.event_set_status('auto_control')

        self.event_set_sensors_delay(self.check_sensors_delay)

        self.publish_dynamic_lasers_difficulty()
        self.publish_laser_alarm_counters()
        self.publish_failures_to_auto_deactivate()
        self.publish_check_sensors_delay()
