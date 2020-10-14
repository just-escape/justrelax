from gpiozero import Button

from twisted.internet.reactor import callLater

from justrelax.common.logging_utils import logger
from justrelax.node.service import JustSockClientService


class SokobanControls(JustSockClientService):
    def __init__(self, *args, **kwargs):
        super(SokobanControls, self).__init__(*args, **kwargs)
        self.controls = [
            {
                'name': 'left',
                'input': Button(self.node_params['left_pin']),
                'was_pressed_last_time': False,
            },
            {
                'name': 'right',
                'input': Button(self.node_params['right_pin']),
                'was_pressed_last_time': False,
            },
            {
                'name': 'up',
                'input': Button(self.node_params['up_pin']),
                'was_pressed_last_time': False,
            },
            {
                'name': 'down',
                'input': Button(self.node_params['down_pin']),
                'was_pressed_last_time': False,
            },
            {
                'name': 'reset',
                'input': Button(self.node_params['reset_pin']),
                'was_pressed_last_time': False,
            },
        ]

        self.check_inputs()

    def check_inputs(self):
        callLater(0, self.check_inputs)
        for control in self.controls:
            if control['input'].is_pressed != control['was_pressed_last_time']:
                control['was_pressed_last_time'] = control['input'].is_pressed
                verb = 'pressed' if control['input'].is_pressed else 'released'
                logger.info('{} button has been {}'.format(control['name'], verb))
                self.send_event(
                    {
                        'category': 'control',
                        'name': control['name'],
                        'pressed': control['input'].is_pressed,
                    }
                )
