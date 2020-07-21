import pexpect

from twisted.internet import reactor

from justrelax.common.logging_utils import logger
from justrelax.node.service import JustSockClientService, EventCategoryToMethodMixin
from justrelax.node.media.player import MediaPlayerMixin


class Player(MediaPlayerMixin):
    def __init__(self, media_path, args=None):
        MediaPlayerMixin.__init__(self)

        self.args = args
        self.video_path = media_path
        self.omx_cmd = '/usr/bin/omxplayer -s {}'.format(media_path)
        if args:
            self.omx_cmd += ' {}'.format(args)
        self.player = None

        reactor.addSystemEventTrigger('before', 'shutdown', self.quit)

    def get_new_player(self):
        logger.debug("Loading a new player")
        return pexpect.spawn(self.omx_cmd)

    def release_player(self):
        logger.debug("Releasing player")
        self.player = None

    def _play(self):
        MediaPlayerMixin._play(self)
        self.player = self.get_new_player()

    def _resume(self):
        MediaPlayerMixin._resume(self)
        self.player.send('p')

    def _pause(self):
        MediaPlayerMixin._pause(self)
        self.player.send('p')

    def _stop(self):
        MediaPlayerMixin._stop(self)
        self.quit()

    def quit(self):
        if self.player:
            self.player.send('q')


class VideoPlayer(EventCategoryToMethodMixin, JustSockClientService):
    def __init__(self, *args, **kwargs):
        super(VideoPlayer, self).__init__(*args, **kwargs)

        self.player = None

        self.videos = {}
        for video_id, video_params in self.node_params['videos'].items():
            args = []
            if video_params.get('loop', False):
                args.append('--loop')
            if 'layer' in video_params:
                args.append('--layer {}'.format(video_params['layer']))
            if 'orientation' in video_params:
                args.append('--orientation {}'.format(video_params['orientation']))
            if 'display' in video_params:
                args.append('--display {} '.format(video_params['display']))
            if 'window' in video_params:
                args.append('--win {} '.format(','.join([x for x in video_params['window'].split()])))
            self.videos[video_id] = Player(video_params['path'], ' '.join(args))
            if video_params.get('autoplay', False):
                self.videos[video_id].play()

    def event_play(self, video_id: str, delay=0):
        if not isinstance(delay, (int, float)):
            raise ValueError("Delay must be int or float (received={}): skipping".format(delay))

        if video_id not in self.videos:
            raise ValueError("Video id={} is not configured: aborting".format(video_id))

        if delay > 0:
            logger.info("Scheduling to play video {} in {} seconds".format(video_id, delay))

        reactor.callLater(delay, self.videos[video_id].play)

    def event_pause(self, video_id: str, delay=0):
        if not isinstance(delay, (int, float)):
            raise ValueError("Delay must be int or float (received={}): skipping".format(delay))

        if video_id not in self.videos:
            raise ValueError("Video id={} is not configured: aborting".format(video_id))

        if delay > 0:
            logger.info("Scheduling to pause video {} in {} seconds".format(video_id, delay))

        reactor.callLater(delay, self.videos[video_id].pause)

    def event_stop(self, video_id: str, delay=0):
        if not isinstance(delay, (int, float)):
            raise ValueError("Delay must be int or float (received={}): skipping".format(delay))

        if video_id not in self.videos:
            raise ValueError("Video id={} is not configured: aborting".format(video_id))

        if delay > 0:
            logger.info("Scheduling to stop video {} in {} seconds".format(video_id, delay))

        reactor.callLater(delay, self.videos[video_id].stop)
