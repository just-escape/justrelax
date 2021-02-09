import gpiozero

from twisted.internet import reactor

from justrelax.core.logging_utils import logger
from justrelax.core.node import MagicNode, on_event


class ArduinoProtocol:
    CATEGORY = "c"

    READ = "r"
    READER_INDEX = "i"
    TAG = "t"


class Cylinders(MagicNode):
    def __init__(self, *args, **kwargs):
        super(Cylinders, self).__init__(*args, **kwargs)

        self.success = False
        self.difficulty = 'normal'
        self.delay = self.config['delay']

        self.index_mapping = self.config['index_mapping']

        self.slots = {}
        for key, slot in self.config['slots'].items():
            red_led = gpiozero.OutputDevice(slot['red_pin'])
            green_led = gpiozero.OutputDevice(slot['green_pin'])
            self.slots[key] = {
                'current_tag': None,
                'expected_tag': slot['expected_tag'],
                'red_led': red_led,
                'green_led': green_led,
                'delayed_task': None,
            }

    @on_event(filter={ArduinoProtocol.CATEGORY: ArduinoProtocol.READ})
    def serial_event_read(self, port, /, i: int, t):
        reader_index = i
        tag = t

        global_reader_index = self.index_mapping[port].get(reader_index, None)

        if global_reader_index is None:
            logger.warning("Undeclared local reader index '{}' for port {}: skipping".format(reader_index, port))
            return

        if global_reader_index not in self.slots:
            logger.warning("Undeclared global reader index '{}': skipping".format(global_reader_index))
            return

        serialized_tag = "-".join([str(byte) for byte in tag]) if tag else None
        self.slots[global_reader_index]['current_tag'] = serialized_tag

        if self.slots[global_reader_index]['delayed_task'] and self.slots[global_reader_index]['delayed_task'].active():
            self.slots[global_reader_index]['delayed_task'].cancel()

        self.slots[global_reader_index]['delayed_task'] = reactor.callLater(self.delay, self.update_leds)

    @on_event(filter={'category': 'reset'})
    def event_reset(self):
        self.success = False

    @on_event(filter={'category': 'set_difficulty'})
    def event_set_difficulty(self, difficulty):
        self.difficulty = difficulty
        self.update_leds()

    def update_leds(self):
        if self.difficulty == 'easy':
            for slot in self.slots.values():
                if slot['current_tag'] == slot['expected_tag']:
                    slot['green_led'].on()
                    slot['red_led'].off()
                elif slot['current_tag'] is not None:
                    slot['green_led'].off()
                    slot['red_led'].on()
                else:
                    slot['green_led'].off()
                    slot['red_led'].off()

        else:
            if all([slot['current_tag'] == slot['expected_tag'] for slot in self.slots.values()]):
                for slot in self.slots.values():
                    slot['green_led'].on()
                    slot['red_led'].off()

                    if not self.success:
                        self.success = True
                        self.notify_success()

            elif all([slot['current_tag'] is not None for slot in self.slots.values()]):
                for slot in self.slots.values():
                    slot['green_led'].off()
                    slot['red_led'].on()

            else:
                for slot in self.slots.values():
                    slot['green_led'].off()
                    slot['red_led'].off()

    def notify_success(self):
        self.publish({"category": "success"})
