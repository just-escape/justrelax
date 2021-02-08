from twisted.internet import reactor

from gpiozero import OutputDevice

from justrelax.common.logging_utils import logger
from justrelax.node.service import MagicNode, on_event


class ArduinoProtocol:
    CATEGORY = 'c'

    CHANNEL = 'h'
    SET_COLOR = 's'
    COLOR = 'r'


class Lights(MagicNode):
    def __init__(self, *args, **kwargs):
        super(Lights, self).__init__(*args, **kwargs)

        self.colors = {}
        self.on_off_pins = {}

        reactor.callLater(3, self.init_arduino)

    def init_arduino(self):
        for channel_mask, color in self.node_params['channels'].items():
            self.event_configure_channel_color(channel_mask, color)

        for color_name, color_params in self.node_params['colors'].items():
            self.colors[color_name] = {
                'on_off_pins': color_params['on_off_pins'],
            }

            for on_off_pin in color_params['on_off_pins']:
                if on_off_pin not in self.on_off_pins:
                    self.on_off_pins[on_off_pin] = OutputDevice(on_off_pin)

            if color_params.get('on_by_default', None) is not None:
                if color_params['on_by_default']:
                    self.event_on(color_name)
                else:
                    self.event_off(color_name)

    @on_event(filter={'category': 'configure_channel_color'})
    def event_configure_channel_color(self, channel: int, rate: int):
        logger.info("Configuring channel {} with rate {}".format(channel, rate))
        self.send_serial(
            {
                ArduinoProtocol.CATEGORY: ArduinoProtocol.SET_COLOR,
                ArduinoProtocol.CHANNEL: channel,
                ArduinoProtocol.COLOR: rate,
            }
        )

    @on_event(filter={'category': 'on'})
    def event_on(self, color):
        logger.info("Turning on {}".format(color))
        for on_off_pin in self.colors[color]['on_off_pins']:
            self.on_off_pins[on_off_pin].on()

    @on_event(filter={'category': 'off'})
    def event_off(self, color):
        logger.info("Turning off {}".format(color))
        for on_off_pin in self.colors[color]['on_off_pins']:
            self.on_off_pins[on_off_pin].off()

    @on_event(filter={'category': 'play_animation'})
    def event_play_animation(self):
        pass
