try:
    from RPi import GPIO
    from pirc522 import RFID
except RuntimeError:
    from mock import MagicMock
    GPIO = MagicMock()
    pirc522 = MagicMock()

from twisted.internet import reactor
from twisted.internet.task import LoopingCall

from justrelax.node.service import JustSockClientService


class FloppyReader(JustSockClientService):
    def start(self):
        self.rst_pin_cycle = []
        self.current_rst_pin_index = -1

        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)

        for pin in self.node_params['rst_pins']:
            self.rst_pin_cycle.append(pin)
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)
        print(self.rst_pin_cycle)

        self.rc522_reader = RFID()

        read_loop = LoopingCall(self.cyclic_read)
        read_loop.start(1 / 100)

        reactor.addSystemEventTrigger('before', 'shutdown', GPIO.cleanup)

    def cycle_rst_pin(self):
        self.current_rst_pin_index = (self.current_rst_pin_index + 1) % len(self.rst_pin_cycle)
        return self.rst_pin_cycle[self.current_rst_pin_index]

    def cyclic_read(self):
        current_rst_pin = self.cycle_rst_pin()

        GPIO.output(current_rst_pin, GPIO.HIGH)
        self.rc522_reader.init()

        request_error, _ = self.rc522_reader.request()
        if request_error:
            self.read_callback(self.current_rst_pin_index, None)
        else:
            anticoll_error, nfc_uid = self.rc522_reader.anticoll()
            if anticoll_error:
                self.read_callback(self.current_rst_pin_index, None)
            else:
                self.read_callback(self.current_rst_pin_index, nfc_uid)

        GPIO.output(current_rst_pin, GPIO.LOW)

    def read_callback(self, reader_index, nfc_uid):
        print("reader_index={}, nfc_uid={}".format(reader_index, nfc_uid))
