from gpiozero import Device
from gpiozero.pins.mock import MockFactory, MockPWMPin

from twisted.application import internet

from justrelax.common.logging_utils import logger
from justrelax.node.factory import JustSockClientFactory


class JustSockClientService(internet.TCPClient):
    def __init__(self, host, port, name, channel, environment, node_params, *args, **kwargs):
        self.host = host
        self.port = port
        self.name = name

        self.factory = JustSockClientFactory(self, name, channel)

        self.node_params = node_params

        if environment != "rpi":
            Device.pin_factory = MockFactory()
            Device.pin_factory.pin_class = MockPWMPin

        super(JustSockClientService, self).__init__(host, port, self.factory, *args, **kwargs)

    def startService(self):
        logger.info("Starting node '{}' on '{}:{}'".format(self.name, self.host, self.port))
        self.start()
        super(JustSockClientService, self).startService()

    def start(self):
        pass

    def stopService(self):
        self.stop()
        super(JustSockClientService, self).stopService()

    def stop(self):
        pass

    def process_event(self, event):
        pass
