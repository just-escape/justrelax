import inspect
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

    def send_event(self, event):
        self.factory.send_event(event)


class EventCategoryToMethodMixin:
    CATEGORY_FIELD = "category"
    METHOD_PREFIX = "process"
    METHOD_SEPARATOR = "_"

    @staticmethod
    def get_category(event):
        if EventCategoryToMethodMixin.CATEGORY_FIELD not in event:
            raise TypeError("Event has no category: ignoring")

        category = event[EventCategoryToMethodMixin.CATEGORY_FIELD]
        return category

    def get_method_from_category(self, category):
        method_name = "{}{}{}".format(
            EventCategoryToMethodMixin.METHOD_PREFIX,
            EventCategoryToMethodMixin.METHOD_SEPARATOR,
            category)
        method = getattr(self, method_name, None)
        if not callable(method):
            raise NotImplementedError("Method {} not found".format(method_name))
        return method

    @staticmethod
    def check_arguments(event, method):
        method_arguments = inspect.signature(method).parameters
        for arg in method_arguments.values():
            if arg.default is arg.empty:
                # No default value: a value must be defined in the event
                if arg.name not in event:
                    raise TypeError("Event has no {} field: ignoring".format(arg.name))

                if arg.annotation is not arg.empty:
                    if type(event[arg.name]) is not arg.annotation:
                        raise TypeError("Event field {} type is not {} (received {}): ignoring".format(
                            arg.name, arg.annotation, type(event[arg.name])))

    @staticmethod
    def pop_superfluous_fields(event, method):
        # This inspection is not 100% proof. Positional only arguments or *args / **kwargs can mess
        # with this logic, but at least it covers a lot of cases.
        method_arguments = inspect.signature(method).parameters
        event.pop(EventCategoryToMethodMixin.CATEGORY_FIELD)
        for field in event:
            if field not in method_arguments:
                event.pop(field)

    def process_event(self, event):
        logger.debug("Processing event '{}'".format(event))
        if type(event) is not dict:
            logger.error("Unknown event: skipping")
            return

        category = self.get_category(event)
        method = self.get_method_from_category(category)

        self.check_arguments(event, method)
        self.pop_superfluous_fields(event, method)

        method(**event)
