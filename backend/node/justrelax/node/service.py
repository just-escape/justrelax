import inspect
from copy import deepcopy
from gpiozero import Device
from gpiozero.pins.mock import MockFactory, MockPWMPin

from twisted.application import internet

from justrelax.common.logging_utils import logger
from justrelax.node.factory import JustSockClientFactory


def orchestrator_event(f=None, filter=None):
    def wrapper(f_):
        f_.filter = filter if type(filter) is dict else {}
        return f_

    if f is None:
        return wrapper
    else:
        return wrapper(f)


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

        self.event_callbacks = []
        for attribute_name in dir(self):
            attribute = getattr(self, attribute_name)
            if not callable(attribute):
                continue

            # attribute is a method

            if hasattr(attribute, 'filter'):
                self.event_callbacks.append({'callback': attribute, 'filter': attribute.filter})

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

    def _get_callbacks(self, event):
        callbacks = []

        for callback in self.event_callbacks:
            for key, value in callback['filter'].items():
                if key not in event or event[key] != value:
                    break
            else:
                callbacks.append(callback['callback'])

        return callbacks

    @staticmethod
    def _check_arguments(event, callback):
        callback_arguments = inspect.signature(callback).parameters
        for arg in callback_arguments.values():
            if arg.default is arg.empty:
                # No default value: a value must be defined in the event
                if arg.name not in event:
                    logger.error("Event has no {} field for {}: ignoring".format(arg.name, callback.__name__))
                    return False

                if arg.annotation is not arg.empty:
                    if type(event[arg.name]) is not arg.annotation:
                        logger.error("Event field {} type is not {} (received {}) for {}: ignoring".format(
                            arg.name, arg.annotation, type(event[arg.name]), callback.__name__))
                        return False

        return True

    @staticmethod
    def _get_trimmed_version_for_callback(event, callback):
        copied_event = deepcopy(event)

        for filter_key in callback.filter.keys():
            copied_event.pop(filter_key)

        # This inspection is not 100% proof. Positional only arguments or *args / **kwargs can mess
        # with this logic, but at least it covers a lot of cases.
        callback_arguments = inspect.signature(callback).parameters

        # Cast as a list so that the entire list is defined before we might pop fields.
        # Otherwise we would raise RuntimeError ("dictionary changed size during iteration").
        for field in list(copied_event.keys()):
            if field not in callback_arguments:
                copied_event.pop(field)

        return copied_event

    def _process_event(self, event):
        logger.debug("Processing event '{}'".format(event))
        if type(event) is not dict:
            logger.error("Unknown event: skipping")
            return

        callbacks = self._get_callbacks(event)

        for callback in callbacks:
            if not self._check_arguments(event, callback):
                continue
            trimmed_event = self._get_trimmed_version_for_callback(event, callback)

            callback(**trimmed_event)

        self.process_event(event)

    def process_event(self, event):
        pass

    def send_event(self, event):
        self.factory.send_event(event)
