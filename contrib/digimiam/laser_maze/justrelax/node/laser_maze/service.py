from twisted.internet import reactor

from justrelax.common.logging_utils import logger
from justrelax.node.helper import Serial
from justrelax.node.service import JustSockClientService, EventCategoryToMethodMixin


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


class LaserMaze(EventCategoryToMethodMixin, JustSockClientService):
    class ARDUINO_PROTOCOL:
        CATEGORY = "c"

        ERROR = "e"
        ALARM = "a"
        ALARM_LASER_INDEX = "i"
        TAG = "t"
        TAG_VALUE = "v"

        LASER_ON = "l"
        LASER_ON_BITMASK = "b"
        STOP_PLAYING = "s"

    def __init__(self, *args, **kwargs):
        super(LaserMaze, self).__init__(*args, **kwargs)

        self.default_difficulty = self.node_params['default_difficulty']
        self._difficulty = None
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

        difficulty_laser_bitmask = self.difficulty_settings[value]
        self.event_set_laser_bitmask(difficulty_laser_bitmask)

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

        elif event[self.ARDUINO_PROTOCOL.CATEGORY] == self.ARDUINO_PROTOCOL.TAG:
            if self.ARDUINO_PROTOCOL.TAG_VALUE not in event:
                logger.error("Event has no tag value: skipping")
                return

            tag = event[self.ARDUINO_PROTOCOL.TAG_VALUE]
            self.on_tag_read(tag)

        else:
            logger.error("Unknown event category '{}': skipping".format(self.ARDUINO_PROTOCOL.CATEGORY))

    def on_tag_read(self, tag):
        logger.info("Tag read={}".format(tag))

    def on_alarm(self, laser_index):
        logger.info("Alarm from laser index={}".format(laser_index))

    def init_arduino(self):
        self.difficulty = self.default_difficulty

    def event_set_laser_bitmask(self, bitmask: int):
        self.buffer.send_event(
            {
                self.ARDUINO_PROTOCOL.CATEGORY: self.ARDUINO_PROTOCOL.LASER_ON,
                self.ARDUINO_PROTOCOL.LASER_ON_BITMASK: bitmask,
            }
        )

    def event_set_difficulty(self, difficulty: str):
        self.difficulty = difficulty

    def event_stop_playing(self):
        self.buffer.send_event(
            {
                self.ARDUINO_PROTOCOL.CATEGORY: self.ARDUINO_PROTOCOL.STOP_PLAYING,
            }
        )

    def event_reset(self):
        self.difficulty = self.default_difficulty
