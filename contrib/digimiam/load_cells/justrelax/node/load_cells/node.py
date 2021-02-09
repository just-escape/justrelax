from gpiozero import InputDevice

from twisted.internet.reactor import callLater

from justrelax.core.logging_utils import logger
from justrelax.core.node import MagicNode


class Cell:
    def __init__(self, pin, on_activation, on_deactivation):
        self.pin = pin
        self.device = InputDevice(pin)
        self.last_state = False

        self.on_activation = on_activation
        self.on_deactivation = on_deactivation

        callLater(0, self.check_myself)

    def check_myself(self):
        callLater(0, self.check_myself)

        is_activated = bool(self.device.value)
        if is_activated is self.last_state:
            return

        self.last_state = is_activated

        if is_activated:
            logger.info("Cell (pin={}) has been activated".format(self.pin))
            self.on_activation()
        else:
            logger.info("Cell (pin={}) has been deactivated".format(self.pin))
            self.on_deactivation()

    def __bool__(self):
        return self.last_state

    def __str__(self):
        return str(self.pin)


class Color:
    def __init__(self, name, deactivation_delay, on_toggle):
        self.name = name
        self.deactivation_delay = deactivation_delay
        self.is_activated = False
        self.deactivation_task = None
        self.cells = []
        self.on_toggle = on_toggle

    def add_cell(self, pin):
        self.cells.append(Cell(pin, self.on_cell_activation, self.on_cell_deactivation))

    def on_cell_activation(self):
        if self.is_activated:
            logger.debug("Color {} is already activated: skipping".format(self))
            return

        # Hide oscillations
        if self.deactivation_task and self.deactivation_task.active():
            logger.debug("Canceling {} deactivation".format(self))
            self.deactivation_task.cancel()

        self.is_activated = True
        self.toggle()

    def on_cell_deactivation(self):
        if not self.is_activated:
            logger.debug("Color {} is already deactivated: skipping".format(self))  # Should not happen often

        else:
            if all([not cell for cell in self.cells]):
                # Don't notify if a task is already planned
                if self.deactivation_task and self.deactivation_task.active():
                    logger.debug("Color {} is already planned to deactivate: skipping".format(self))
                    return

                self.is_activated = False
                self.toggle()

            else:
                logger.debug("Color {} was activated, but some cells remain active: skipping".format(self))

    def toggle(self):
        if self.is_activated:
            self._toggle(self.name, self.is_activated)
        else:
            self.deactivation_task = callLater(self.deactivation_delay, self._toggle, self.name, self.is_activated)

    def _toggle(self, color, activate):
        if activate:
            logger.debug("Activating {}".format(self))
        else:
            logger.debug("Deactivating {}".format(self))

        self.on_toggle(color, activate)

    def __str__(self):
        return str(self.name)


class LoadCells(MagicNode):
    def __init__(self, *args, **kwargs):
        super(LoadCells, self).__init__(*args, **kwargs)

        deactivation_delay = self.config['deactivation_delay']

        self.colors = {}
        for pin, color in self.config['cells'].items():
            if color not in self.colors:
                self.colors[color] = Color(color, deactivation_delay, self.notify)
            self.colors[color].add_cell(pin)

    def notify(self, color, activated):
        self.publish({'category': 'load_cell', 'color': color, 'activated': activated})
