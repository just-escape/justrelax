import os

import requests
from simpleaudio import WaveObject

from justrelax.node.service import JustSockNodeClientService
from justrelax.common.logging import logger


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

    def play(self, sound_file):
        logger.info("Playing sound")
        sound_path = os.path.join(self.media['directory'], sound_file)
        if not os.path.isfile(sound_path):
            success = self.download_sound(sound_file, sound_path)
            if not success:
                return
        wave_obj = WaveObject.from_wave_file(sound_path)
        wave_obj.play()

    def download_sound(self, sound_file, sound_path):
        url = "{}{}".format(self.media['base_url'], sound_file)
        logger.info("Downloading sound {} at {}".format(sound_file, url))
        response = requests.get(url)
        if response.status_code != 200:
            logger.error("Error downloading sound ({} - {}): skipping".format(
                response.status_code, response.text))
            return False

        with open(sound_path, 'w+') as f:
            f.write(response.text)

        return True
