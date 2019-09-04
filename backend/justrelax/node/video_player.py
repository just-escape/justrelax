import os

import vlc

from justrelax.common.logging import logger
from justrelax.common.utils import download_file
from justrelax.node.service import JustSockNodeClientService


class VideoPlayer(JustSockNodeClientService):
    class COMMANDS:
        COMMAND_TYPE = "type"
        PLAY = "play"
        VIDEO = "video"

    def start(self):
        self.vlc_instance = vlc.Instance('--no-xlib')

        self.media_list = self.vlc_instance.media_list_new()

        self.media_list_player = self.vlc_instance.media_list_player_new()
        self.media_list_player.set_media_list(self.media_list)
        self.media_list_player.set_playback_mode(vlc.PlaybackMode.loop)

        self.media_player = self.vlc_instance.media_player_new()
        self.media_player.set_fullscreen(True)
        self.media_list_player.set_media_player(self.media_player)

    def stop(self):
        self.media_player.stop()
        self.vlc_instance.release()

    def process_message(self, message):
        logger.debug("Processing message '{}'".format(message))
        if type(message) is not dict:
            logger.debug("Unknown message: skipping")
            return

        if self.COMMANDS.COMMAND_TYPE not in message:
            logger.debug("Message has no command type: skipping")
            return

        if message[self.COMMANDS.COMMAND_TYPE] == self.COMMANDS.PLAY:
            if self.COMMANDS.VIDEO not in message:
                logger.debug("Play command has no video: skipping")
                return

            self.play(message[self.COMMANDS.VIDEO])
        else:
            logger.debug("Unknown command type '{}': skipping".format(
                message[self.COMMANDS.COMMAND_TYPE]))

    def play(self, video_file):
        logger.info("Playing video")
        video_path = os.path.join(self.media['directory'], video_file)
        if not os.path.isfile(video_path):
            url = "{}{}".format(self.media['base_url'], video_file)
            success = download_file(url, video_path)
            if not success:
                return

        self.media_list.add_media(self.vlc_instance.media_new(video_path))
        self.media_list_player.play()
