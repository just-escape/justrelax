import inspect
from copy import deepcopy
from gpiozero import Device
from gpiozero.pins.mock import MockFactory, MockPWMPin

from twisted.application import internet

from justrelax.common.logging_utils import logger
from justrelax.node.factory import PublishSubscribeClientFactory


def on_event(f=None, channel=..., filter=None):
    def wrapper(f_):
        f_.on_event_callback = True
        f_.channel = channel
        f_.filter = filter if isinstance(filter, dict) else {}
        return f_

    if f is None:
        return wrapper
    else:
        return wrapper(f)


class EventFilterMixin:
    def __init__(self):
        self._event_callbacks = []
        self._gather_event_callbacks()

    def _gather_event_callbacks(self):
        for attribute_name in dir(self):
            attribute = getattr(self, attribute_name)
            if not callable(attribute):
                continue

            # attribute is a method

            if not hasattr(attribute, 'on_event_callback'):
                continue

            inspection_data = self._get_callback_inspection_data(attribute)
            self._event_callbacks.append(inspection_data)

    def _get_callback_inspection_data(self, callable):
        callback_parameters = inspect.signature(callable).parameters
        inspection_data = {
            'callable': callable,
            'filter': callable.filter,
            'pass_channel': False,
            'variable_kwargs': False,
            'kwargs': {},
        }

        # This inspection is not 100% proof. Positional only arguments or cases that I would not think about can mess
        # with this logic, but at least it covers a lot of cases.

        for param in callback_parameters.values():
            if param.kind == param.POSITIONAL_ONLY:
                if not inspection_data['pass_channel']:
                    inspection_data['pass_channel'] = True
                else:
                    logger.error(
                        "Multiple positional only parameters detected in {}. Only one for the channel is "
                        "supported.".format(callable.__name__))

            elif param.kind == param.VAR_KEYWORD:
                # If there is one variable keyword argument in the signature, we don't need to check if some event
                # fields need to be popped, we already know we can pass all kwargs
                inspection_data['variable_kwargs'] = True

            elif param.kind == param.POSITIONAL_OR_KEYWORD:
                inspection_data['kwargs'][param.name] = {
                    'required': param.default is param.empty,
                    'annotation': ... if param.annotation is param.empty else param.annotation
                }

            else:
                # Only inspect._ParameterKind.VAR_POSITIONAL left, but variable positional arguments are not used
                pass

        return inspection_data

    def _get_callbacks(self, event, channel):
        callbacks = []

        for callback in self._event_callbacks:
            if channel is not ... or channel != callback['channel']:
                continue

            for key, value in callback['filter'].items():
                if key not in event or event[key] != value:
                    break
            else:
                callbacks.append(callback)

        return callbacks

    @staticmethod
    def _get_args_for_callback(event, channel, callback):
        args = (channel,) if callback['pass_channel'] else ()

        if callback['variable_kwargs']:
            kwargs = event
        else:
            kwargs = {k: v for k, v in event.items() if k in callback['kwargs']}

        for callback_kwarg in callback['kwargs']:
            if callback_kwarg in kwargs:
                annotation = callback['kwargs'][callback_kwarg]['annotation']
                if not isinstance(kwargs[callback_kwarg], annotation):
                    raise ValueError("Event field {} type is not {} (received={})".format(
                        callback_kwarg, annotation, kwargs[callback_kwarg]))

            else:
                if callback['kwargs'][callback_kwarg]['required']:
                    raise ValueError("Event has no {} field, which is a required attribute".format(callback_kwarg))

        return args, kwargs

    def process_event(self, event, channel):
        if isinstance(event, dict):
            callbacks = self._get_callbacks(event, channel)

            for callback in callbacks:
                try:
                    args, kwargs = self._get_args_for_callback(event, channel, callback)
                except ValueError as e:
                    logger.error("Could not execute callback {} ({}): ignoring".format(callback.__name__, e))
                    continue

                callback['callable'](*args, **kwargs)

        else:
            # The event parameter has not been verified. This code is not really safe but it handles the case...
            if callback['pass_channel']:
                callback['callable'](channel, event)
            else:
                callback['callable'](event)


class Node(internet.TCPClient):
    def __init__(self, host, port, name, subscriptions, node_params, *args, **kwargs):
        self.host = host
        self.port = port
        self.name = name

        self.factory = PublishSubscribeClientFactory(self, subscriptions)

        self.node_params = node_params

        super(Node, self).__init__(host, port, self.factory, *args, **kwargs)

    def startService(self):
        logger.info("Starting node {} on {}:{}".format(self.name, self.host, self.port))
        self.start()
        super(Node, self).startService()

    def start(self):
        pass

    def stopService(self):
        self.stop()
        super(Node, self).stopService()

    def stop(self):
        pass

    def process_event(self, event, channel):
        pass

    def publish(self, event, channel='default_channel'):
        self.factory.publish(event, channel)


class MagicNode(EventFilterMixin, Node):
    def __init__(self, *args, **kwargs):
        self.default_publication_channel = kwargs.pop('default_publication_channel', 'default_channel')
        self.serials = kwargs.pop('serials', [])

        self.environment = kwargs.pop('environment', 'rpi')
        if self.environment != "rpi":
            Device.pin_factory = MockFactory()
            Device.pin_factory.pin_class = MockPWMPin

        EventFilterMixin.__init__(self)
        Node.__init__(self, *args, **kwargs)

        self._serials = {}
        for serial in self.serials:
            port = serial['port']
            baud_rate = serial.get('baud_rate')
            buffering_interval = serial['buffering_interval']
            self._serials[serial['port']] = Serial(port, baud_rate, buffering_interval)
            self._serials[serial['port']].process_event = self.process_event  # magic

    def publish(self, event, channel=...):
        event['from'] = self.name
        super().publish(event, self.default_publication_channel if channel is ... else channel)

    def send_serial(self, event, port=None):
        if port is None:
            if not self._serials:
                logger.error("No serial instance available: skipping")
                return

            serial = self._serials.values()[0]

        else:
            if port not in self._serials:
                logger.error("Port {} has no serial instance available: skipping".format(port))
                return

            serial = self._serials[port]

        serial.send_event(event)
