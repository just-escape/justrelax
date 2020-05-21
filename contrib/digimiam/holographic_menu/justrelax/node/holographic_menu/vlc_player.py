import vlc

from twisted.internet import reactor

from justrelax.common.logging_utils import logger
from justrelax.node.media.player import MediaPlayerMixin


class VLCVideoPlayer(MediaPlayerMixin):
    def __init__(self, media_path, *args, **kwargs):
        MediaPlayerMixin.__init__(self)

        self.player = None
        self.video = vlc.Media(media_path)
        self.video.parse()

    def new_player(self):
        logger.debug("Loading a new player")
        self.player = vlc.MediaPlayer()
        self.player.set_fullscreen(True)
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


class VLCDynamicSlidesPlayer(VLCVideoPlayer):
    def __init__(self, media_path, initial_slides, chapters, service, *args, **kwargs):
        super(VLCDynamicSlidesPlayer, self).__init__(
            media_path, *args, **kwargs)

        self.slide_task = None

        self.chapters = {}
        self.load_chapters(chapters)
        self.current_slide_index = 0
        self.slides = initial_slides

        self.service = service

    @property
    def current_chapter(self):
        return self.chapters[self.slides[self.current_slide_index]]

    def load_chapters(self, chapters):
        for chapter in chapters:
            self.chapters[chapter['id']] = {
                'start': chapter['start'],
                'end': chapter['end'],
            }

    def next_slide(self):
        self.current_slide_index = (self.current_slide_index + 1) % len(self.slides)

        time_before_slide = self.current_chapter['end'] - self.current_chapter['start']
        self.schedule_slide_task(time_before_slide)

        logger.debug('Setting player time to {} because current slide is chapter id={}'.format(
            self.current_chapter['start'], self.slides[self.current_slide_index]))
        self.player.set_time(int(self.current_chapter['start']) * 1000)
        self.service.notify_slide(self.current_slide_index)

    def schedule_slide_task(self, time):
        logger.debug('Scheduling next slide in {} seconds'.format(time))
        self.slide_task = reactor.callLater(time, self.next_slide)

    def cancel_slide_task(self):
        if self.slide_task and self.slide_task.active():
            logger.debug('Cancelling slide task')
            self.slide_task.cancel()

    def new_player(self):
        super(VLCDynamicSlidesPlayer, self).new_player()
        logger.debug('Setting time={} because current slide is chapter id={}'.format(
            self.current_chapter['start'], self.slides[self.current_slide_index]))
        # callLater because VLC seems to need some delay
        reactor.callLater(
            0.01, self.player.set_time,
            int(self.current_chapter['start'] * 1000))

    def set_slide(self, slide_index, chapter_id):
        self.current_slide_index = slide_index
        self.slides[self.current_slide_index] = chapter_id
        self.cancel_slide_task()
        if self.player is not None:
            logger.debug('Setting time={} because current slide is {}'.format(
                self.current_chapter['start'], self.slides[self.current_slide_index]))
            self.player.set_time(int(self.current_chapter['start'] * 1000))
            self.service.notify_slide(slide_index)
            if self.current_state == MediaPlayerMixin.STATE_PLAYING:
                time_before_slide = self.current_chapter['end'] - self.current_chapter['start']
                self.schedule_slide_task(time_before_slide)

    def _play(self):
        super(VLCDynamicSlidesPlayer, self)._play()
        time_before_slide = self.current_chapter['end'] - self.current_chapter['start']
        self.schedule_slide_task(time_before_slide)

    def _resume(self):
        super(VLCDynamicSlidesPlayer, self)._resume()
        current_time = self.player.get_time() / 1000
        time_before_slide = self.current_chapter['end'] - current_time
        self.schedule_slide_task(time_before_slide)

    def _pause(self):
        super(VLCDynamicSlidesPlayer, self)._pause()
        self.cancel_slide_task()

    def _stop(self):
        super(VLCDynamicSlidesPlayer, self)._stop()
        self.cancel_slide_task()


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
