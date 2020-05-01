from twisted.internet import reactor

from justrelax.common.logging_utils import logger
from justrelax.node.service import JustSockClientService, EventCategoryToMethodMixin
from justrelax.node.hologram_player.vlc_player import VLCDynamicSlidesPlayer

# TODO: only one video is handled by this node


class HologramPlayer(EventCategoryToMethodMixin, JustSockClientService):
    def __init__(self, *args, **kwargs):
        super(HologramPlayer, self).__init__(*args, **kwargs)

        self.videos = {}
        for video in self.node_params.get('videos', []):
            id_ = video['id']
            path = video['path']

            initial_slides = video['initial_slides']
            chapters = video['chapters']
            player = VLCDynamicSlidesPlayer(
                media_path=path, initial_slides=initial_slides, chapters=chapters)

            self.videos[id_] = player

    def play_pause_stop(self, action, method_name, video_id, delay):
        if not isinstance(delay, (int, float)):
            raise TypeError("Delay must be int or float (received={}): skipping".format(delay))

        logger.info("{} video id={}".format(action, video_id))

        player = self.videos.get(video_id, None)
        if player is None:
            raise ValueError("Unknown video id={}: aborting".format(video_id))

        reactor.callLater(delay, getattr(player, method_name))

    def event_play(self, video_id: str, delay=0):
        self.play_pause_stop("Playing", "play", video_id, delay)

    def event_pause(self, video_id: str, delay=0):
        self.play_pause_stop("Pausing", "pause", video_id, delay)

    def event_stop(self, video_id: str, delay=0):
        self.play_pause_stop("Stopping", "stop", video_id, delay)

    def event_set_slide(self, video_id: str, slide_index: int, chapter_id: str, delay=0):
        if not isinstance(delay, (int, float)):
            raise TypeError("Delay must be int or float (received={}): skipping".format(delay))

        player = self.videos.get(video_id, None)
        if player is None:
            raise ValueError("Unknown video id={}: aborting".format(video_id))

        if slide_index >= len(player.slides):
            raise ValueError("Video id={} has only {} slides ({} is out of range): skipping".format(
                video_id, len(player.slides), slide_index))

        if chapter_id not in player.chapters:
            raise ValueError("Video id={} has not chapter id={}: skipping".format(
                video_id, chapter_id))

        logger.info("Setting chapter id={} in slide index={} for video id={}".format(
            chapter_id, slide_index, video_id))

        reactor.callLater(delay, player.set_slide, slide_index, chapter_id)
