import neopixel
import board

from justrelax.core.node import MagicNode


class Relays(MagicNode):
    def __init__(self, *args, **kwargs):
        super(Relays, self).__init__(*args, **kwargs)

        self.led_strip = neopixel.NeoPixel(board.D18, 9)
        self.led_strip.fill((10, 10, 10))
