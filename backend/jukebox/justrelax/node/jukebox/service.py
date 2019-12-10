import pyglet

from twisted.internet import reactor
from twisted.internet.task import LoopingCall

from justrelax.common.logging_utils import logger
from justrelax.node.service import JustSockNodeClientService
from justrelax.node.jukebox.core import EASE_MAPPING, MasterVolume
from justrelax.node.jukebox.vlc_player import VLCSelfReleasingTrackHandler
from justrelax.node.jukebox.vlc_player import VLCLoopingTrackHandler
from justrelax.node.jukebox.pyglet_player import PygletTrackHandler
from justrelax.node.jukebox.pyglet_player import PygletLoopingTrackHandler


class Jukebox(JustSockNodeClientService):
    class COMMANDS:
        ACTION = "action"

        TRACK_ID = "track_id"
        DELAY = "delay"

        ACTION_PLAY = "play"
        ACTION_PAUSE = "pause"
        ACTION_STOP = "stop"

        ACTION_SET_VOLUME = "set_volume"
        VOLUME = "volume"
        DURATION = "duration"
        EASE = "ease"

    def start(self):
        initial_master_volume = self.node_params.get('master_volume', None)
        default_initial_volume = self.node_params.get('default_volume', 100)

        player = self.node_params.get('player', 'vlc')
        if player == 'vlc':
            track_handler = VLCSelfReleasingTrackHandler
            looping_track_handler = VLCLoopingTrackHandler
        elif player == 'pyglet':
            track_handler = PygletTrackHandler
            looping_track_handler = PygletLoopingTrackHandler
            loop = LoopingCall(self.pyglet_loop)
            loop.start(1 / 30)
        else:
            raise ValueError(
                "Bad player value ({}). Possible values are vlc or "
                "pyglet.".format(player))

        try:
            self.master_volume = MasterVolume(initial_volume=initial_master_volume)
        except Exception:
            logger.exception()
            logger.warning(
                "Unable to initialize the master volume controller. Further "
                "actions on the master volume will be ignored.")
            self.master_volume = None

        self.tracks = {}
        for track in self.node_params.get('tracks', []):
            id_ = track['id']
            path = track['path']
            volume = track.get('volume', default_initial_volume)
            mode = track.get('mode', 'one_shot')
            if mode == 'loop':
                loop_a = track['loop_a']
                loop_b = track['loop_b']
                handler = looping_track_handler(
                    track_path=path,
                    loop_a=loop_a,
                    loop_b=loop_b,
                    initial_volume=volume,
                )
            else:
                handler = track_handler(
                    track_path=path,
                    initial_volume=volume,
                )
            self.tracks[id_] = handler

        # Factorisation
        self.play_pause_stop = {
            self.COMMANDS.ACTION_PLAY: {
                'verb': 'Play',
                'ing': 'Playing',
                'method': 'play',
            },
            self.COMMANDS.ACTION_PAUSE: {
                'verb': 'Pause',
                'ing': 'Pausing',
                'method': 'pause',
            },
            self.COMMANDS.ACTION_STOP: {
                'verb': 'Stop',
                'ing': 'Stopping',
                'method': 'stop',
            },
        }

    def pyglet_loop(self):
        pyglet.clock.tick()
        pyglet.app.platform_event_loop.dispatch_posted_events()

    def process_message(self, message):
        logger.debug("Processing message '{}'".format(message))
        if type(message) is not dict:
            logger.error("Unknown message: skipping")
            return

        if self.COMMANDS.ACTION not in message:
            logger.error("Message has no action: skipping")
            return

        delay = message.get(self.COMMANDS.DELAY, 0)
        if not isinstance(delay, (int, float)):
            logger.error("Delay must be int or float (received={}): skipping".format(delay))
            return

        if message[self.COMMANDS.ACTION] in self.play_pause_stop:
            action = self.play_pause_stop[message[self.COMMANDS.ACTION]]

            if self.COMMANDS.TRACK_ID not in message:
                logger.error("{} action has no track_id: skipping".format(action['verb']))
                return

            track_id = message[self.COMMANDS.TRACK_ID]
            logger.info("{} track id={}".format(action['ing'], track_id))

            track = self.tracks.get(track_id, None)
            if track is None:
                logger.error("Unknown track id={}: aborting".format(track_id))
                return

            reactor.callLater(delay, getattr(track, action['method']))

        elif message[self.COMMANDS.ACTION] == self.COMMANDS.ACTION_SET_VOLUME:
            if self.COMMANDS.VOLUME not in message:
                logger.error("Set volume action has not volume: skipping")
                return

            volume = message[self.COMMANDS.VOLUME]
            track_id = message.get(self.COMMANDS.TRACK_ID, None)
            duration = message.get(self.COMMANDS.DURATION, 0)
            ease = message.get(self.COMMANDS.EASE, 'easeInOutSine')

            self.set_volume(delay, volume, track_id, duration, ease)

        else:
            logger.debug("Unknown command type '{}': skipping".format(
                message[self.COMMANDS.ACTION]))

    def set_volume(self, delay, volume, track_id=None, duration=0, ease='easeInOutSine'):
        if not isinstance(volume, int):
            logger.error('Volume must be an int (received={}): aborting'.format(volume))
            return

        if track_id is not None and track_id not in self.tracks:
            logger.error('Unknown track id={}: aborting'.format(track_id))
            return

        if not isinstance(duration, int):
            logger.error('Duration must be an int (received={}): aborting'.format(duration))
            return

        if ease not in EASE_MAPPING:
            logger.error('Unknown easing function (received={}): aborting'.format(ease))
            return

        volume = min(volume, 100)
        volume = max(0, volume)

        duration = max(0, duration)

        ease = EASE_MAPPING[ease]

        if track_id is None:
            if self.master_volume is None:
                logger.error("Master volume has not been initialized properly: skipping")
                callable_ = None
            else:
                callable_ = self.master_volume.fade_volume
        else:
            callable_ = self.tracks[track_id].fade_volume

        if callable_:
            reactor.callLater(delay, callable_, volume, duration, ease)
