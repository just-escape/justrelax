import time

from gpiozero import OutputDevice, InputDevice

from twisted.internet.reactor import callLater

from justrelax.core.logging_utils import logger
from justrelax.core.node import MagicNode, on_event


class Cell:
    def __init__(self, name, pin, deactivation_delay, on_toggle):
        self.name = name
        self.deactivation_delay = deactivation_delay
        self.is_activated = False
        self.deactivation_task = None
        self.on_toggle = on_toggle
        self.pin = pin
        self.device = InputDevice(self.pin)

        callLater(0, self.check_myself)

    def check_myself(self):
        callLater(0, self.check_myself)

        is_activated = bool(self.device.value)
        if is_activated is self.is_activated:
            return

        if is_activated:
            logger.info("Cell (pin={}) has been activated".format(self.pin))
            self.on_cell_activation()
        else:
            logger.info("Cell (pin={}) has been deactivated".format(self.pin))
            self.on_cell_deactivation()

    def on_cell_activation(self):
        # Hide oscillations
        if self.deactivation_task and self.deactivation_task.active():
            logger.debug("Canceling {} deactivation".format(self))
            self.deactivation_task.cancel()

        self.is_activated = True
        self.on_toggle(self.name, self.pin, True)

    def on_cell_deactivation(self):
        # Don't notify if a task is already planned
        if self.deactivation_task and self.deactivation_task.active():
            logger.debug("Color {} is already planned to deactivate: skipping".format(self))
            return

        self.is_activated = False
        self.deactivation_task = callLater(self.deactivation_delay, self._deactivate)

    def _deactivate(self):
        self.on_toggle(self.name, self.pin, False)


class LoadCells(MagicNode):
    def __init__(self, *args, **kwargs):
        super(LoadCells, self).__init__(*args, **kwargs)
        self.cells = []

        self.calibration_pins = [OutputDevice(calibration_pin) for calibration_pin in self.config['calibration_pins']]
        for calibration_pin in self.calibration_pins:
            calibration_pin.off()

    def on_first_connection(self):
        deactivation_delay = self.config['deactivation_delay']

        for pin, color in self.config['cells'].items():
            self.cells.append(Cell(color, pin, deactivation_delay, self.notify))

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
