import time

from gpiozero import OutputDevice, InputDevice

from twisted.internet.reactor import callLater

from justrelax.core.logging_utils import logger
from justrelax.core.node import MagicNode, on_event


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
            self.on_activation(self.pin)
        else:
            logger.info("Cell (pin={}) has been deactivated".format(self.pin))
            self.on_deactivation(self.pin)

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

    def on_cell_activation(self, pin):
        if self.is_activated:
            logger.debug("Color {} is already activated: skipping".format(self))
            return

        # Hide oscillations
        if self.deactivation_task and self.deactivation_task.active():
            logger.debug("Canceling {} deactivation".format(self))
            self.deactivation_task.cancel()

        self.is_activated = True
        self.toggle(pin)

    def on_cell_deactivation(self, pin):
        if not self.is_activated:
            logger.debug("Color {} is already deactivated: skipping".format(self))  # Should not happen often

        else:
            if all([not cell for cell in self.cells]):
                # Don't notify if a task is already planned
                if self.deactivation_task and self.deactivation_task.active():
                    logger.debug("Color {} is already planned to deactivate: skipping".format(self))
                    return

                self.is_activated = False
                self.toggle(pin)

            else:
                logger.debug("Color {} was activated, but some cells remain active: skipping".format(self))

    def toggle(self, pin):
        if self.is_activated:
            self._toggle(self.name, pin, self.is_activated)
        else:
            self.deactivation_task = callLater(
                self.deactivation_delay, self._toggle, self.name, pin, self.is_activated)

    def _toggle(self, color, pin, activate):
        if activate:
            logger.debug("Activating {}".format(self))
        else:
            logger.debug("Deactivating {}".format(self))

        self.on_toggle(color, pin, activate)

    def __str__(self):
        return str(self.name)


class LoadCells(MagicNode):
    def __init__(self, *args, **kwargs):
        super(LoadCells, self).__init__(*args, **kwargs)
        self.colors = {}

        self.calibration_pins = [OutputDevice(calibration_pin) for calibration_pin in self.config['calibration_pins']]
        for calibration_pin in self.calibration_pins:
            calibration_pin.off()

    def on_first_connection(self):
        deactivation_delay = self.config['deactivation_delay']

        for pin, color in self.config['cells'].items():
            if color not in self.colors:
                self.colors[color] = Color(color, deactivation_delay, self.notify)
            self.colors[color].add_cell(pin)

    def notify(self, color, id_, activated):
        self.publish({'category': 'load_cell', 'color': color, 'id': id_, 'activated': activated})

    @on_event(filter={'category': 'calibrate'})
    def event_calibrate(self):
        logger.info("Calibration sensors")

        logger.info("Triggering calibration rising edges...")
        for calibration_pin in self.calibration_pins:
            calibration_pin.on()

        # Blocking sleep (no reactor.callLater), because load cell pins will not behave deterministically during this
        # operation. It has not a huge impact on the whole system, and this way, in the hypothetical case in which
        # players toggle cells states (on/off), it should be transparent after the sleep.
        time.sleep(5)

        logger.info("Triggering calibration falling edges...")
        for calibration_pin in self.calibration_pins:
            calibration_pin.off()
