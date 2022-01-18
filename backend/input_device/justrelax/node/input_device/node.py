import gpiozero

from twisted.internet import reactor

from justrelax.core.node import MagicNode, on_event
from justrelax.core.logging_utils import logger


class InputDevice(MagicNode):
    def __init__(self, *args, **kwargs):
        super(InputDevice, self).__init__(*args, **kwargs)

        pin = self.config["pin"]
        self.name = self.config['name']
        pull_up = self.config.get('pull_up', False)
        self.device = gpiozero.InputDevice(pin, pull_up=pull_up)
        self.device_state = self.device.is_active

        self.check_myself()

    def check_myself(self):
        reactor.callLater(0.01, self.check_myself)
        new_device_state = self.device.is_active
        has_state_changed = new_device_state != self.device_state
        if has_state_changed:
            self.publish({'category': 'state_change', 'state': device_state})
            self.device_state = device_state

        return has_state_changed


class PersistentInputDevice(InputDevice):
    def check_myself(self):
        has_state_changed = super().check_myself()
        if has_state_changed:
            self.publish_session_data()

    @on_event(filter={'category': 'request_node_session_data'})
    def publish_session_data(self):
        self.publish(
            {
                'category': 'set_session_data',
                'key': self.name,
                'data': self.device_state,
            }
        )
