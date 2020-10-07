from twisted.internet import reactor

from gpiozero import OutputDevice, InputDevice

from justrelax.common.logging_utils import logger
from justrelax.node.helper import Serial
from justrelax.node.service import JustSockClientService, EventCategoryToMethodMixin


class Cell:
    def __init__(self, pin, on_toggle, led_strip):
        self.pin = pin
        self.device = InputDevice(pin)
        self.last_state = False

        self.on_toggle = on_toggle
        self.led_strip = led_strip

        reactor.callLater(0, self.check_myself)

    def check_myself(self):
        reactor.callLater(0, self.check_myself)

        is_activated = bool(self.device.value)
        if is_activated is self.last_state:
            return

        self.last_state = is_activated

        if is_activated:
            logger.info("Cell (pin={}, led_strip={}) has been activated".format(self.pin, self.led_strip))
            self.on_toggle(True, self.led_strip)
        else:
            logger.info("Cell (pin={}, led_strip={}) has been deactivated".format(self.pin, self.led_strip))
            self.on_toggle(False, self.led_strip)

    def __bool__(self):
        return self.last_state

    def __str__(self):
        return str(self.pin)


class SecureFloor(EventCategoryToMethodMixin, JustSockClientService):
    class ARDUINO_PROTOCOL:
        CATEGORY = 'c'

        SET_COLOR_BLACK = 'b'
        SET_COLOR_ORANGE = 'o'
        SET_COLOR_RED = 'r'
        SET_COLOR_WHITE = 'w'
        STRIP_BIT_MASK = 's'

    STATUSES = {'playing', 'alarm'}

    def __init__(self, *args, **kwargs):
        super(SecureFloor, self).__init__(*args, **kwargs)

        port = self.node_params['leds']['arduino']['port']
        baud_rate = self.node_params['leds']['arduino']['baud_rate']

        self.serial = Serial(self, port, baud_rate)

        self.status = 'playing'
        self.success = False

        self.clear_alarm_delay = self.node_params['clear_alarm_delay']
        self.clear_alarm_task = None

        self.tare = OutputDevice(self.node_params['load_cells']['tare_pin'])
        self.tare.off()

        self.leds = {}
        self.cells = []
        for cell in self.node_params['load_cells']['cells']:
            self.cells.append((Cell(cell['pin'], self.on_load_cell_toggle, cell['led_strip'])))

            if cell['led_strip']:
                self.leds[cell['led_strip']] = 'black'

        # Init once we are sure the serial port will be able to receive data
        self.reactor.callLater(3, self.set_led_color, "black", sum(self.leds.keys()))

    def process_serial_event(self, event):
        # Error by default because events should not be received from the arduino
        logger.error(event)
        self.send_event(event)

    def set_led_color(self, color, bit_mask):
        logger.info("Setting led bit_mask={} color={}".format(bit_mask, color))

        color_mapping = {
            'orange': self.ARDUINO_PROTOCOL.SET_COLOR_ORANGE,
            'red': self.ARDUINO_PROTOCOL.SET_COLOR_RED,
            'white': self.ARDUINO_PROTOCOL.SET_COLOR_WHITE,
        }

        event_color = color_mapping.get(color, self.ARDUINO_PROTOCOL.SET_COLOR_BLACK)

        self.serial.send_event({
            self.ARDUINO_PROTOCOL.CATEGORY: event_color,
            self.ARDUINO_PROTOCOL.STRIP_BIT_MASK: bit_mask,
        })

    def event_set_led_color(self, color: str, bit_mask: int):
        self.set_led_color(color, bit_mask)

    def event_set_all_leds_color(self, color: str):
        self.set_led_color(color, sum(self.leds.keys()))

    def event_tare(self):
        logger.info("Triggering tare rising edge...")
        self.tare.on()

        def event_tare_falling_edge():
            logger.info("Triggering tare falling edge...")
            self.tare.off()

        reactor.callLater(1, event_tare_falling_edge)

    def event_reset(self):
        logger.info("Resetting node")
        self.success = False
        self.set_led_color("black", sum(self.leds.keys()))
        self.event_tare()
        self.event_set_status('playing')

    def event_set_status(self, status: str):
        if self.success is False:
            if status in self.STATUSES:
                logger.info("Setting status to '{}'".format(status))
                self.status = status
                if status == 'alarm':
                    self.event_set_led_color(
                        'red',
                        sum(led_strip for led_strip, led_color in self.leds.items() if led_color != 'black'))

            else:
                logger.info("Unknown status '{}': skipping".format(status))
        else:
            logger.info("Node is in success mode: ignoring set status to '{}'".format(status))

    def event_success(self):
        if self.success is False:
            logger.info("Setting node in success mode")
            self.success = True
            self.event_set_all_leds_color('white')

    def _clear_alarm(self):
        self.event_set_status('playing')
        self.event_set_led_color(
            'orange',
            sum(led_strip for led_strip, led_color in self.leds.items() if led_color != 'black'))
        self.notify_clear()

    def notify_clear(self):
        self.send_event({'category': 'clear'})

    def on_load_cell_toggle(self, activated, led_strip):
        if self.success:
            return

        if self.status == 'playing':
            if activated and led_strip and self.leds[led_strip] == 'black':
                self.event_set_led_color('orange', led_strip)

        if self.status == 'alarm':
            if activated:
                if self.clear_alarm_task and self.clear_alarm_task.active():
                    logger.info("Cancelling clear alarm task")
                    self.clear_alarm_task.cancel()
            else:
                if all(not c for c in self.cells):  # If all cells are deactivated
                    self.clear_alarm_task = reactor.callLater(self.clear_alarm_delay, self._clear_alarm)
