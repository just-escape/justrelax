import json

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
    def __init__(self, *args, **kwargs):
        self._difficulty = None

        super(LaserMaze, self).__init__(*args, **kwargs)

        self.laser_prefix = self.config['laser_prefix']

        self.default_difficulty = self.config['default_difficulty']
        self.difficulty_settings = self.config['difficulty_settings']

        try:
            with open(self.config['deactivation_file'], "r") as fh:
                self.deactivated_lasers = json.loads(fh.read())
        except Exception:
            logger.error("Unable to load deactivation file", exc_info=True)
            self.deactivated_lasers = []
        self.laser_alarm_counters = {}

        reactor.callLater(3, self.init_arduino)

    def on_first_connection(self):
        self.publish_session_data()

    @on_event(filter={'category': 'request_node_session_data'})
    def publish_session_data(self):
        self.publish_deactivated_lasers()
        self.publish_laser_alarm_counters()

    def publish_deactivated_lasers(self):
        self.publish(
            {
                'category': 'set_session_data',
                'key': f"deactivated_lasers_{self.laser_prefix}",
                'data': self.deactivated_lasers,
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

    def get_bitmask(self, lasers):
        bitmask = 0
        for bit_of_mask in lasers:
            if bit_of_mask not in self.deactivated_lasers:
                bitmask += 2 ** bit_of_mask
        return bitmask

    @property
    def difficulty(self):
        return self._difficulty

    @difficulty.setter
    def difficulty(self, value):
        if value not in self.difficulty_settings:
            logger.warning("Unknown difficulty {} (must be one of {}): skipping".format(
                value, ", ".join(self.difficulty_settings.keys())
            ))
            return

        self._difficulty = value

        bitmask = self.get_bitmask(self.difficulty_settings[value]['lasers'])
        dynamic_bitmask = self.get_bitmask(self.difficulty_settings[value]['dynamic_lasers'])
        dynamic_downtime = self.difficulty_settings[value]['dynamic_laser_downtime']
        dynamic_uptime = self.difficulty_settings[value]['dynamic_laser_uptime']
        dynamic_incremental_offset = self.difficulty_settings[value]['dynamic_laser_incremental_offset']
        self.event_laser_on(
            bitmask, dynamic_bitmask, dynamic_downtime, dynamic_uptime, dynamic_incremental_offset)

    @on_event(filter={'category': 'reactivate_permanently'})
    def event_reactivate_permanently(self, index: int):
        logger.info("Reactivating laser index={}".format(index))
        self.deactivated_lasers = [x for x in self.deactivated_lasers if x != index]
        self.publish_deactivated_lasers()
        try:
            with open(self.config['deactivation_file'], 'w+') as fh:
                json.dump(self.deactivated_lasers, fh)
        except Exception:
            logger.error("Unable to make reactivation persistent", exc_info=True)
        else:
            logger.info("Laser index={} has been permanently reactivated (new deactivated list={})".format(
                index, self.deactivated_lasers))

    @on_event(filter={'category': 'deactivate_permanently'})
    def event_deactivate_permanently(self, index: int):
        if index in self.deactivated_lasers:
            logger.info("Laser index={} is already deactivated: skipping".format(index))

        else:
            logger.info("Deactivating laser index={}".format(index))
            self.deactivated_lasers = sorted(self.deactivated_lasers + [index])
            self.publish_deactivated_lasers()
            try:
                with open(self.config['deactivation_file'], 'w+') as fh:
                    json.dump(self.deactivated_lasers, fh)
            except Exception:
                logger.error("Unable to make deactivation persistent", exc_info=True)
            else:
                logger.info("Laser index={} has been permanently deactivated (new deactivated list={})".format(
                    index, self.deactivated_lasers))

    @on_event(filter={ArduinoProtocol.CATEGORY: ArduinoProtocol.ALARM})
    def serial_event_alarm(self, i: int):
        laser_index = i

        logger.info("Alarm from laser index={}".format(laser_index))
        self.publish({"category": "alarm", "laser": "{}{}".format(self.laser_prefix, laser_index)})

        if laser_index not in self.laser_alarm_counters:
            self.laser_alarm_counters[laser_index] = 0

        self.laser_alarm_counters[laser_index] += 1
        self.publish_laser_alarm_counters()

    def init_arduino(self):
        self.difficulty = self.default_difficulty

    @on_event(filter={'category': 'laser_on'})
    def event_laser_on(
            self, bitmask: int = 0, dynamic_bitmask: int = 0, dynamic_downtime: int = 0,
            dynamic_uptime: int = 0, dynamic_incremental_offset: int = 0,
            sample_delay: int = 10,
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

    @on_event(filter={'category': 'set_difficulty'})
    def event_set_difficulty(self, difficulty: str):
        self.difficulty = difficulty

    @on_event(filter={'category': 'stop_playing'})
    def event_stop_playing(self):
        logger.info("Stop playing")
        self.send_serial(
            {
                ArduinoProtocol.CATEGORY: ArduinoProtocol.STOP_PLAYING,
            }
        )

    @on_event(filter={'category': 'playing'})
    def event_playing(self):
        bitmask = self.get_bitmask(self.difficulty_settings[self.difficulty]['lasers'])
        dynamic_bitmask = self.get_bitmask(self.difficulty_settings[self.difficulty]['dynamic_lasers'])
        dynamic_downtime = self.difficulty_settings[self.difficulty]['dynamic_laser_downtime']
        dynamic_uptime = self.difficulty_settings[self.difficulty]['dynamic_laser_uptime']
        dynamic_incremental_offset = self.difficulty_settings[self.difficulty]['dynamic_laser_incremental_offset']
        self.event_laser_on(
            bitmask, dynamic_bitmask, dynamic_downtime, dynamic_uptime, dynamic_incremental_offset)

    @on_event(filter={'category': 'set_success'})
    def event_set_success(self, value: bool):
        logger.info("Setting success={}".format(value))
        self.send_serial(
            {
                ArduinoProtocol.CATEGORY: ArduinoProtocol.SET_SUCCESS,
                ArduinoProtocol.SET_SUCCESS_VALUE: value,
            }
        )

    @on_event(filter={'category': 'set_sample_delay'})
    def event_set_sample_delay(self, value: int):
        logger.info("Setting sample delay={}".format(value))
        self.send_serial(
            {
                ArduinoProtocol.CATEGORY: ArduinoProtocol.SET_SAMPLE_DELAY,
                ArduinoProtocol.SAMPLE_DELAY: value,
            }
        )

    @on_event(filter={'category': 'reset'})
    def event_reset(self):
        logger.info("Resetting")
        self.event_set_success(False)
        self.difficulty = self.default_difficulty
        self.laser_alarm_counters = {}
        self.publish_laser_alarm_counters()
