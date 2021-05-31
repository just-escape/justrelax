import neopixel
import board

from justrelax.core.node import MagicNode


class Chopsticks(MagicNode):
    def __init__(self, *args, **kwargs):
        super(Chopsticks, self).__init__(*args, **kwargs)

        self.led_strip = neopixel.NeoPixel(board.D18, 9)
        self.led_strip.fill((10, 10, 10))
