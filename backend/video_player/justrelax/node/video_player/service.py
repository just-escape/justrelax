from omxplayer.player import OMXPlayer

from twisted.internet import reactor

from justrelax.common.logging_utils import logger
from justrelax.node.service import JustSockClientService
from justrelax.node.common.media import MediaPlayerMixin


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
    class PROTOCOL:
        ACTION = "action"

        DELAY = "delay"

        ACTION_PLAY = "play"
        ACTION_PAUSE = "pause"
        ACTION_STOP = "stop"

    def __init__(self, *args, **kwargs):
        super(VideoPlayer, self).__init__(*args, **kwargs)

        path = self.node_params['path']
        loop = self.node_params['loop']
        player = Player(media_path=path, loop=loop)

        self.player = player

        # Factorisation
        self.play_pause_stop = {
            self.PROTOCOL.ACTION_PLAY: {
                'verb': 'Play',
                'ing': 'Playing',
                'method': 'play',
            },
            self.PROTOCOL.ACTION_PAUSE: {
                'verb': 'Pause',
                'ing': 'Pausing',
                'method': 'pause',
            },
            self.PROTOCOL.ACTION_STOP: {
                'verb': 'Stop',
                'ing': 'Stopping',
                'method': 'stop',
            },
        }

        autoplay = self.node_params.get('autoplay', False)
        if autoplay:
            self.process_event(
                {
                    self.PROTOCOL.ACTION: self.PROTOCOL.ACTION_PLAY,
                }
            )

    def process_event(self, event):
        logger.debug("Processing event '{}'".format(event))

        if type(event) is not dict:
            logger.debug("Unknown event: skipping")
            return

        delay = event.get(self.PROTOCOL.DELAY, 0)
        if not isinstance(delay, (int, float)):
            logger.error("Delay must be int or float (received={}): skipping".format(delay))
            return

        if event[self.PROTOCOL.ACTION] in self.play_pause_stop:
            action = self.play_pause_stop[event[self.PROTOCOL.ACTION]]

            logger.info("{} video".format(action['ing']))
            reactor.callLater(delay, getattr(self.player, action['method']))

        else:
            logger.debug("Unknown command type '{}': skipping".format(
                event[self.PROTOCOL.ACTION]))
