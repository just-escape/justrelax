import vlc

from twisted.internet import reactor

from justrelax.core.logging_utils import logger
from justrelax.core.media import MediaPlayerMixin
from justrelax.core.media import VolumeFaderMixin


class VLCTrackPlayer(VolumeFaderMixin, MediaPlayerMixin):
    def __init__(self, media_path, initial_volume=0, *args, **kwargs):
        VolumeFaderMixin.__init__(self, initial_volume=initial_volume)
        MediaPlayerMixin.__init__(self)

        self.player = None
        self.track = vlc.Media(media_path)
        self.track.parse()

    def new_player(self):
        logger.debug("Loading a new player")
        self.player = vlc.MediaPlayer()
        self.player.set_media(self.track)
        self.set_volume()

    def release_player(self):
        logger.debug("Releasing player")
        self.player.release()
        self.player = None

    def _play(self):
        self.new_player()
        MediaPlayerMixin._play(self)
        self.player.play()

    def _resume(self):
        MediaPlayerMixin._resume(self)
        self.player.play()

    def _pause(self):
        MediaPlayerMixin._pause(self)
        self.player.pause()

    def _stop(self):
        MediaPlayerMixin._stop(self)
        self.player.stop()
        self.release_player()

    def set_volume(self):
        if self.player:
            self.player.audio_set_volume(int(self.current_volume))


class VLCSelfReleasingTrackPlayer(VLCTrackPlayer):
    def __init__(self, *args, **kwargs):
        super(VLCSelfReleasingTrackPlayer, self).__init__(*args, **kwargs)
        self.release_task = None

    def schedule_release_task(self, time):
        logger.debug("Scheduling player release in {} seconds".format(time))
        self.release_task = reactor.callLater(time, self.stop)

    def cancel_release_task(self):
        logger.debug('Cancelling release task')
        try:
            self.release_task.cancel()
        except Exception as e:
            logger.warning("Could not cancel release task (reason={})".format(e))

    def _play(self):
        super(VLCSelfReleasingTrackPlayer, self)._play()
        # Add 0.1 seconds before release by precaution
        time_before_release = 0.1 + self.track.get_duration() / 1000
        self.schedule_release_task(time_before_release)

    def _resume(self):
        super(VLCSelfReleasingTrackPlayer, self)._resume()
        current_time = self.player.get_time()
        time_before_release = 0.1 + (self.track.get_duration() - current_time) / 1000
        self.schedule_release_task(time_before_release)

    def _pause(self):
        super(VLCSelfReleasingTrackPlayer, self)._pause()
        self.cancel_release_task()

    def _stop(self):
        super(VLCSelfReleasingTrackPlayer, self)._stop()
        self.cancel_release_task()


class VLCLoopingTrackPlayer(VLCTrackPlayer):
    def __init__(
            self, track_id, media_path, loop_a, loop_b,
            pause_callback, stop_callback, resume_callback, loop_callback,
            *args, **kwargs
    ):
        super(VLCLoopingTrackPlayer, self).__init__(
            media_path, *args, **kwargs)
        self.track_id = track_id
        self.loop_a = loop_a
        self.loop_b = loop_b
        self.looping_task = None
        self.pause_callback = pause_callback
        self.stop_callback = stop_callback
        self.resume_callback = resume_callback
        self.loop_callback = loop_callback

    def loop_track(self):
        time_before_loop = self.loop_b - self.loop_a
        self.schedule_looping_task(time_before_loop)

        logger.debug('Setting player time to {}'.format(self.loop_a))
        self.player.set_time(int(self.loop_a * 1000))
        self.loop_callback(self.track_id)

    def schedule_looping_task(self, time):
        logger.debug('Scheduling track loop in {} seconds'.format(time))
        self.looping_task = reactor.callLater(time, self.loop_track)

    def cancel_looping_task(self):
        logger.debug('Cancelling looping task')
        try:
            self.looping_task.cancel()
        except Exception as e:
            logger.warning("Could not cancel looping task (reason={})".format(e))

    def _play(self):
        super(VLCLoopingTrackPlayer, self)._play()
        self.schedule_looping_task(self.loop_b)

    def _resume(self):
        super(VLCLoopingTrackPlayer, self)._resume()
        current_time = self.player.get_time() / 1000
        time_before_loop = self.loop_b - current_time
        self.schedule_looping_task(time_before_loop)
        self.resume_callback(self.track_id)

    def _pause(self):
        super(VLCLoopingTrackPlayer, self)._pause()
        self.cancel_looping_task()
        self.pause_callback(self.track_id)

    def _stop(self):
        super(VLCLoopingTrackPlayer, self)._stop()
        self.cancel_looping_task()
        self.stop_callback(self.track_id)
