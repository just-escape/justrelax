from justrelax.common.logging_utils import logger
from justrelax.node.service import JustSockClientService
from justrelax.node.helper import Serial


class LoadCells(JustSockClientService):
    def __init__(self, *args, **kwargs):
        super(LoadCells, self).__init__(*args, **kwargs)

        self.serials = []
        self.colors = {}
        for serial_index, serial_conf in enumerate(self.node_params['serials']):
            serial = Serial(
                self, serial_conf['port'], serial_conf['baud_rate'],
                getattr(self, '_on_serial_{}_event'.format(serial_index)))
            self.serials.append({'serial': serial, 'conf': serial_conf})

            for cell_index, color in serial_conf['cells'].items():
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
        is_color_activated = self.is_color_activated(color)

        # Only notify in case of diff
        if activation is not is_color_activated:
            self.send_event({'category': 'load_cell', 'color': color, 'activated': activation})

        self.colors[(serial_index, cell_id)] = activation

        # Pink is hardcoded. Don't hit me.
        if color in ['red', 'white']:
            complementary_color = 'red' if color == 'white' else 'white'
            is_complementary_color_activated = self.is_color_activated(complementary_color)
            pink_activation = self.is_color_activated(color) and is_complementary_color_activated

            # Only notify in case of diff
            if pink_activation is not self.is_pink_activated:
                self.send_event({'category': 'load_cell', 'color': 'pink', 'activated': pink_activation})
                self.is_pink_activated = pink_activation

    def is_color_activated(self, color):
        return any(self.colors[color].values())
