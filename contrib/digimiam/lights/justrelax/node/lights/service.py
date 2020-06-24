import time

import pytweening
from gpiozero import PWMLED

from twisted.internet import reactor

from justrelax.common.logging_utils import logger
from justrelax.node.service import JustSockClientService, EventCategoryToMethodMixin


EASE_MAPPING = {
    'easeInSine': pytweening.easeInSine,
    'easeOutSine': pytweening.easeOutSine,
    'easeInOutSine': pytweening.easeInOutSine,
    'easeInCubic': pytweening.easeInCubic,
    'easeOutCubic': pytweening.easeOutCubic,
    'easeInOutCubic': pytweening.easeInOutCubic,
    'easeInQuint': pytweening.easeInQuint,
    'easeOutQuint': pytweening.easeOutQuint,
    'easeInOutQuint': pytweening.easeInOutQuint,
    'easeInCirc': pytweening.easeInCirc,
    'easeOutCirc': pytweening.easeOutCirc,
    'easeInOutCirc': pytweening.easeInOutCirc,
    'easeInElastic': pytweening.easeInElastic,
    'easeOutElastic': pytweening.easeOutElastic,
    'easeInOutElastic': pytweening.easeInOutElastic,
    'easeInQuad': pytweening.easeInQuad,
    'easeOutQuad': pytweening.easeOutQuad,
    'easeInOutQuad': pytweening.easeInOutQuad,
    'easeInQuart': pytweening.easeInQuart,
    'easeOutQuart': pytweening.easeOutQuart,
    'easeInExpo': pytweening.easeInExpo,
    'easeOutExpo': pytweening.easeOutExpo,
    'easeInOutExpo': pytweening.easeInOutExpo,
    'easeInBack': pytweening.easeInBack,
    'easeOutBack': pytweening.easeOutBack,
    'easeInOutBack': pytweening.easeInOutBack,
    'easeInBounce': pytweening.easeInBounce,
    'easeOutBounce': pytweening.easeOutBounce,
    'easeInOutBounce': pytweening.easeInOutBounce,
    'linear': pytweening.linear,
}


class BrightnessFaderMixin:
    def __init__(self, default_brightness, frequency):
        self.update_frequency = frequency
        self.current_brightness = default_brightness
        self.target_brightness = default_brightness

    def fade_brightness(self, brightness, duration, ease=pytweening.easeInOutSine):
        if duration == 0:
            self.current_brightness = brightness
            self.target_brightness = brightness
            self.update_brightness()
        else:
            self._fade_brightness(brightness, duration, ease=ease)

    def _fade_brightness(self, brightness, duration, ease=pytweening.easeInOutSine):
        t_start = time.time()
        current_brightness_diff = 0
        target_brightness_diff = brightness - self.target_brightness
        self.target_brightness = self.target_brightness + target_brightness_diff

        def update():
            now = time.time()
            progression = (now - t_start) / duration
            logger.info("progression={}, now={}, t_start={}, duration={}".format(
                self.current_brightness, now, t_start, duration))

            nonlocal current_brightness_diff
            if progression < 1:
                eased_progression = ease(progression)
                reactor.callLater(self.update_frequency, update)
            else:
                eased_progression = 1

            new_brightness_diff = target_brightness_diff * eased_progression - current_brightness_diff
            self.current_brightness += new_brightness_diff
            current_brightness_diff += new_brightness_diff
            logger.info("current_brightness={}".format(self.current_brightness))

            self.update_brightness()

        reactor.callLater(self.update_frequency, update)

    def update_brightness(self):
        pass


class Light(BrightnessFaderMixin):
    def __init__(self, pin, default_brightness=1, off_by_default=False, frequency=0.01):
        super(Light, self).__init__(default_brightness, frequency)

        self.led = PWMLED(pin)
        self.is_on = not off_by_default

        self.update_brightness()

    def update_brightness(self):
        self.led.value = min(max(self.current_brightness, 0), 1) if self.is_on else 0

    def on(self):
        self.is_on = True
        self.update_brightness()

    def off(self):
        self.is_on = False
        self.update_brightness()


class RGBLight(BrightnessFaderMixin):
    def __init__(self, pins, color, default_brightness=1, off_by_default=False, frequency=0.01):
        super(RGBLight, self).__init__(default_brightness, frequency)

        self.color = color
        self.r = PWMLED(pins['r'])
        self.g = PWMLED(pins['g'])
        self.b = PWMLED(pins['b'])

        self.is_on = not off_by_default

        self.update_brightness()

    def update_brightness(self):
        self.r.value = self.color['r'] * min(max(self.current_brightness, 0), 1) if self.is_on else 0
        self.g.value = self.color['g'] * min(max(self.current_brightness, 0), 1) if self.is_on else 0
        self.b.value = self.color['b'] * min(max(self.current_brightness, 0), 1) if self.is_on else 0

    def on(self):
        self.is_on = True
        self.update_brightness()

    def off(self):
        self.is_on = False
        self.update_brightness()


class Lights(EventCategoryToMethodMixin, JustSockClientService):
    def __init__(self, *args, **kwargs):
        super(Lights, self).__init__(*args, **kwargs)

        self.colors = {}

        for color, color_params in self.node_params['colors'].items():
            if color_params['type'] == 'led':
                self.colors[color] = Light(
                    color_params['pin'],
                    color_params['default_brightness'],
                    color_params['off_by_default'],
                    frequency=self.node_params['fade_frequency'],
                )
            elif color_params['type'] == 'rgbled':
                self.colors[color] = RGBLight(
                    color_params['pins'],
                    color_params['color'],
                    color_params['default_brightness'],
                    color_params['off_by_default'],
                    frequency=self.node_params['fade_frequency'],
                )

    def event_on(self, color):
        self.colors[color].on()

    def event_off(self, color):
        self.colors[color].off()

    def event_fade_brightness(self, color, brightness, duration=0, ease='easeInOutSine'):
        if ease in EASE_MAPPING:
            ease_function = EASE_MAPPING[ease]
        else:
            ease_function = pytweening.easeInOutSine
            logger.warning("Ease {} not found: falling back with easeInOutSine".format(ease))
        self.colors[color].fade_brightness(brightness, duration, ease_function)
