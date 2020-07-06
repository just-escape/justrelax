from twisted.internet import reactor

from justrelax.common.logging_utils import logger

from justrelax.node.helper import Serial
from justrelax.node.service import JustSockClientService, EventCategoryToMethodMixin


class SerialEventBuffer:
    def __init__(self, protocol, serial, interval):
        self.PROTOCOL = protocol
        self.serial = serial
        self.interval = interval

        self.queue = []

        self.delay_task = None

    def send_event(self, base_event, channel):
        if self.delay_task and self.delay_task.active():
            self.queue_event(base_event, channel)

        else:
            self._send_event(base_event, channel)

    def _send_event(self, base_event, channel):
        event = base_event
        event[self.PROTOCOL.CHANNEL] = channel

        self.serial.send_event(event)
        self.delay_task = reactor.callLater(self.interval, self.pop_event)

    def pop_event(self):
        if not self.queue:
            return

        event = self.queue.pop(0)
        base_event = event['base_event']
        channel = sum(event['channel'])

        self._send_event(base_event, channel)

    def queue_event(self, base_event, channel):
        for queued_event in self.queue:
            if queued_event['base_event'] == base_event:
                queued_event['channel'].add(channel)
                return

        else:
            self.queue.append(
                {
                    'base_event': base_event,
                    'channel': {channel},
                }
            )

        if base_event == {self.PROTOCOL.CATEGORY: self.PROTOCOL.ON}:
            event_to_cancel = {self.PROTOCOL.CATEGORY: self.PROTOCOL.OFF}
        elif base_event == {self.PROTOCOL.CATEGORY: self.PROTOCOL.OFF}:
            event_to_cancel = {self.PROTOCOL.CATEGORY: self.PROTOCOL.ON}
        else:
            event_to_cancel = None

        if event_to_cancel:
            for index, queued_event in enumerate(self.queue[:]):
                if queued_event['base_event'] == event_to_cancel:
                    queued_event.remove(channel)
                    if not queued_event['channel']:
                        self.queue.pop(index)


class Lights(EventCategoryToMethodMixin, JustSockClientService):
    class ARDUINO_PROTOCOL:
        CATEGORY = 'c'

        ON = 'n'
        OFF = 'f'
        CHANNEL = 'h'
        SET_COLOR = 's'
        COLOR = 'r'
        FADE_BRIGHTNESS = 'b'
        TARGET_BRIGHTNESS = 't'

    def __init__(self, *args, **kwargs):
        super(Lights, self).__init__(*args, **kwargs)

        self.colors = {}

        port = self.node_params['arduino']['port']
        baud_rate = self.node_params['arduino']['baud_rate']

        buffering_interval = self.node_params['arduino']['buffering_interval']

        self.serial = Serial(self, port, baud_rate)
        self.buffer = SerialEventBuffer(self.ARDUINO_PROTOCOL, self.serial, buffering_interval)

        reactor.callLater(3, self.init_arduino)

    def init_arduino(self):
        for channel in self.node_params['channels']:
            self.configure_channel_color(channel['n'], channel['rate'])

        for color_name, color_params in self.node_params['colors'].items():
            self.colors[color_name] = color_params['channel']

            on_by_default = color_params.get('on_by_default', False)
            default_brightness = color_params.get('default_brightness', None)

            if on_by_default:
                self.event_on(color_name)

            if default_brightness is not None:
                self.event_fade_brightness(color_name, default_brightness)

    def process_serial_event(self, event):
        # Error because events should not be received from the arduino
        logger.error(event)
        self.send_event(event)

    def configure_channel_color(self, channel, rate):
        self.buffer.send_event(
            base_event={
                self.ARDUINO_PROTOCOL.CATEGORY: self.ARDUINO_PROTOCOL.SET_COLOR,
                self.ARDUINO_PROTOCOL.COLOR: rate,
            },
            channel=channel,
        )

    def event_on(self, color):
        self.buffer.send_event(
            base_event={
                self.ARDUINO_PROTOCOL.CATEGORY: self.ARDUINO_PROTOCOL.ON,
            },
            channel=self.colors[color],
        )

    def event_off(self, color):
        self.buffer.send_event(
            base_event={
                self.ARDUINO_PROTOCOL.CATEGORY: self.ARDUINO_PROTOCOL.OFF,
            },
            channel=self.colors[color],
        )

    def event_fade_brightness(self, color, brightness):
        self.buffer.send_event(
            base_event={
                self.ARDUINO_PROTOCOL.CATEGORY: self.ARDUINO_PROTOCOL.FADE_BRIGHTNESS,
                self.ARDUINO_PROTOCOL.TARGET_BRIGHTNESS: brightness,
            },
            channel=self.colors[color],
        )
