from twisted.internet import reactor

from justrelax.common.logging_utils import logger
from justrelax.node.service import PublishSubscribeClientService, on_event
from justrelax.node.holographic_menu.vlc_player import VLCDynamicSlidesPlayer


class HolographicMenu(PublishSubscribeClientService):
    def __init__(self, *args, **kwargs):
        super(HolographicMenu, self).__init__(*args, **kwargs)

        path = self.node_params['path']
        initial_slides = self.node_params['initial_slides']
        chapters = self.node_params['chapters']

        self.player = VLCDynamicSlidesPlayer(
            media_path=path, initial_slides=initial_slides, chapters=chapters, service=self)

        reactor.callLater(1, self.event_play)

    def notify_slide(self, slide_index):
        self.publish({"category": "play_slide", "slide": slide_index})

    def play_pause_stop(self, action, method_name, delay):
        if not isinstance(delay, (int, float)):
            raise TypeError("Delay must be int or float (received={}): skipping".format(delay))

        logger.info("{} video".format(action))

        reactor.callLater(delay, getattr(self.player, method_name))

    @on_event(filter={'category': 'play'})
    def event_play(self, delay=0):
        self.play_pause_stop("Playing", "play", delay)

    @on_event(filter={'category': 'pause'})
    def event_pause(self, delay=0):
        self.play_pause_stop("Pausing", "pause", delay)

    @on_event(filter={'category': 'stop'})
    def event_stop(self, delay=0):
        self.play_pause_stop("Stopping", "stop", delay)

    @on_event(filter={'category': 'set_slide'})
    def event_set_slide(self, slide_index: int, chapter_id: str, delay=0):
        if not isinstance(delay, (int, float)):
            raise TypeError("Delay must be int or float (received={}): skipping".format(delay))

        if slide_index >= len(self.player.slides):
            raise ValueError("Video has only {} slides ({} is out of range): skipping".format(
                len(self.player.slides), slide_index))

        if chapter_id not in self.player.chapters:
            raise ValueError("Video has no chapter id={}: skipping".format(
                chapter_id))

        logger.info("Setting chapter id={} in slide index={}".format(
            chapter_id, slide_index))

        reactor.callLater(delay, self.player.set_slide, slide_index, chapter_id)
