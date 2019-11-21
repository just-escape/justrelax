import os
import time

import vlc
import pytweening

from twisted.internet import reactor

from justrelax.common.logging import logger
from justrelax.common.utils import download_file
from justrelax.node.service import JustSockNodeClientService


class AudioPlayer(JustSockNodeClientService):
    current_volume = 0
    target_volume = 0
    CALLBACK_FREQUENCY = 0.01

    class COMMANDS:
        COMMAND_TYPE = "type"

        PLAY = "play"
        AUDIO = "audio"

        SET_VOLUME = "set_volume"
        VOLUME = "volume"
        DURATION = "duration"
        EASE = "ease"

    def start(self):
        self.vlc_instance = vlc.Instance('--no-xlib')

        self.media_list = self.vlc_instance.media_list_new()

        self.media_list_player = self.vlc_instance.media_list_player_new()
        self.media_list_player.set_media_list(self.media_list)

        self.media_player = self.vlc_instance.media_player_new()
        self.media_list_player.set_media_player(self.media_player)

        self.media_player.audio_set_volume(self.current_volume)

    def stop(self):
        self.media_player.stop()
        self.vlc_instance.release()

    def process_message(self, message):
        logger.debug("Processing message '{}'".format(message))
        if type(message) is not dict:
            logger.error("Unknown message: skipping")
            return

        if self.COMMANDS.COMMAND_TYPE not in message:
            logger.error("Message has no command type: skipping")
            return

        if message[self.COMMANDS.COMMAND_TYPE] == self.COMMANDS.PLAY:
            if self.COMMANDS.AUDIO not in message:
                logger.error("Play command has no video: skipping")
                return

            self.play(message[self.COMMANDS.AUDIO])

        elif message[self.COMMANDS.COMMAND_TYPE] == self.COMMANDS.SET_VOLUME:
            if self.COMMANDS.VOLUME not in message:
                logger.error("Set volume command has not volume: skipping")
                return

            volume = message[self.COMMANDS.VOLUME]
            duration = message.get(self.COMMANDS.DURATION, 0)
            ease = message.get(self.COMMANDS.EASE, 'easeInOutSine')

            self.set_volume(volume, duration, ease)

        else:
            logger.debug("Unknown command type '{}': skipping".format(
                message[self.COMMANDS.COMMAND_TYPE]))

    def play(self, audio_file):
        logger.info("Playing audio")
        audio_path = os.path.join(self.media['directory'], audio_file)
        if not os.path.isfile(audio_path):
            url = "{}{}".format(self.media['base_url'], audio_file)
            success = download_file(url, audio_path)
            if not success:
                return

        self.media_list.add_media(self.vlc_instance.media_new(audio_path))
        self.media_list_player.play()

    def set_volume(self, volume, duration=0, ease='easeInOutSine'):
        if not isinstance(volume, int):
            logger.error('Volume must be an int (received={}): aborting'.format(volume))
            return

        if not isinstance(duration, int):
            logger.error('Duration must be an int (received={}): aborting'.format(duration))
            return

        volume = min(volume, 100)
        volume = max(0, volume)

        duration = max(0, duration)

        if duration == 0:
            self.current_volume += volume
            self.target_volume += volume
            self.media_player.audio_set_volume(int(self.current_volume))
        else:
            ease_mapping = {
                'easeInSine': pytweening.easeInSine,
                'easeOutSine': pytweening.easeOutSine,
                'easeInOutSine': pytweening.easeInOutSine,
                'easeInCubic': pytweening.easeInCubic,
                'easeOutCubic': pytweening.easeOutCubic,
                'easeInOutCubic': pytweening.easeInOutCubic,
                'easeInQuint': pytweening.easeInQuint,
                'easeOutQuint': pytweening.easeOutQuint,
                'easeInOutQuint': pytweening.easeInOutQuint,
                'easeInCirc': pytweening.easeInCirc,
                'easeOutCirc': pytweening.easeOutCirc,
                'easeInOutCirc': pytweening.easeInOutCirc,
                'easeInElastic': pytweening.easeInElastic,
                'easeOutElastic': pytweening.easeOutElastic,
                'easeInOutElastic': pytweening.easeInOutElastic,
                'easeInQuad': pytweening.easeInQuad,
                'easeOutQuad': pytweening.easeOutQuad,
                'easeInOutQuad': pytweening.easeInOutQuad,
                'easeInQuart': pytweening.easeInQuart,
                'easeOutQuart': pytweening.easeOutQuart,
                'easeInExpo': pytweening.easeInExpo,
                'easeOutExpo': pytweening.easeOutExpo,
                'easeInOutExpo': pytweening.easeInOutExpo,
                'easeInBack': pytweening.easeInBack,
                'easeOutBack': pytweening.easeOutBack,
                'easeInOutBack': pytweening.easeInOutBack,
                'easeInBounce': pytweening.easeInBounce,
                'easeOutBounce': pytweening.easeOutBounce,
                'easeInOutBounce': pytweening.easeInOutBounce,
                'linear': pytweening.linear,
            }
            easing_function = ease_mapping.get(ease, None)

            if easing_function is None:
                logger.error('Ease {} is not recognized: aborting'.format(ease))
                return

            self._fade_volume_to_over(volume, duration, easing_function=easing_function)

    def _fade_volume_to_over(self, volume, duration, easing_function=pytweening.easeInOutSine):
        t_start = time.time()
        current_volume_diff = 0
        target_volume_diff = volume - self.target_volume
        self.target_volume = self.current_volume + target_volume_diff

        def set_volume():
            now = time.time()
            progression = (now - t_start) * 1000 / duration

            nonlocal current_volume_diff
            if progression < 1:
                eased_progression = easing_function(progression)
                reactor.callLater(self.CALLBACK_FREQUENCY, set_volume)
            else:
                eased_progression = 1

            new_volume_diff = target_volume_diff * eased_progression - current_volume_diff
            self.current_volume += new_volume_diff
            current_volume_diff += new_volume_diff

            self.media_player.audio_set_volume(int(self.current_volume))

        reactor.callLater(self.CALLBACK_FREQUENCY, set_volume)
