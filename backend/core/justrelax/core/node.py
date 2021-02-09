import json
import inspect
import socket
import argparse
from copy import deepcopy

import yaml
from gpiozero import Device
from gpiozero.pins.mock import MockFactory, MockPWMPin

from twisted.internet import reactor
from twisted.internet.protocol import ReconnectingClientFactory
from autobahn.twisted.websocket import WebSocketClientProtocol, WebSocketClientFactory

from justrelax.core.logging_utils import init_logging, logger


class NodeProtocol(WebSocketClientProtocol):
    def onConnect(self, response):
        logger.debug("Connected to broker at {}".format(response.peer))

    def onConnecting(self, transport_details):
        logger.debug("Connecting. Transport details: {}".format(transport_details))

    def onOpen(self):
        logger.debug("WebSocket connection opened")
        self.factory.connection_opened()

    def onMessage(self, payload, isBinary):
        if isBinary:
            logger.warning("Binary message received ({} bytes): ignoring".format(len(payload)))
            return

        unicode_message = payload.decode('utf8', 'replace')

        try:
            message = json.loads(unicode_message)
        except json.JSONDecodeError:
            logger.warning("Cannot load {}: ignoring".format(unicode_message))
            return

        # message could be validated here with something like pydantic

        logger.info("{} >>> {}".format(channel, event))

        try:
            self.factory.process_event(message['event'], message['channel'])
        except Exception as e:
            formatted_exception = "{}: {}".format(type(e).__name__, e)
            logger.error("Error while trying to process message={} ({})".format(message, formatted_exception))

    def onClose(self, wasClean, code, reason):
        logger.info("WebSocket connection closed (reason={})".format(reason))

    def send_message(self, event):
        unicode_json = json.dumps(event, ensure_ascii=False)
        bytes_ = unicode_json.encode("utf8", "replace")
        self.sendMessage(bytes_)


class Node(WebSocketClientFactory, ReconnectingClientFactory):
    maxDelay = 30

    def __init__(self, *args, **kwargs):
        super(Node, self).__init__(*args, **kwargs)
        self.protocol = None

    def connection_opened(self):
        pass

    def startedConnecting(self, connector):
        logger.debug('Started to connect')

    def buildProtocol(self, addr):
        self.resetDelay()
        self.protocol = NodeProtocol()
        self.protocol.factory = self
        return self.protocol

    def clientConnectionLost(self, connector, reason):
        logger.error('Connection lost (reason={})'.format(reason))
        ReconnectingClientFactory.clientConnectionLost(self, connector, reason)

    def clientConnectionFailed(self, connector, reason):
        logger.error('Connection failed. Reason: {}'.format(reason))
        ReconnectingClientFactory.clientConnectionFailed(self, connector, reason)

    def publish(self, event, channel):
        logger.info("{} <<< {}".format(channel, event))
        self.protocol.send_message({'action': 'publish', 'channel': channel, 'event': event})

    def process_event(self, event, channel):
        pass


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


class MagicNode(EventFilterMixin, Node):
    def __init__(self, config=..., *args, **kwargs):
        self.config = config if config is not ... else {}

        self._name = self.config.get('name', 'default_name')
        self._default_publication_channel = self.config.get('default_publication_channel', 'default_channel')
        self._subscriptions = self.config.get('subscriptions', [])

        rpi_detected = False
        try:
            with open('/proc/cpuinfo', 'r') as f:
                rpi_detected = any(['Raspberry Pi' in line for line in f.readlines()])
        except Exception:
            pass

        if not rpi_detected:
            logger.warning("The detected platform is not a raspberry pi: mocking gpiozero library pin interfaces")
            Device.pin_factory = MockFactory()
            Device.pin_factory.pin_class = MockPWMPin

        serials = self.config.get('serials', [])
        self._serials = {}
        for serial in serials:
            port = serial['port']
            baud_rate = serial.get('baud_rate', 9600)
            buffering_interval = serial.get('buffering_interval', 0.1)
            self._serials[serial['port']] = Serial(port, baud_rate, buffering_interval)
            self._serials[serial['port']].process_event = self.process_event  # magic

        self._first_connection = False

        EventFilterMixin.__init__(self)
        Node.__init__(self, *args, **kwargs)

    def connection_opened(self):
        if not self._first_connection:
            self._first_connection = True
            self.on_first_connection()

        for channel in self._subscriptions:
            logger.info("Subscribing to {}".format(channel))
            self.subscribe(channel)

    def on_first_connection(self):
        pass

    def subscribe(self, channel):
        self.protocol.send_message(
            {
                "action": "subscribe",
                "channel": channel,
            }
        )

    def publish(self, event, channel=...):
        if isinstance(event, dict):
            event['from'] = self._name
        super().publish(event, channel if channel is not ... else self._default_publication_channel)

    def log_published_error(self, message):
        logger.error(message)
        self.publish({'hostname': socket.gethostname(), 'log': message}, 'error')

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


def run_node(klass):
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='localhost', help='localhost by default')
    parser.add_argument('-p', '--port', type=int, default=3031, help='3031 by default')
    parser.add_argument('-c', '--config', type=str, help='Path to a config file')
    parser.add_argument('-l', '--log-level', type=str, default='INFO', help='INFO by default')
    parser.add_argument('-f', '--log-file', type=str, default='/dev/null', help='/dev/null by default (no file)')
    parser.add_argument('-t', '--twisted-logs', action='store_true', help='Include twisted logs (no by default)')
    args = parser.parse_args()

    init_logging(level=args.log_level, file=args.log_file, twisted_logs=args.twisted_logs)

    if args.config:
        with open(args.config, "rt") as f:
            config = yaml.safe_load(f.read())

    kwargs = {'config': config} if args.config else {}

    logger.info("Initializing node")
    node = klass(**kwargs)

    logger.info("Connecting to broker at {}:{}".format(args.host, args.port))

    reactor.connectTCP(args.host, args.port, node)
    reactor.run()
