from twisted.internet import reactor

from justrelax.common.logging_utils import logger
from justrelax.node.service import JustSockNodeClientService
from justrelax.node.video_player.vlc_player import VLCVideoPlayer
from justrelax.node.video_player.vlc_player import VLCLoopingChapterVideoPlayer


class VideoPlayer(JustSockNodeClientService):
    class COMMANDS:
        ACTION = "action"

        VIDEO_ID = "video_id"
        DELAY = "delay"

        ACTION_PLAY = "play"
        ACTION_PAUSE = "pause"
        ACTION_STOP = "stop"

        ACTION_SET_CHAPTER = "set_chapter"
        CHAPTER_ID = "chapter_id"

    def start(self):
        self.videos = {}
        for video in self.node_params.get('videos', []):
            id_ = video['id']
            path = video['path']
            mode = video.get('mode', 'one_shot')

            if mode == 'chapter_loop':
                chapters = video['chapters']
                player = VLCLoopingChapterVideoPlayer(
                    media_path=path, chapters=chapters)
            else:
                player = VLCVideoPlayer(media_path=path)

            self.videos[id_] = player

        # Factorisation
        self.play_pause_stop = {
            self.COMMANDS.ACTION_PLAY: {
                'verb': 'Play',
                'ing': 'Playing',
                'method': 'play',
            },
            self.COMMANDS.ACTION_PAUSE: {
                'verb': 'Pause',
                'ing': 'Pausing',
                'method': 'pause',
            },
            self.COMMANDS.ACTION_STOP: {
                'verb': 'Stop',
                'ing': 'Stopping',
                'method': 'stop',
            },
        }

    def process_message(self, message):
        logger.debug("Processing message '{}'".format(message))
        if type(message) is not dict:
            logger.debug("Unknown message: skipping")
            return

        if self.COMMANDS.ACTION not in message:
            logger.debug("Message has no action: skipping")
            return

        delay = message.get(self.COMMANDS.DELAY, 0)
        if not isinstance(delay, (int, float)):
            logger.error("Delay must be int or float (received={}): skipping".format(delay))
            return

        if message[self.COMMANDS.ACTION] in self.play_pause_stop:
            action = self.play_pause_stop[message[self.COMMANDS.ACTION]]

            if self.COMMANDS.VIDEO_ID not in message:
                logger.error("{} action has no video_id: skipping".format(action['verb']))
                return

            video_id = message[self.COMMANDS.VIDEO_ID]
            logger.info("{} video id={}".format(action['ing'], video_id))

            player = self.videos.get(video_id, None)
            if player is None:
                logger.error("Unknown video id={}: aborting".format(video_id))
                return

            reactor.callLater(delay, getattr(player, action['method']))

        elif message[self.COMMANDS.ACTION] == self.COMMANDS.ACTION_SET_CHAPTER:
            if self.COMMANDS.VIDEO_ID not in message:
                logger.error("Set chapter action has no video_id: skipping")
                return

            video_id = message[self.COMMANDS.VIDEO_ID]
            player = self.videos.get(video_id, None)
            if player is None:
                logger.error("Unknown video id={}: aborting".format(video_id))
                return

            if self.COMMANDS.CHAPTER_ID not in message:
                logger.error("Set chapter action has no chapter id: skipping")
                return

            chapter_id = message[self.COMMANDS.CHAPTER_ID]
            if chapter_id not in player.chapters:
                logger.error("Video id={} has not chapter id={}: skipping".format(
                    video_id, chapter_id))
                return

            logger.info("Setting chapter id={} for video id={}".format(
                chapter_id, video_id))

            reactor.callLater(delay, player.set_chapter, chapter_id)

        else:
            logger.debug("Unknown command type '{}': skipping".format(
                message[self.COMMANDS.ACTION]))
