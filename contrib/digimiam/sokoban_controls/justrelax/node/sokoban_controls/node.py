from gpiozero import Button

from twisted.internet.reactor import callLater

from justrelax.core.logging_utils import logger
from justrelax.core.node import MagicNode


class SokobanControls(MagicNode):
    def __init__(self, *args, **kwargs):
        super(SokobanControls, self).__init__(*args, **kwargs)
        self.controls = [
            {
                'name': 'left',
                'input': Button(self.config['left_pin']),
                'was_pressed_last_time': False,
            },
            {
                'name': 'right',
                'input': Button(self.config['right_pin']),
                'was_pressed_last_time': False,
            },
            {
                'name': 'up',
                'input': Button(self.config['up_pin']),
                'was_pressed_last_time': False,
            },
            {
                'name': 'down',
                'input': Button(self.config['down_pin']),
                'was_pressed_last_time': False,
            },
            {
                'name': 'reset',
                'input': Button(self.config['reset_pin']),
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
                self.publish(
                    {
                        'category': 'control',
                        'name': control['name'],
                        'pressed': control['input'].is_pressed,
                    }
                )
