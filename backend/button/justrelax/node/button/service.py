import time
from threading import Event

try:
    from RPi import GPIO
except RuntimeError:
    from mock import MagicMock
    GPIO = MagicMock()

from twisted.internet import reactor

from justrelax.node.service import JustSockNodeClientService


class Button(JustSockNodeClientService):
    PIN = 14

    class PROTOCOL:
        PRESS = 'press'
        RELEASE = 'release'

    def listen(self, stop_event):
        pin = self.PIN
        last_state = 0

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

        while not stop_event.is_set():
            state = GPIO.input(pin)

            if state != last_state:
                last_state = state
                message = self.PROTOCOL.PRESS if state == 1 else self.PROTOCOL.RELEASE
                reactor.callFromThread(self.factory.send_message, message)

            time.sleep(0.1)

        GPIO.cleanup()

    def start(self):
        stop_event = Event()
        reactor.callInThread(self.listen, stop_event)
        reactor.addSystemEventTrigger('before', 'shutdown', stop_event.set)
