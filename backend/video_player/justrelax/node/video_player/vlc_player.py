import vlc

from twisted.internet import reactor

from justrelax.common.logging_utils import logger
from justrelax.node.common.media import MediaPlayerMixin


class VLCVideoPlayer(MediaPlayerMixin):
    def __init__(self, media_path, *args, **kwargs):
        MediaPlayerMixin.__init__(self)

        self.player = None
        self.video = vlc.Media(media_path)
        self.video.parse()

    def new_player(self):
        logger.debug("Loading a new player")
        self.player = vlc.MediaPlayer()
        self.player.set_media(self.video)

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

    def _stop(self):
        MediaPlayerMixin._stop(self)
        self.player.stop()
        self.release_player()


class VLCLoopingChapterVideoPlayer(VLCVideoPlayer):
    def __init__(self, media_path, chapters, *args, **kwargs):
        super(VLCLoopingChapterVideoPlayer, self).__init__(
            media_path, *args, **kwargs)

        self.looping_task = None

        default_chapter_id = chapters[0]['id']
        logger.debug("Default chapter is chapter id={}".format(
            default_chapter_id))

        chapter_dict = {}
        for c in chapters:
            id_ = c.pop('id')
            chapter_dict[id_] = c

        self.chapters = chapter_dict
        self.current_chapter_id = None
        self.set_chapter(default_chapter_id)

    @property
    def current_chapter(self):
        return self.chapters[self.current_chapter_id]

    def loop_track(self):
        time_before_loop = self.current_chapter['loop_b'] - self.current_chapter['loop_a']
        self.schedule_looping_task(time_before_loop)

        logger.debug('Setting player time to {}'.format(self.current_chapter['loop_a']))
        self.player.set_time(int(self.current_chapter['loop_a'] * 1000))

    def schedule_looping_task(self, time):
        logger.debug('Scheduling track loop in {} seconds'.format(time))
        self.looping_task = reactor.callLater(time, self.loop_track)

    def cancel_looping_task(self):
        if self.looping_task is not None:
            logger.debug('Cancelling looping task')
            try:
                self.looping_task.cancel()
            except Exception as e:
                logger.warning("Could not cancel looping task (reason={})".format(e))

    def new_player(self):
        super(VLCLoopingChapterVideoPlayer, self).new_player()
        logger.debug('Setting time={} because current chapter is {}'.format(
            self.current_chapter['t_start'], self.current_chapter_id))
        # callLater because VLC seems to need some delay
        reactor.callLater(
            0.01, self.player.set_time,
            int(self.current_chapter['t_start'] * 1000))

    def set_chapter(self, chapter_id):
        self.current_chapter_id = chapter_id
        self.cancel_looping_task()
        if self.player is not None:
            logger.debug('Setting time={} because current chapter is {}'.format(
                self.current_chapter['t_start'], self.current_chapter_id))
            self.player.set_time(int(self.current_chapter['t_start'] * 1000))
            if self.current_state == MediaPlayerMixin.STATE_PLAYING:
                time_before_loop = self.current_chapter['loop_b'] - self.current_chapter['t_start']
                self.schedule_looping_task(time_before_loop)

    def _play(self):
        super(VLCLoopingChapterVideoPlayer, self)._play()
        time_before_loop = self.current_chapter['loop_b'] - self.current_chapter['t_start']
        self.schedule_looping_task(time_before_loop)

    def _resume(self):
        super(VLCLoopingChapterVideoPlayer, self)._resume()
        current_time = self.player.get_time() / 1000
        time_before_loop = self.current_chapter['loop_b'] - current_time
        self.schedule_looping_task(time_before_loop)

    def _pause(self):
        super(VLCLoopingChapterVideoPlayer, self)._pause()
        self.cancel_looping_task()

    def _stop(self):
        super(VLCLoopingChapterVideoPlayer, self)._stop()
        self.cancel_looping_task()
