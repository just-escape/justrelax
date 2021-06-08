import random
import uuid
import operator

import neopixel
import board

from twisted.internet import reactor

from justrelax.core.node import MagicNode, on_event


class Relays(MagicNode):
    def __init__(self, *args, **kwargs):
        super(Relays, self).__init__(*args, **kwargs)

        self.color_palette = 4 * ['white'] + 2 * ['orange'] + 1 * ['red']

        self.colors = self.config['colors']
        self.cpu_indexes = self.config['cpu_indexes']
        self.cable_indexes = self.config['cable_indexes']
        self.data_indexes = self.config['data_indexes']
        self.relay_indexes = self.config['relay_indexes']

        strip_length = (
            len(self.cpu_indexes) +
            len(self.cable_indexes) +
            len(self.data_indexes) +
            sum([len(ri) for ri in self.relay_indexes]))
        self.led_strip = neopixel.NeoPixel(board.D18, strip_length, auto_write=False, brightness=0.1)

        self.cpu_led_color = {}
        for index in self.cpu_indexes:
            self.cpu_led_color[index] = 'white'
            self.rotate_cpu_led_color(index)
            self.blink_cpu_led(index)

        self.cable_led_color = {}
        for index in self.cable_indexes:
            self.cable_led_color[index] = 'white'
            self.rotate_cable_led_color(index)
            self.fake_data_through_a_cable(index)

        self.data_frames = {}
        self.create_new_data_frames()

        for relay in self.relay_indexes:
            self.animate_relay(relay, current_index=len(relay) - 1)

    @on_event(filter={'category': 'reset'})
    def reset(self):
        self.color_palette = 4 * ['white'] + 2 * ['orange'] + 1 * ['red']

    @on_event(filter={'category': 'alarm'})
    def alarm(self, activated: bool = True):
        self.color_palette = ['red'] if activated else 4 * ['white'] + 2 * ['orange'] + 1 * ['red']

    def set_led_color(self, index, color):
        self.led_strip[index] = color

    def rotate_cpu_led_color(self, index):
        self.cpu_led_color[index] = random.choice(self.color_palette)
        delay = random.uniform(0.5, 4) if self.cpu_led_color[index] == 'white' else random.uniform(0.5, 2)
        reactor.callLater(delay, self.rotate_cpu_led_color, index)

    def blink_cpu_led(self, index, on=True):
        if random.random() > 0.01:
            self.set_led_color(index, self.colors[self.cpu_led_color[index]] if on else (0, 0, 0))
            self.led_strip.show()
            reactor.callLater(random.uniform(0.01, 0.25), self.blink_cpu_led, index, not on)
        else:
            reactor.callLater(random.uniform(1, 4), self.blink_cpu_led, index, not on)

    def rotate_cable_led_color(self, index):
        self.cable_led_color[index] = random.choice(self.color_palette)
        delay = random.uniform(5, 10) if self.cable_led_color[index] == 'white' else random.uniform(0.5, 2)
        reactor.callLater(delay, self.rotate_cable_led_color, index)

    def fake_data_through_a_cable(self, index, counter=0, transfer_speed=0.01, on=True, slow_packet_counter=0):
        if counter > 0:
            self.set_led_color(index, self.colors[self.cable_led_color[index]] if on else (0, 0, 0))
            self.led_strip.show()
            next_bit_delay = transfer_speed * 3 if slow_packet_counter > 0 else transfer_speed
            reactor.callLater(
                next_bit_delay,
                self.fake_data_through_a_cable,
                index,
                counter - 1,
                transfer_speed,
                not on,
                slow_packet_counter - 1 if random.random() > 0.005 else random.randint(2, 10)
            )
        else:
            reactor.callLater(
                random.uniform(0.3, 0.7),
                self.fake_data_through_a_cable,
                index,
                random.randint(1, 20) * 2 if random.random() > 0.4 else random.randint(1, 100) * 2,
                random.uniform(0.01, 0.05)
            )

    def create_new_data_frames(self):
        create_a_new_data_frame = False
        if len(self.data_frames) == 0:
            create_a_new_data_frame = True
        elif len(self.data_frames) < 5:
            if random.random() < 0.1 - 0.019 * len(self.data_frames):
                create_a_new_data_frame = True

        if create_a_new_data_frame:
            id_ = str(uuid.uuid4())
            data_frame = {
                'bits': 0b0_000_000_000_000_000_000_000_000_000_000,
                'color': random.choice(self.color_palette),
                'speed': random.uniform(0.03, 0.12),
                'move_operator': random.choice([operator.rshift, operator.lshift]),
            }

            if data_frame['move_operator'] == operator.rshift:
                data_frame['bits'] = (
                    0b1_111_111_100_000_000_000_000_000_000_000 << random.randint(0, 6)) % 2147483648  # 2^31
            else:
                data_frame['bits'] = 0b0_000_000_000_000_000_000_000_011_111_111 >> random.randint(0, 6)

            self.data_frames[id_] = data_frame
            self.animate_data_frame(id_)

        reactor.callLater(0.1, self.create_new_data_frames)

    def animate_data_frame(self, id_):
        if self.data_frames[id_]['bits'] == 0:
            del self.data_frames[id_]
        else:
            reactor.callLater(self.data_frames[id_]['speed'], self.animate_data_frame, id_)
            self.data_frames[id_]['bits'] = (
                    self.data_frames[id_]['move_operator'](self.data_frames[id_]['bits'], 1) % 2147483648)  # 2^31
            self.blit_data_frames()

    def blit_data_frames(self):
        led_mask = 0b0_000_000_010_000_000_000_000_000_000_000
        frames_sorted_by_speed = sorted(self.data_frames.values(), key=operator.itemgetter('speed'))
        for current_data_index in range(15):
            color = (0, 0, 0)
            for data_frame in frames_sorted_by_speed:
                if led_mask & data_frame['bits'] == led_mask:
                    color = self.colors[data_frame['color']]
                    break
            self.set_led_color(self.data_indexes[current_data_index], color)
            led_mask = led_mask >> 1
        self.led_strip.show()

    def animate_relay(
            self, led_indexes, color='white', filling=True, stop_at=0, start_at=0, current_index=0):
        if filling:
            if current_index < len(led_indexes) - 1:
                self.set_led_color(led_indexes[current_index + 1], (0, 0, 0))
            self.set_led_color(led_indexes[current_index], self.colors[color])
            self.led_strip.show()

            if current_index == stop_at:
                if stop_at == len(led_indexes) - 1:
                    reactor.callLater(
                        random.uniform(0.8, 1.3),
                        self.animate_relay,
                        led_indexes,
                        color,
                        filling=False,
                        start_at=0,
                        current_index=0,
                    )
                else:
                    reactor.callLater(
                        random.uniform(0.2, 1.3),
                        self.animate_relay,
                        led_indexes,
                        color,
                        filling=True,
                        stop_at=stop_at + 1,
                        current_index=len(led_indexes) - 1,
                    )
            else:
                reactor.callLater(
                    0.08,
                    self.animate_relay,
                    led_indexes,
                    color,
                    filling=True,
                    stop_at=stop_at,
                    current_index=current_index - 1,
                )

        else:
            if 0 < current_index:
                self.set_led_color(led_indexes[current_index - 1], self.colors[color])
            self.set_led_color(led_indexes[current_index], (0, 0, 0))
            self.led_strip.show()

            if current_index == 0:
                if start_at == len(led_indexes) - 1:
                    reactor.callLater(
                        random.uniform(1, 2.5),
                        self.animate_relay,
                        led_indexes,
                        random.choice(self.color_palette),
                        filling=True,
                        stop_at=0,
                        current_index=len(led_indexes) - 1,
                    )
                else:
                    reactor.callLater(
                        0.08,
                        self.animate_relay,
                        led_indexes,
                        color,
                        filling=False,
                        start_at=start_at + 1,
                        current_index=start_at + 1,
                    )

            else:
                reactor.callLater(
                    0.08,
                    self.animate_relay,
                    led_indexes,
                    color,
                    filling=False,
                    start_at=start_at,
                    current_index=current_index - 1,
                )
