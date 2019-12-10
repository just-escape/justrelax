import vlc

from twisted.internet import reactor

from justrelax.common.logging_utils import logger
from justrelax.node.jukebox.core import VolumeFaderMixin, TrackPlayerMixin


class VLCTrackHandler(VolumeFaderMixin, TrackPlayerMixin):
    def __init__(self, track_path, initial_volume=0, *args, **kwargs):
        VolumeFaderMixin.__init__(self, initial_volume=initial_volume)
        TrackPlayerMixin.__init__(self)

        self.track = vlc.Media(track_path)
        self.track.parse()

    def new_player(self):
        logger.debug("Loading a new player")
        self.player = vlc.MediaPlayer()
        self.player.set_media(self.track)
        self.set_volume()

    def release_player(self):
        logger.debug("Releasing player")
        self.player.release()

    def _play(self):
        self.new_player()
        TrackPlayerMixin._play(self)
        self.player.play()

    def _resume(self):
        TrackPlayerMixin._resume(self)
        self.player.play()

    def _pause(self):
        TrackPlayerMixin._pause(self)
        self.player.pause()

    def _stop(self):
        TrackPlayerMixin._stop(self)
        self.player.stop()
        self.release_player()

    def set_volume(self):
        self.player.audio_set_volume(int(self.current_volume))


class VLCSelfReleasingTrackHandler(VLCTrackHandler):
    def __init__(self, *args, **kwargs):
        super(VLCSelfReleasingTrackHandler, self).__init__(*args, **kwargs)
        self.release_task = None

    def schedule_release_task(self, time):
        logger.debug("Scheduling player release in {} seconds".format(time))
        self.release_task = reactor.callLater(time, self.release_player)

    def cancel_release_task(self):
        logger.debug('Cancelling release task')
        try:
            self.release_task.cancel()
        except Exception as e:
            logger.warning("Could not cancel release task (reason={})".format(e))

    def _play(self):
        super(VLCSelfReleasingTrackHandler, self)._play()
        # Add 0.1 seconds before release by precaution
        time_before_release = 0.1 + self.track.get_duration() / 1000
        self.schedule_release_task(time_before_release)

    def _resume(self):
        super(VLCSelfReleasingTrackHandler, self)._resume()
        current_time = self.player.get_time()
        time_before_release = 0.1 + (self.track.get_duration() - current_time) / 1000
        self.schedule_release_task(time_before_release)

    def _pause(self):
        super(VLCSelfReleasingTrackHandler, self)._pause()
        self.cancel_release_task()

    def _stop(self):
        super(VLCSelfReleasingTrackHandler, self)._stop()
        self.cancel_release_task()


class VLCLoopingTrackHandler(VLCTrackHandler):
    def __init__(self, track_path, loop_a, loop_b, *args, **kwargs):
        super(VLCLoopingTrackHandler, self).__init__(
            track_path, *args, **kwargs)
        self.loop_a = loop_a
        self.loop_b = loop_b
        self.looping_task = None

    def loop_track(self):
        time_before_loop = self.loop_b - self.loop_a
        self.schedule_looping_task(time_before_loop)

        logger.debug('Setting player time to {}'.format(self.loop_a))
        self.player.set_time(int(self.loop_a * 1000))

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
        super(VLCLoopingTrackHandler, self)._play()
        self.schedule_looping_task(self.loop_b)

    def _resume(self):
        super(VLCLoopingTrackHandler, self)._resume()
        current_time = self.player.get_time() / 1000
        time_before_loop = self.loop_b - current_time
        self.schedule_looping_task(time_before_loop)

    def _pause(self):
        super(VLCLoopingTrackHandler, self)._pause()
        self.cancel_looping_task()

    def _stop(self):
        super(VLCLoopingTrackHandler, self)._stop()
        self.cancel_looping_task()
