import os

from justrelax.common.logging_utils import logger
from justrelax.common.utils import download_file
from justrelax.node.service import JustSockNodeClientService


class SoundPlayer(JustSockNodeClientService):
    class COMMANDS:
        COMMAND_TYPE = "type"
        PLAY = "play"
        SOUND = "sound"

    def process_message(self, message):
        logger.debug("Processing message '{}'".format(message))
        if type(message) is not dict:
            logger.debug("Unknown message: skipping")
            return

        if self.COMMANDS.COMMAND_TYPE not in message:
            logger.debug("Message has no command type: skipping")
            return

        if message[self.COMMANDS.COMMAND_TYPE] == self.COMMANDS.PLAY:
            if self.COMMANDS.SOUND not in message:
                logger.debug("Play command has no sound: skipping")
                return

            self.play(message[self.COMMANDS.SOUND])
        else:
            logger.debug("Unknown command type '{}': skipping".format(
                message[self.COMMANDS.COMMAND_TYPE]))

    def play(self, video_file):
        logger.info("Playing sound")
        sound_path = os.path.join(self.media['directory'], video_file)
        if not os.path.isfile(sound_path):
            url = "{}{}".format(self.media['base_url'], video_file)
            success = download_file(url, sound_path)
            if not success:
                return
        wave_obj = WaveObject.from_wave_file(sound_path)
        wave_obj.play()
