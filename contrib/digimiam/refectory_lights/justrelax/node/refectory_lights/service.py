from gpiozero import OutputDevice

from justrelax.common.logging_utils import logger
from justrelax.node.service import JustSockClientService, EventCategoryToMethodMixin


class RefectoryLights(EventCategoryToMethodMixin, JustSockClientService):
    def __init__(self, *args, **kwargs):
        super(RefectoryLights, self).__init__(*args, **kwargs)

        self.colors = {}
        for color, conf in self.node_params['colors'].items():
            self.colors[color] = OutputDevice(conf['pin'])
            if not conf.get('off_by_default', False):
                self.colors[color].on()

    def event_on(self, color):
        logger.info("Turning on {}".format(color))
        self.colors[color].on()

    def event_off(self, color):
        logger.info("Turning off {}".format(color))
        self.colors[color].off()
