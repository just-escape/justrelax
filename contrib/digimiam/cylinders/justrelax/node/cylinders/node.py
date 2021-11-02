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

        self.check_availability_scan_delay = self.config['check_availability_scan_delay']
        self.check_availability_off_delay = self.config['check_availability_off_delay']
        self.ingredients = self.config['ingredients']

        self.post_success_task = None

        self.check_availability_tasks = []

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
        if self.slots[global_reader_index]['current_tag'] and serialized_tag is None:
            # Delay only if a tag is removed, because this kind of reaction is acceptable if delayed for several seconds
            delay = self.delay
        else:
            delay = 0

        if self.slots[global_reader_index]['delayed_task'] and self.slots[global_reader_index]['delayed_task'].active():
            self.slots[global_reader_index]['delayed_task'].cancel()

        self.slots[global_reader_index]['delayed_task'] = reactor.callLater(
            delay, self.confirm_tag, serialized_tag, global_reader_index)

    def confirm_tag(self, tag, global_reader_index):
        self.update_leds()
        if self.slots[global_reader_index]['current_tag'] != tag:
            self.slots[global_reader_index]['current_tag'] = tag
            self.publish({'category': 'tag', 'tag': tag, 'chamber': global_reader_index})

    @on_event(filter={'category': 'reset'})
    def event_reset(self):
        logger.info("Reset")
        self.success = False
        self.difficulty = "normal"
        if self.post_success_task and self.post_success_task.active():
            self.post_success_task.cancel()

        for check_availability_task in self.check_availability_tasks:
            if check_availability_task and check_availability_task.active():
                check_availability_task.cancel()
        self.check_availability_tasks = []

        self.update_leds()

    @on_event(filter={'category': 'set_difficulty'})
    def event_set_difficulty(self, difficulty):
        self.difficulty = difficulty
        self.update_leds()

    def update_leds(self):
        if self.success:
            return

        logger.info("updating leds")

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

            if all([slot['current_tag'] == slot['expected_tag'] for slot in self.slots.values()]):
                self.success = True
                self.post_success_task = reactor.callLater(10, self.turn_off_all_led)
                self.notify_success()

        else:
            if all([slot['current_tag'] == slot['expected_tag'] for slot in self.slots.values()]):
                for slot in self.slots.values():
                    slot['green_led'].on()
                    slot['red_led'].off()

                    if not self.success:
                        self.success = True
                        self.post_success_task = reactor.callLater(10, self.turn_off_all_led)
                        self.notify_success()

            elif all([slot['current_tag'] is not None for slot in self.slots.values()]):
                for slot in self.slots.values():
                    slot['green_led'].off()
                    slot['red_led'].on()

            else:
                for slot in self.slots.values():
                    slot['green_led'].off()
                    slot['red_led'].off()

    def turn_off_all_led(self):
        logger.info("Turning off all led")
        for slot in self.slots.values():
            slot['green_led'].off()
            slot['red_led'].off()

    def notify_success(self):
        self.publish({"category": "success"})

    @on_event(filter={'category': 'check_availability'})
    def event_check_availability(self, id: str):
        if id not in self.ingredients:
            logger.error(f"Unknown recipe {id}: ignoring")
            return

        self.turn_off_all_led()

        for check_availability_task in self.check_availability_tasks:
            if check_availability_task and check_availability_task.active():
                check_availability_task.cancel()
        self.check_availability_tasks = []

        available_ingredients = []

        def animate_and_check(step, ingredients):
            # There are len(ingredients) + 1 steps, the last one being used to turn off the last led

            if step > 0:
                last_cylinder_id = ingredients[step - 1]

                self.check_availability_tasks.append(reactor.callLater(
                    self.check_availability_off_delay, self.slots[last_cylinder_id]['green_led'].off))
                self.check_availability_tasks.append(reactor.callLater(
                    self.check_availability_off_delay, self.slots[last_cylinder_id]['red_led'].off))

            if step < len(ingredients):
                cylinder_id = ingredients[step]

                is_available = self.slots[cylinder_id]['current_tag'] == self.slots[cylinder_id]['expected_tag']
                available_ingredients.append(is_available)

                logger.info(f"{cylinder_id} available={is_available}")

                if is_available:
                    self.slots[cylinder_id]['green_led'].on()
                else:
                    self.slots[cylinder_id]['red_led'].on()
                self.publish({
                    'category': 'check_availability_scan',
                    'id': id,
                    'cylinder_id': cylinder_id,
                    'is_available': is_available,
                })

                self.check_availability_tasks.append(reactor.callLater(
                    self.check_availability_scan_delay, animate_and_check, step + 1, ingredients))

            else:
                self.publish({
                    'category': 'availability',
                    'missing_ingredients': available_ingredients.count(False),
                    'id': id,
                })

        animate_and_check(0, self.ingredients[id])
