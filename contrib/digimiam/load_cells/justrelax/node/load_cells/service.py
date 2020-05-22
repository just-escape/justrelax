from twisted.internet.reactor import callLater

from justrelax.common.logging_utils import logger
from justrelax.node.service import JustSockClientService
from justrelax.node.helper import Serial


class LoadCells(JustSockClientService):
    def __init__(self, *args, **kwargs):
        super(LoadCells, self).__init__(*args, **kwargs)

        self.deactivation_delay = self.node_params['deactivation_delay']

        self.serials = []
        self.colors = {}
        self.color_deactivation_tasks = {}
        for serial_index, serial_conf in enumerate(self.node_params['serials']):
            serial = Serial(
                self, serial_conf['port'], serial_conf['baud_rate'],
                getattr(self, '_on_serial_{}_event'.format(serial_index)))
            self.serials.append({'serial': serial, 'conf': serial_conf})

            for cell_index, color in serial_conf['cells'].items():
                if color not in self.color_deactivation_tasks:
                    self.color_deactivation_tasks[color] = None

                if color not in self.colors:
                    self.colors[color] = {}
                self.colors[color][(serial_index, cell_index)] = False

        self.is_pink_activated = False

    def _on_serial_0_event(self, event):
        self.on_serial_x_event(event, 0)

    def _on_serial_1_event(self, event):
        self.on_serial_x_event(event, 1)

    def _on_serial_2_event(self, event):
        self.on_serial_x_event(event, 2)

    def _on_serial_3_event(self, event):
        self.on_serial_x_event(event, 3)

    def on_serial_x_event(self, event, serial_index):
        if event['c'] != 'm':
            logger.warning("Unknown event {}: ignoring".format(event))
            return

        if 'i' not in event:
            logger.warning("Event {} has no cell id: ignoring".format(event))
            return

        if 'v' not in event:
            logger.warning("Event {} has no value: ignoring".format(event))
            return

        cell_id = event['i']
        value = event['v']

        threshold = self.serials[serial_index]['conf']['threshold']
        color = self.serials[serial_index]['conf']['cells'][cell_id]

        activation = value > threshold
        logger.debug("Serial={}, cell_id={}, value={}, threshold={}".format(serial_index, cell_id, value, threshold))
        is_color_activated = self.is_color_activated(color)

        if activation:
            # Hide oscillations
            if self.color_deactivation_tasks[color] and self.color_deactivation_tasks[color].active():
                logger.debug("Canceling {} deactivation".format(color))
                self.color_deactivation_tasks[color].cancel()
        else:
            # Don't notify if a task is already planned
            if self.color_deactivation_tasks[color] and self.color_deactivation_tasks[color].active():
                return

        # Only notify in case of diff
        if activation is not is_color_activated:
            self.toggle(color, activation, (serial_index, cell_id))

    def toggle(self, color, activate, key):
        if activate:
            self._toggle(color, activate, key)
        else:
            logger.debug("Scheduling {} deactivation".format(color))
            self.color_deactivation_tasks[color] = callLater(
                self.deactivation_delay, self._toggle, color, activate, key)

    def _toggle(self, color, activate, key):
        if activate:
            logger.debug("Activating {}".format(color))
        else:
            logger.debug("Deactivating {}".format(color))

        self.send_event({'category': 'load_cell', 'color': color, 'activated': activate})
        self.colors[color][key] = activate

        # Pink is hardcoded. Don't hit me.
        if color in ['red', 'white']:
            complementary_color = 'red' if color == 'white' else 'white'
            is_complementary_color_activated = self.is_color_activated(complementary_color)
            pink_activation = self.is_color_activated(color) and is_complementary_color_activated

            # Only notify in case of diff
            if pink_activation is not self.is_pink_activated:
                if pink_activation:
                    logger.debug("Activating pink")
                else:
                    logger.debug("Deactivating pink")

                self.send_event({'category': 'load_cell', 'color': 'pink', 'activated': activate})
                self.is_pink_activated = activate

    def is_color_activated(self, color):
        return any(self.colors[color].values())
