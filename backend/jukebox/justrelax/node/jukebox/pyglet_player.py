import pyglet

from twisted.internet import reactor

from justrelax.common.logging_utils import logger
from justrelax.node.common.media import MediaPlayerMixin
from justrelax.node.common.volume import VolumeFaderMixin


class PygletTrackHandler(VolumeFaderMixin, MediaPlayerMixin):
    def __init__(self, media_path, initial_volume=100, *args, **kwargs):
        VolumeFaderMixin.__init__(self, initial_volume=initial_volume)
        MediaPlayerMixin.__init__(self)

        self.track = pyglet.media.load(media_path, streaming=False)
        self.new_player()

    def new_player(self):
        logger.debug("Loading a new player")
        self.player = pyglet.media.Player()
        self.player.queue(self.track)
        self.player.on_player_eos = self.on_player_eos
        self.set_volume()

    def on_player_eos(self):
        self.stop()

    def _play(self):
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
        self.new_player()

    def set_volume(self):
        self.player.volume = self.current_volume / 100


class PygletLoopingTrackHandler(PygletTrackHandler):
    def __init__(self, media_path, loop_a, loop_b,  *args, **kwargs):
        super(PygletLoopingTrackHandler, self).__init__(
            media_path, *args, **kwargs)
        self.loop_a = loop_a
        self.loop_b = loop_b
        self.looping_task = None

    def loop_track(self):
        time_before_loop = self.loop_b - self.loop_a
        self.schedule_looping_task(time_before_loop)

        logger.debug('Setting player time to {}'.format(self.loop_a))
        self.player.seek(self.loop_a)

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
        super(PygletLoopingTrackHandler, self)._play()
        self.schedule_looping_task(self.loop_b)

    def _resume(self):
        super(PygletLoopingTrackHandler, self)._resume()
        current_time = self.player.time
        time_before_loop = self.loop_b - current_time
        self.schedule_looping_task(time_before_loop)

    def _pause(self):
        super(PygletLoopingTrackHandler, self)._pause()
        self.cancel_looping_task()

    def _stop(self):
        super(PygletLoopingTrackHandler, self)._stop()
        self.cancel_looping_task()
