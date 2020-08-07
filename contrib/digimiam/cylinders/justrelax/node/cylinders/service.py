import gpiozero

from justrelax.common.logging_utils import logger
from justrelax.node.service import JustSockClientService, EventCategoryToMethodMixin
from justrelax.node.helper import Serial


class Cylinders(EventCategoryToMethodMixin, JustSockClientService):
    class ARDUINO_PROTOCOL:
        CATEGORY = "c"

        READ = "r"
        READER_INDEX = "i"
        TAG = "t"

    def __init__(self, *args, **kwargs):
        super(Cylinders, self).__init__(*args, **kwargs)

        self.success = False
        self.difficulty = 'normal'

        self.serials = []

        for reader in self.node_params.get('readers', []):
            index_mapping = reader['index_mapping']
            port = reader['port']
            baud_rate = reader['baud_rate']
            self.serials.append(Serial(self, port, baud_rate, self.process_serial_event, index_mapping))

        self.slots = {}
        for key, slot in self.node_params['slots'].items():
            red_led = gpiozero.OutputDevice(slot['red_pin'])
            green_led = gpiozero.OutputDevice(slot['green_pin'])
            self.slots[key] = {
                'current_tag': None,
                'expected_tag': slot['expected_tag'],
                'red_led': red_led,
                'green_led': green_led,
            }

    def process_serial_event(self, event, index_mapping):
        logger.debug("Processing event '{}'".format(event))

        if self.ARDUINO_PROTOCOL.CATEGORY not in event:
            logger.error("Event has no category: skipping")
            return

        if event[self.ARDUINO_PROTOCOL.CATEGORY] == self.ARDUINO_PROTOCOL.READ:
            if self.ARDUINO_PROTOCOL.READER_INDEX not in event:
                logger.error("Event has no reader index: skipping")
                return

            if self.ARDUINO_PROTOCOL.TAG not in event:
                logger.error("Event has no tag: skipping")
                return

            local_reader_index = event[self.ARDUINO_PROTOCOL.READER_INDEX]
            global_reader_index = index_mapping.get(local_reader_index, None)
            if global_reader_index is None:
                logger.error("Undeclared local reader index '{}': skipping".format(local_reader_index))
                return
            if global_reader_index not in self.slots:
                logger.error("Undeclared global reader index '{}': skipping".format(global_reader_index))
                return
            tag = event[self.ARDUINO_PROTOCOL.TAG]
            self.on_nfc_read(global_reader_index, tag)

        else:
            logger.error("Unknown event category '{}': skipping".format(self.ARDUINO_PROTOCOL.CATEGORY))

    def event_reset(self):
        self.success = False

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

    def on_nfc_read(self, reader_index, tag):
        serialized_tag = "-".join([str(byte) for byte in tag]) if tag else None
        self.slots[reader_index]['current_tag'] = serialized_tag
        self.update_leds()

    def notify_success(self):
        self.send_event({"category": "success"})
