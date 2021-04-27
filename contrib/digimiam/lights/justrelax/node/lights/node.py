from twisted.internet import reactor

from gpiozero import OutputDevice

from justrelax.core.logging_utils import logger
from justrelax.core.node import MagicNode, on_event


class ArduinoProtocol:
    CATEGORY = 'c'

    CHANNEL = 'h'
    SET_COLOR = 's'
    COLOR = 'r'
    STOP_GLITCH_ANIMATION = 'sga'
    ANIMATE_GLITCH = 'g'
    SHORT_GLITCH_PM = 'sg'
    SHORT_DIMMED_GLITCH_PM = 'sdg'
    LONG_GLITCH_PM = 'lg'
    LONG_DIMMED_GLITCH_PM = 'ldg'
    STABILITY = 'st'
    STABILITY_DURATION = 'std'


class Lights(MagicNode):
    def __init__(self, *args, **kwargs):
        super(Lights, self).__init__(*args, **kwargs)

        self.colors = {}
        self.on_off_pins = {}

        self.animations = self.config.get('animations', {})

        reactor.callLater(3, self.init_arduino)

    @on_event(filter={'category': 'reset'})
    def init_arduino(self):
        for channel_mask, color in self.config['channels'].items():
            self.event_configure_channel_color(channel_mask, color)

        for color_name, color_params in self.config['colors'].items():
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

            if 'glitch' in color_params:
                self.colors[color_name]['glitch'] = color_params['glitch']
                glitch_by_default = color_params['glitch'].get('by_default', False)
                if not glitch_by_default:
                    self.event_stop_glitch(color_name)
                else:
                    self.event_glitch(color_name)

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
    def event_on(self, color: str):
        logger.info("Turning on {}".format(color))

        color_config = self.colors.get(color, None)
        if not color_config:
            logger.error("Color {} not found: aborting".format(color))
            return

        for on_off_pin in self.colors[color]['on_off_pins']:
            self.on_off_pins[on_off_pin].on()

    @on_event(filter={'category': 'off'})
    def event_off(self, color: str):
        logger.info("Turning off {}".format(color))

        color_config = self.colors.get(color, None)
        if not color_config:
            logger.error("Color {} not found: aborting".format(color))
            return

        for on_off_pin in self.colors[color]['on_off_pins']:
            self.on_off_pins[on_off_pin].off()

    @on_event(filter={'category': 'glitch_channel'})
    def event_glitch_channel(
            self, channel: int, sg: int = 36, sdg: int = 0, lg: int = 3, ldg: int = 1, st: int = 5, std: int = 8000):
        logger.info("Glitching channel={}".format(channel))

        self.send_serial(
            {
                ArduinoProtocol.CATEGORY: ArduinoProtocol.ANIMATE_GLITCH,
                ArduinoProtocol.CHANNEL: channel,
                ArduinoProtocol.SHORT_GLITCH_PM: sg,
                ArduinoProtocol.SHORT_DIMMED_GLITCH_PM: sdg,
                ArduinoProtocol.LONG_GLITCH_PM: lg,
                ArduinoProtocol.LONG_DIMMED_GLITCH_PM: ldg,
                ArduinoProtocol.STABILITY: st,
                ArduinoProtocol.STABILITY_DURATION: std,
            }
        )

    @on_event(filter={'category': 'glitch'})
    def event_glitch(self, color: str):
        logger.info("Glitching color={}".format(color))

        color_config = self.colors.get(color, None)
        if not color_config:
            logger.error("Color {} not found: aborting".format(color))
            return

        glitch_config = color_config.get('glitch', None)
        if not glitch_config:
            logger.error("Color {} has no glitch parameters: aborting".format(color))
            return

        channel = glitch_config.get('channel', 0)
        sg = glitch_config.get('short_glitch_per_mille', 36)
        sdg = glitch_config.get('short_dimmed_glitch_per_mille', 0)
        lg = glitch_config.get('long_glitch_per_mille', 3)
        ldg = glitch_config.get('long_dimmed_glitch_per_mille', 1)
        st = glitch_config.get('stability_per_mille', 5)
        std = glitch_config.get('stability_duration', 8000)
        self.event_glitch_channel(channel, sg, sdg, lg, ldg, st, std)

    @on_event(filter={'category': 'stop_glitch_channel'})
    def event_stop_glitch_channel(self, channel: int):
        logger.info("Stop glitching channel={}".format(channel))

        self.send_serial(
            {
                ArduinoProtocol.CATEGORY: ArduinoProtocol.STOP_GLITCH_ANIMATION,
                ArduinoProtocol.CHANNEL: channel,
            }
        )

    @on_event(filter={'category': 'stop_glitch'})
    def event_stop_glitch(self, color: str):
        logger.info("Stop glitching color={}".format(color))

        color_config = self.colors.get(color, None)
        if not color_config:
            logger.error("Color {} not found: aborting".format(color))
            return

        glitch_config = color_config.get('glitch', None)
        if not glitch_config:
            logger.error("Color {} has no glitch parameters: aborting".format(color))
            return

        channel = glitch_config.get('channel', 0)
        self.event_stop_glitch_channel(channel)

    @on_event(filter={'category': 'play_animation'})
    def event_play_animation(
            self, name: str, color: str, speed: float = 1, reversed_t: bool = False, inverted_on_off: bool = False):
        logger.info("Playing animation {} on color {} (speed={}, reversed_t={}, inverted_on_off={})".format(
            name, color, speed, reversed_t, inverted_on_off))
        animation = self.animations.get(name, None)
        if animation is None:
            logger.info("Animation {} not found: aborting".format(animation))
            return

        key_frames = animation if not reversed_t else reversed(animation)
        for key_frame_t, key_frame_on in key_frames.items():
            key_frame_on = not key_frame_on if inverted_on_off else key_frame_on
            event = self.event_on if key_frame_on else self.event_off
            reactor.callLater(key_frame_t / speed, event, color)
