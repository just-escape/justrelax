from twisted.internet import reactor

from justrelax.common.logging_utils import logger

from justrelax.node.helper import Serial
from justrelax.node.service import JustSockClientService, EventCategoryToMethodMixin


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

        self.serial = Serial(self, port, baud_rate)

        # Delay everything to avoid a burst of characters on the arduino serial input, ensuring
        # all characters are read.
        incremental_delay = 1

        for channel in self.node_params['channels']:
            reactor.callLater(
                incremental_delay,
                self.configure_channel_color,
                channel['n'],
                channel['rate'],
            )
            incremental_delay += 0.1

        for color_name, color_params in self.node_params['colors'].items():
            self.colors[color_name] = color_params['channel']

            on_by_default = color_params.get('on_by_default', False)
            default_brightness = color_params.get('default_brightness', None)

            if on_by_default:
                reactor.callLater(
                    incremental_delay,
                    self.event_on,
                    color_name,
                )
                incremental_delay += 0.1

            if default_brightness is not None:
                reactor.callLater(
                    incremental_delay,
                    self.event_fade_brightness,
                    color_name,
                    default_brightness,
                )
                incremental_delay += 0.1

    def process_serial_event(self, event):
        self.send_event(event)

    def configure_channel_color(self, channel, rate):
        self.serial.send_event({
            self.ARDUINO_PROTOCOL.CATEGORY: self.ARDUINO_PROTOCOL.SET_COLOR,
            self.ARDUINO_PROTOCOL.CHANNEL: channel,
            self.ARDUINO_PROTOCOL.COLOR: rate,
        })

    def event_on(self, color):
        self.serial.send_event({
            self.ARDUINO_PROTOCOL.CATEGORY: self.ARDUINO_PROTOCOL.ON,
            self.ARDUINO_PROTOCOL.CHANNEL: self.colors[color],
        })

    def event_off(self, color):
        self.serial.send_event({
            self.ARDUINO_PROTOCOL.CATEGORY: self.ARDUINO_PROTOCOL.OFF,
            self.ARDUINO_PROTOCOL.CHANNEL: self.colors[color],
        })

    def event_fade_brightness(self, color, brightness):
        self.serial.send_event({
            self.ARDUINO_PROTOCOL.CATEGORY: self.ARDUINO_PROTOCOL.FADE_BRIGHTNESS,
            self.ARDUINO_PROTOCOL.CHANNEL: self.colors[color],
            self.ARDUINO_PROTOCOL.TARGET_BRIGHTNESS: brightness,
        })
