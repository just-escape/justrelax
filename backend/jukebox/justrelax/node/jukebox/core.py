from justrelax.common.logging_utils import logger


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
