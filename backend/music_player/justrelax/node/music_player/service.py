import pyglet

from twisted.internet import reactor
from twisted.internet.task import LoopingCall

from justrelax.common.logging_utils import logger
from justrelax.node.service import JustSockClientService
from justrelax.node.common.volume import EASE_MAPPING, MasterVolume
from justrelax.node.music_player.vlc_player import VLCSelfReleasingTrackPlayer
from justrelax.node.music_player.vlc_player import VLCLoopingTrackPlayer
from justrelax.node.music_player.pyglet_player import PygletTrackPlayer
from justrelax.node.music_player.pyglet_player import PygletLoopingTrackPlayer


class MusicPlayer(JustSockClientService):
    class PROTOCOL:
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
        master_volume_mixer = self.node_params.get('mixer', '')
        default_initial_volume = self.node_params.get('default_volume', 100)

        player = self.node_params.get('player', 'vlc')
        if player == 'vlc':
            track_handler = VLCSelfReleasingTrackPlayer
            looping_track_handler = VLCLoopingTrackPlayer
        elif player == 'pyglet':
            track_handler = PygletTrackPlayer
            looping_track_handler = PygletLoopingTrackPlayer
            loop = LoopingCall(self.pyglet_loop)
            loop.start(1 / 30)
        else:
            raise ValueError(
                "Bad player value ({}). Possible values are vlc or "
                "pyglet.".format(player))

        try:
            self.master_volume = MasterVolume(
                initial_volume=initial_master_volume,
                mixer=master_volume_mixer,
            )
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
                    media_path=path,
                    loop_a=loop_a,
                    loop_b=loop_b,
                    initial_volume=volume,
                )
            else:
                handler = track_handler(
                    media_path=path,
                    initial_volume=volume,
                )
            self.tracks[id_] = handler

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

    def pyglet_loop(self):
        pyglet.clock.tick()
        pyglet.app.platform_event_loop.dispatch_posted_events()

    def process_event(self, event):
        logger.debug("Processing event '{}'".format(event))
        if type(event) is not dict:
            logger.error("Unknown event: skipping")
            return

        if self.PROTOCOL.ACTION not in event:
            logger.error("Event has no action: skipping")
            return

        delay = event.get(self.PROTOCOL.DELAY, 0)
        if not isinstance(delay, (int, float)):
            logger.error("Delay must be int or float (received={}): skipping".format(delay))
            return

        if event[self.PROTOCOL.ACTION] in self.play_pause_stop:
            action = self.play_pause_stop[event[self.PROTOCOL.ACTION]]

            if self.PROTOCOL.TRACK_ID not in event:
                logger.error("{} action has no track_id: skipping".format(action['verb']))
                return

            track_id = event[self.PROTOCOL.TRACK_ID]
            logger.info("{} track id={}".format(action['ing'], track_id))

            track = self.tracks.get(track_id, None)
            if track is None:
                logger.error("Unknown track id={}: aborting".format(track_id))
                return

            reactor.callLater(delay, getattr(track, action['method']))

        elif event[self.PROTOCOL.ACTION] == self.PROTOCOL.ACTION_SET_VOLUME:
            if self.PROTOCOL.VOLUME not in event:
                logger.error("Set volume action has no volume: skipping")
                return

            volume = event[self.PROTOCOL.VOLUME]
            track_id = event.get(self.PROTOCOL.TRACK_ID, None)
            duration = event.get(self.PROTOCOL.DURATION, 0)
            ease = event.get(self.PROTOCOL.EASE, 'easeInOutSine')

            self.set_volume(delay, volume, track_id, duration, ease)

        else:
            logger.debug("Unknown command type '{}': skipping".format(
                event[self.PROTOCOL.ACTION]))

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
