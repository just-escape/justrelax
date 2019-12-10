import time

import pytweening
import alsaaudio

from twisted.internet import reactor

from justrelax.common.logging_utils import logger


EASE_MAPPING = {
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


class VolumeFaderMixin:
    def __init__(self, initial_volume=0, update_frequency=0.01):
        self.current_volume = initial_volume
        self.target_volume = initial_volume

        self.update_frequency = update_frequency

    def fade_volume(self, volume, duration=0, ease=pytweening.easeInOutSine):
        if duration == 0:
            self.current_volume += volume
            self.target_volume += volume
            self.set_volume()
        else:
            self._fade_volume(volume, duration, ease=ease)

    def _fade_volume(self, volume, duration, ease=pytweening.easeInOutSine):
        t_start = time.time()
        current_volume_diff = 0
        target_volume_diff = volume - self.target_volume
        self.target_volume = self.target_volume + target_volume_diff

        def update():
            now = time.time()
            progression = (now - t_start) * 1000 / duration

            nonlocal current_volume_diff
            if progression < 1:
                eased_progression = ease(progression)
                reactor.callLater(self.update_frequency, update)
            else:
                eased_progression = 1

            new_volume_diff = target_volume_diff * eased_progression - current_volume_diff
            self.current_volume += new_volume_diff
            current_volume_diff += new_volume_diff

            self.set_volume()

        reactor.callLater(self.update_frequency, update)

    def set_volume(self):
        pass


class MasterVolume(VolumeFaderMixin):
    def __init__(self, initial_volume=None):
        self.mixer = alsaaudio.Mixer()

        if initial_volume is None:
            volume = self.mixer.getvolume()
        else:
            volume = initial_volume

        super(MasterVolume, self).__init__(initial_volume=volume)
        self.set_volume()

    def set_volume(self):
        self.mixer.setvolume(int(self.current_volume))


class TrackPlayerMixin:
    STATE_NOT_STARTED = 'not_started'
    STATE_PLAYING = 'playing'
    STATE_PAUSED = 'paused'

    def __init__(self):
        self.current_state = TrackPlayerMixin.STATE_NOT_STARTED

    def play(self):
        if self.current_state == TrackPlayerMixin.STATE_NOT_STARTED:
            logger.debug('Player has not been started yet')
            self._play()
            self.current_state = TrackPlayerMixin.STATE_PLAYING
        elif self.current_state == TrackPlayerMixin.STATE_PLAYING:
            logger.debug('Player is already playing')
            logger.debug('Nothing to do')
        elif self.current_state == TrackPlayerMixin.STATE_PAUSED:
            logger.debug('Player is paused and had already been started')
            self._resume()
            self.current_state = TrackPlayerMixin.STATE_PLAYING
        else:
            pass

    def pause(self):
        if self.current_state == TrackPlayerMixin.STATE_NOT_STARTED:
            logger.debug('Player has not been started yet')
            logger.debug('Nothing to do')
        elif self.current_state == TrackPlayerMixin.STATE_PLAYING:
            logger.debug('Player is already playing')
            self._pause()
            self.current_state = TrackPlayerMixin.STATE_PAUSED
        elif self.current_state == TrackPlayerMixin.STATE_PAUSED:
            logger.debug('Player is paused and had already been started')
            logger.debug('Nothing to do')
        else:
            pass

    def stop(self):
        if self.current_state == TrackPlayerMixin.STATE_NOT_STARTED:
            logger.debug('Player has not been started yet')
            logger.debug('Nothing to do')
        elif self.current_state == TrackPlayerMixin.STATE_PLAYING:
            logger.debug('Player is already playing')
            self._stop()
            self.current_state = TrackPlayerMixin.STATE_NOT_STARTED
        elif self.current_state == TrackPlayerMixin.STATE_PAUSED:
            logger.debug('Player is paused and had already been started')
            self._stop()
            self.current_state = TrackPlayerMixin.STATE_NOT_STARTED
        else:
            pass

    def _play(self):
        logger.debug("Playing track")

    def _resume(self):
        logger.debug("Resuming track")

    def _pause(self):
        logger.debug("Pausing track")

    def _stop(self):
        logger.debug("Stopping track")
