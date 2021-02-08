import pyglet

from twisted.internet import reactor
from twisted.internet.task import LoopingCall

from justrelax.common.logging_utils import logger
from justrelax.node.service import OrchestratorNode, on_event
from justrelax.node.media.volume import EASE_MAPPING, MasterVolume
from justrelax.node.music_player.vlc_player import VLCSelfReleasingTrackPlayer
from justrelax.node.music_player.vlc_player import VLCLoopingTrackPlayer
from justrelax.node.music_player.pyglet_player import PygletTrackPlayer
from justrelax.node.music_player.pyglet_player import PygletLoopingTrackPlayer


class MusicPlayer(OrchestratorNode):
    def __init__(self, *args, **kwargs):
        super(MusicPlayer, self).__init__(*args, **kwargs)

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

    def pyglet_loop(self):
        pyglet.clock.tick()
        pyglet.app.platform_event_loop.dispatch_posted_events()

    def play_pause_stop(self, action, method, track_id, delay=0):
        if not isinstance(delay, (int, float)):
            raise ValueError("Delay must be int or float (received={}): skipping".format(delay))

        logger.info("{} track id={}".format(action, track_id))

        track = self.tracks.get(track_id, None)
        if track is None:
            raise ValueError("Unknown track id={}: aborting".format(track_id))

        reactor.callLater(delay, getattr(track, method))

    @on_event(filter={'category': 'play'})
    def event_play(self, track_id: str, delay=0):
        self.play_pause_stop("Playing", "play", track_id, delay)

    @on_event(filter={'category': 'pause'})
    def event_pause(self, track_id: str, delay=0):
        self.play_pause_stop("Pausing", "pause", track_id, delay)

    @on_event(filter={'category': 'stop'})
    def event_stop(self, track_id: str, delay=0):
        self.play_pause_stop("Stopping", "stop", track_id, delay)

    @on_event(filter={'category': 'set_volume'})
    def event_set_volume(self, volume: int, track_id=None, duration=0, ease: str = 'easeInOutSine', delay=0):
        if not isinstance(delay, (int, float)):
            raise ValueError("Delay must be int or float (received={}): skipping".format(delay))

        if not isinstance(duration, (int, float)):
            raise ValueError("Delay must be int or float (received={}): skipping".format(delay))

        if ease not in EASE_MAPPING:
            raise ValueError('Unknown easing function (received={}): aborting'.format(ease))

        if track_id is not None and track_id not in self.tracks:
            raise ValueError('Unknown track id={}: aborting'.format(track_id))

        volume = min(volume, 100)
        volume = max(0, volume)

        duration = max(0, duration)

        ease = EASE_MAPPING[ease]

        if track_id is None:
            if self.master_volume is None:
                raise ValueError("Master volume has not been initialized properly: skipping")
            else:
                callable_ = self.master_volume.fade_volume
        else:
            callable_ = self.tracks[track_id].fade_volume

        reactor.callLater(delay, callable_, volume, duration, ease)
