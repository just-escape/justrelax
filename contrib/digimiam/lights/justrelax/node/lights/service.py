from twisted.internet import reactor

from gpiozero import OutputDevice

from justrelax.common.logging_utils import logger
from justrelax.node.helper import Serial
from justrelax.node.service import JustSockClientService, orchestrator_event


class ArduinoProtocol:
    CATEGORY = 'c'

    CHANNEL = 'h'
    SET_COLOR = 's'
    COLOR = 'r'


class LightsSerialBuffer:
    def __init__(self, buffering_interval):
        self.buffering_interval = buffering_interval

        self.queue = []

        self.delay_task = None

    def send_event(self, event):
        if self.delay_task and self.delay_task.active():
            self.queue_event(event)

        else:
            self._send_event(event)
            self.delay_task = reactor.callLater(self.buffering_interval, self.pop_event)

    def pop_event(self):
        if not self.queue:
            return

        split_event = self.queue.pop(0)
        event = split_event['base_event']
        event[ArduinoProtocol.CHANNEL] = sum(split_event['channel'])

        self._send_event(event)
        self.delay_task = reactor.callLater(self.buffering_interval, self.pop_event)

    def queue_event(self, event):
        channel = event.pop(ArduinoProtocol.CHANNEL)

        for queued_event in self.queue:
            if queued_event['base_event'] == event:
                queued_event['channel'].add(channel)
                return

        else:
            self.queue.append(
                {
                    'base_event': event,
                    'channel': {channel},
                }
            )


class LightsBufferedSerial(LightsSerialBuffer, Serial):
    def __init__(self, service, port, baud_rate=9600, buffering_interval=0.1):
        LightsSerialBuffer.__init__(self, buffering_interval)
        Serial.__init__(self, service, port, baud_rate)


class Lights(JustSockClientService):
    def __init__(self, *args, **kwargs):
        super(Lights, self).__init__(*args, **kwargs)

        self.colors = {}
        self.on_off_pins = {}

        port = self.node_params['arduino']['port']
        baud_rate = self.node_params['arduino']['baud_rate']

        buffering_interval = self.node_params['arduino']['buffering_interval']

        self.serial = LightsBufferedSerial(self, port, baud_rate, buffering_interval)
        self.serial.process_event = self.process_serial_event

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

    @orchestrator_event(filter={'category': 'configure_channel_color'})
    def event_configure_channel_color(self, channel: int, rate: int):
        logger.info("Configuring channel {} with rate {}".format(channel, rate))
        self.serial.send_event(
            {
                ArduinoProtocol.CATEGORY: ArduinoProtocol.SET_COLOR,
                ArduinoProtocol.CHANNEL: channel,
                ArduinoProtocol.COLOR: rate,
            }
        )

    @orchestrator_event(filter={'category': 'on'})
    def event_on(self, color):
        logger.info("Turning on {}".format(color))
        for on_off_pin in self.colors[color]['on_off_pins']:
            self.on_off_pins[on_off_pin].on()

    @orchestrator_event(filter={'category': 'off'})
    def event_off(self, color):
        logger.info("Turning off {}".format(color))
        for on_off_pin in self.colors[color]['on_off_pins']:
            self.on_off_pins[on_off_pin].off()

    @orchestrator_event(filter={'category': 'play_animation'})
    def event_play_animation(self):
        pass
