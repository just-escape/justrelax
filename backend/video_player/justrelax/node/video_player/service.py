from twisted.internet import reactor

from justrelax.common.logging_utils import logger
from justrelax.node.service import JustSockClientService
from justrelax.node.video_player.vlc_player import VLCVideoPlayer
from justrelax.node.video_player.vlc_player import VLCDynamicSlidesPlayer


class VideoPlayer(JustSockClientService):
    class PROTOCOL:
        ACTION = "action"

        VIDEO_ID = "video_id"
        DELAY = "delay"

        ACTION_PLAY = "play"
        ACTION_PAUSE = "pause"
        ACTION_STOP = "stop"

        ACTION_SET_SLIDE = "set_slide"
        SLIDE_INDEX = "slide_index"
        CHAPTER_ID = "chapter_id"

    def __init__(self, *args, **kwargs):
        super(VideoPlayer, self).__init__(*args, **kwargs)

        self.videos = {}
        for video in self.node_params.get('videos', []):
            id_ = video['id']
            path = video['path']
            mode = video.get('mode', 'one_shot')

            if mode == 'dynamic_slides':
                initial_slides = video['initial_slides']
                chapters = video['chapters']
                player = VLCDynamicSlidesPlayer(
                    media_path=path, initial_slides=initial_slides, chapters=chapters)
            else:
                player = VLCVideoPlayer(media_path=path)

            self.videos[id_] = player

        # Factorisation
        self.play_pause_stop = {
            self.PROTOCOL.ACTION_PLAY: {
                'verb': 'Play',
                'ing': 'Playing',
                'method': 'play',
            },
            self.PROTOCOL.ACTION_PAUSE: {
                'verb': 'Pause',
                'ing': 'Pausing',
                'method': 'pause',
            },
            self.PROTOCOL.ACTION_STOP: {
                'verb': 'Stop',
                'ing': 'Stopping',
                'method': 'stop',
            },
        }

    def process_event(self, event):
        logger.debug("Processing event '{}'".format(event))
        if type(event) is not dict:
            logger.debug("Unknown event: skipping")
            return

        if self.PROTOCOL.ACTION not in event:
            logger.debug("Event has no action: skipping")
            return

        delay = event.get(self.PROTOCOL.DELAY, 0)
        if not isinstance(delay, (int, float)):
            logger.error("Delay must be int or float (received={}): skipping".format(delay))
            return

        if event[self.PROTOCOL.ACTION] in self.play_pause_stop:
            action = self.play_pause_stop[event[self.PROTOCOL.ACTION]]

            if self.PROTOCOL.VIDEO_ID not in event:
                logger.error("{} action has no video_id: skipping".format(action['verb']))
                return

            video_id = event[self.PROTOCOL.VIDEO_ID]
            logger.info("{} video id={}".format(action['ing'], video_id))

            player = self.videos.get(video_id, None)
            if player is None:
                logger.error("Unknown video id={}: aborting".format(video_id))
                return

            reactor.callLater(delay, getattr(player, action['method']))

        elif event[self.PROTOCOL.ACTION] == self.PROTOCOL.ACTION_SET_SLIDE:
            if self.PROTOCOL.VIDEO_ID not in event:
                logger.error("Set slide action has no video_id: skipping")
                return

            video_id = event[self.PROTOCOL.VIDEO_ID]
            player = self.videos.get(video_id, None)
            if player is None:
                logger.error("Unknown video id={}: aborting".format(video_id))
                return

            if self.PROTOCOL.SLIDE_INDEX not in event:
                logger.error("Set slide action has no chapter id: skipping")
                return

            slide_index = event[self.PROTOCOL.SLIDE_INDEX]
            if slide_index >= len(player.slides):
                logger.error("Video id={} has only {} slides ({} is out of range): skipping".format(
                    video_id, len(player.slides), slide_index))
                return

            if self.PROTOCOL.CHAPTER_ID not in event:
                logger.error("Set slide action has no chapter id: skipping")
                return

            chapter_id = event[self.PROTOCOL.CHAPTER_ID]
            if chapter_id not in player.chapters:
                logger.error("Video id={} has not chapter id={}: skipping".format(
                    video_id, chapter_id))
                return

            logger.info("Setting chapter id={} in slide index={} for video id={}".format(
                chapter_id, slide_index, video_id))

            reactor.callLater(delay, player.set_slide, slide_index, chapter_id)

        else:
            logger.debug("Unknown command type '{}': skipping".format(
                event[self.PROTOCOL.ACTION]))
