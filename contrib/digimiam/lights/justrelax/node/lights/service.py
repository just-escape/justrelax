from twisted.internet import reactor

from gpiozero import OutputDevice

from justrelax.common.logging_utils import logger
from justrelax.node.helper import Serial
from justrelax.node.service import JustSockClientService, event


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


class Lights(JustSockClientService):
    class ARDUINO_PROTOCOL:
        CATEGORY = 'c'

        CHANNEL = 'h'
        SET_COLOR = 's'
        COLOR = 'r'

    def __init__(self, *args, **kwargs):
        super(Lights, self).__init__(*args, **kwargs)

        self.colors = {}
        self.on_off_pins = {}

        port = self.node_params['arduino']['port']
        baud_rate = self.node_params['arduino']['baud_rate']

        buffering_interval = self.node_params['arduino']['buffering_interval']

        self.serial = Serial(self, port, baud_rate)
        self.buffer = SerialEventBuffer(self.ARDUINO_PROTOCOL, self.serial, buffering_interval)

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

    @staticmethod
    def process_serial_event(event):
        # Error because events should not be received from the arduino
        logger.error(event)

    @event(filter={'category': 'configure_channel_color'})
    def event_configure_channel_color(self, channel: int, rate: int):
        logger.info("Configuring channel {} with rate {}".format(channel, rate))
        self.buffer.send_event(
            base_event={
                self.ARDUINO_PROTOCOL.CATEGORY: self.ARDUINO_PROTOCOL.SET_COLOR,
                self.ARDUINO_PROTOCOL.COLOR: rate,
            },
            channel=channel,
        )

    @event(filter={'category': 'on'})
    def event_on(self, color):
        logger.info("Turning on {}".format(color))
        for on_off_pin in self.colors[color]['on_off_pins']:
            self.on_off_pins[on_off_pin].on()

    @event(filter={'category': 'off'})
    def event_off(self, color):
        logger.info("Turning off {}".format(color))
        for on_off_pin in self.colors[color]['on_off_pins']:
            self.on_off_pins[on_off_pin].off()

    @event(filter={'category': 'play_animation'})
    def event_play_animation(self):
        pass
