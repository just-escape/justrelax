from twisted.internet import reactor

from justrelax.common.logging_utils import logger
from justrelax.node.helper import Serial
from justrelax.node.service import JustSockClientService, orchestrator_event


class SerialEventBuffer:
    def __init__(self, serial, interval):
        self.queue = []

        self.serial = serial
        self.interval = interval

        self.delay_task = None

    def _send_event(self, event):
        self.serial.send_event(event)
        self.delay_task = reactor.callLater(self.interval, self.pop_event)

    def send_event(self, event):
        if self.delay_task and self.delay_task.active():
            self.queue.append(event)

        else:
            self._send_event(event)

    def pop_event(self):
        if not self.queue:
            return

        event = self.queue.pop(0)
        self._send_event(event)


class LaserMaze(JustSockClientService):
    class ARDUINO_PROTOCOL:
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

    def __init__(self, *args, **kwargs):
        self._difficulty = None

        super(LaserMaze, self).__init__(*args, **kwargs)

        self.success = False

        self.laser_prefix = self.node_params['laser_prefix']

        self.default_difficulty = self.node_params['default_difficulty']
        self.difficulty_settings = self.node_params['difficulty_settings']

        port = self.node_params['arduino']['port']
        baud_rate = self.node_params['arduino']['baud_rate']
        buffering_interval = self.node_params['arduino']['buffering_interval']

        self.serial = Serial(self, port, baud_rate)
        self.buffer = SerialEventBuffer(self.serial, buffering_interval)

        reactor.callLater(3, self.init_arduino)

    @property
    def difficulty(self):
        return self._difficulty

    @difficulty.setter
    def difficulty(self, value):
        if value not in self.difficulty_settings:
            logger.error("Unknown difficulty {} (must be one of {}): skipping".format(
                value, ", ".join(self.difficulty_settings.keys())
            ))
            return

        self._difficulty = value

        bitmask = self.difficulty_settings[value]['laser_bitmask']
        dynamic_bitmask = self.difficulty_settings[value]['dynamic_laser_bitmask']
        dynamic_downtime = self.difficulty_settings[value]['dynamic_laser_downtime']
        dynamic_uptime = self.difficulty_settings[value]['dynamic_laser_uptime']
        dynamic_incremental_offset = self.difficulty_settings[value]['dynamic_laser_incremental_offset']
        self.event_laser_on(
            bitmask, dynamic_bitmask, dynamic_downtime, dynamic_uptime, dynamic_incremental_offset)

    def process_serial_event(self, event):
        logger.debug("Processing event '{}'".format(event))

        if self.ARDUINO_PROTOCOL.CATEGORY not in event:
            logger.error("Event has not category: skipping")
            return

        if event[self.ARDUINO_PROTOCOL.CATEGORY] == self.ARDUINO_PROTOCOL.ALARM:
            if self.ARDUINO_PROTOCOL.ALARM_LASER_INDEX not in event:
                logger.error("Event has no laser index: skipping")
                return

            laser_index = event[self.ARDUINO_PROTOCOL.ALARM_LASER_INDEX]
            self.on_alarm(laser_index)

        else:
            logger.error("Unknown event category '{}': skipping".format(event[self.ARDUINO_PROTOCOL.CATEGORY]))

    def on_alarm(self, laser_index):
        logger.info("Alarm from laser index={}".format(laser_index))
        self.send_event({"category": "alarm", "laser": "{}{}".format(self.laser_prefix, laser_index)})

    def init_arduino(self):
        self.difficulty = self.default_difficulty

    @orchestrator_event(filter={'category': 'laser_on'})
    def event_laser_on(
            self, bitmask: int = 0, dynamic_bitmask: int = 0, dynamic_downtime: int = 0,
            dynamic_uptime: int = 0, dynamic_incremental_offset: int = 0,
            sample_delay: int = 10,
    ):
        logger.info("Set bitmask={}".format(bitmask))
        self.buffer.send_event(
            {
                self.ARDUINO_PROTOCOL.CATEGORY: self.ARDUINO_PROTOCOL.LASER_ON,
                self.ARDUINO_PROTOCOL.LASER_ON_BITMASK: bitmask,
                self.ARDUINO_PROTOCOL.DYNAMIC_LASER_ON_BITMASK: dynamic_bitmask,
                self.ARDUINO_PROTOCOL.DYNAMIC_LASER_DOWNTIME: dynamic_downtime,
                self.ARDUINO_PROTOCOL.DYNAMIC_LASER_UPTIME: dynamic_uptime,
                self.ARDUINO_PROTOCOL.DYNAMIC_LASER_INCREMENTAL_OFFSET: dynamic_incremental_offset,
                self.ARDUINO_PROTOCOL.SAMPLE_DELAY: sample_delay,
            }
        )

    @orchestrator_event(filter={'category': 'set_difficulty'})
    def event_set_difficulty(self, difficulty: str):
        self.difficulty = difficulty

    @orchestrator_event(filter={'category': 'stop_playing'})
    def event_stop_playing(self):
        logger.info("Stop playing")
        self.buffer.send_event(
            {
                self.ARDUINO_PROTOCOL.CATEGORY: self.ARDUINO_PROTOCOL.STOP_PLAYING,
            }
        )

    @orchestrator_event(filter={'category': 'playing'})
    def event_playing(self):
        bitmask = self.difficulty_settings[self.difficulty]['laser_bitmask']
        dynamic_bitmask = self.difficulty_settings[self.difficulty]['dynamic_laser_bitmask']
        dynamic_downtime = self.difficulty_settings[self.difficulty]['dynamic_laser_downtime']
        dynamic_uptime = self.difficulty_settings[self.difficulty]['dynamic_laser_uptime']
        dynamic_incremental_offset = self.difficulty_settings[self.difficulty]['dynamic_laser_incremental_offset']
        self.event_laser_on(
            bitmask, dynamic_bitmask, dynamic_downtime, dynamic_uptime, dynamic_incremental_offset)

    @orchestrator_event(filter={'category': 'set_success'})
    def event_set_success(self, value: bool):
        logger.info("Setting success={}".format(value))
        self.success = value
        self.buffer.send_event(
            {
                self.ARDUINO_PROTOCOL.CATEGORY: self.ARDUINO_PROTOCOL.SET_SUCCESS,
                self.ARDUINO_PROTOCOL.SET_SUCCESS_VALUE: value,
            }
        )

    @orchestrator_event(filter={'category': 'set_sample_delay'})
    def event_set_sample_delay(self, value: int):
        logger.info("Setting sample delay={}".format(value))
        self.buffer.send_event(
            {
                self.ARDUINO_PROTOCOL.CATEGORY: self.ARDUINO_PROTOCOL.SET_SAMPLE_DELAY,
                self.ARDUINO_PROTOCOL.SAMPLE_DELAY: value,
            }
        )

    @orchestrator_event(filter={'category': 'reset'})
    def event_reset(self):
        logger.info("Resetting")
        self.event_set_success(False)
        self.difficulty = self.default_difficulty
