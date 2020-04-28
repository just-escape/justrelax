from omxplayer.player import OMXPlayer

from twisted.internet import reactor

from justrelax.common.logging_utils import logger
from justrelax.node.service import JustSockClientService
from justrelax.node.media.player import MediaPlayerMixin


class Player(MediaPlayerMixin):
    def __init__(self, media_path, loop=True):
        MediaPlayerMixin.__init__(self)

        self.player = None
        self.loop = loop
        self.video_path = media_path
        self.new_player()

        reactor.addSystemEventTrigger('before', 'shutdown', self.quit)

    def new_player(self):
        logger.debug("Loading a new player")
        args = ['--loop'] if self.loop else None
        self.player = OMXPlayer(self.video_path, args=args, pause=True)

    def release_player(self):
        logger.debug("Releasing player")
        self.player = None

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
        self.player.stop()
        self.release_player()
        self.new_player()

    def quit(self):
        if self.player:
            self.player.quit()


class VideoPlayer(JustSockClientService):
    def __init__(self, *args, **kwargs):
        super(VideoPlayer, self).__init__(*args, **kwargs)

        path = self.node_params['path']
        loop = self.node_params['loop']
        player = Player(media_path=path, loop=loop)

        self.player = player

        autoplay = self.node_params.get('autoplay', False)
        if autoplay:
            self.process_event(
                {
                    self.PROTOCOL.ACTION: self.PROTOCOL.ACTION_PLAY,
                }
            )

    def process_play(self, delay=0):
        if not isinstance(delay, (int, float)):
            raise ValueError("Delay must be int or float (received={}): skipping".format(delay))

        logger.info("Playing video")

        reactor.callLater(delay, self.player.play)

    def process_pause(self, delay=0):
        if not isinstance(delay, (int, float)):
            raise ValueError("Delay must be int or float (received={}): skipping".format(delay))

        logger.info("Pausing video")

        reactor.callLater(delay, self.player.pause)

    def process_stop(self, delay=0):
        if not isinstance(delay, (int, float)):
            raise ValueError("Delay must be int or float (received={}): skipping".format(delay))

        logger.info("Stopping video")

        reactor.callLater(delay, self.player.stop)
