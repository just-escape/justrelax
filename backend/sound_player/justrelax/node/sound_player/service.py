import vlc
import pyglet

from twisted.internet import reactor
from twisted.internet.task import LoopingCall

from justrelax.common.logging_utils import logger
from justrelax.node.service import JustSockNodeClientService
from justrelax.node.common.volume import EASE_MAPPING, MasterVolume


class SoundPlayer(JustSockNodeClientService):
    class COMMANDS:
        ACTION = "action"

        SOUND_ID = "sound_id"
        DELAY = "delay"

        ACTION_PLAY = "play"

        ACTION_SET_VOLUME = "set_volume"
        VOLUME = "volume"
        DURATION = "duration"
        EASE = "ease"

    def start(self):
        initial_master_volume = self.node_params.get('master_volume', None)
        master_volume_mixer = self.node_params.get('mixer', '')
        default_initial_volume = self.node_params.get('default_volume', 100)

        player = self.node_params.get('player', 'pyglet')
        if player == 'vlc':
            self.sound_player = self.vlc_play_sound
        elif player == 'pyglet':
            self.sound_player = self.pyglet_play_sound
            self.pyglet_players = []
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

        self.sounds = {}
        for sound in self.node_params.get('sounds', []):
            id_ = sound['id']
            path = sound['path']
            volume = sound.get('volume', default_initial_volume)

            if player == 'vlc':
                media = vlc.Media(path)
                media.parse()
                # / 1000 because we will be interested by the value in seconds
                duration = media.get_duration() / 1000
                self.sounds[id_] = {
                    'media': media,
                    'duration': duration,
                    'volume': volume,
                }
            else:
                media = pyglet.media.load(path, streaming=False)
                self.sounds[id_] = {
                    'media': media,
                    'volume': volume,
                }

    def pyglet_loop(self):
        pyglet.clock.tick()
        pyglet.app.platform_event_loop.dispatch_posted_events()

    def process_message(self, message):
        logger.debug("Processing message '{}'".format(message))
        if type(message) is not dict:
            logger.debug("Unknown message: skipping")
            return

        if self.COMMANDS.ACTION not in message:
            logger.debug("Message has no action: skipping")
            return

        delay = message.get(self.COMMANDS.DELAY, 0)
        if not isinstance(delay, (int, float)):
            logger.error("Delay must be int or float (received={}): skipping".format(delay))
            return

        if message[self.COMMANDS.ACTION] == self.COMMANDS.ACTION_PLAY:
            if self.COMMANDS.SOUND_ID not in message:
                logger.error("Play action has no sound_id: skipping")
                return

            sound_id = message[self.COMMANDS.SOUND_ID]
            logger.info("Playing sound id={}".format(sound_id))

            sound = self.sounds.get(sound_id, None)
            if sound is None:
                logger.error("Unknown sound id={}: aborting".format(sound_id))
                return

            reactor.callLater(delay, self.sound_player, sound)

        elif message[self.COMMANDS.ACTION] == self.COMMANDS.ACTION_SET_VOLUME:
            if self.COMMANDS.VOLUME not in message:
                logger.error("Set volume action has not volume: skipping")
                return

            volume = message[self.COMMANDS.VOLUME]
            duration = message.get(self.COMMANDS.DURATION, 0)
            ease = message.get(self.COMMANDS.EASE, 'easeInOutSine')

            self.set_volume(delay, volume, duration, ease)

        else:
            logger.debug("Unknown command type '{}': skipping".format(
                message[self.COMMANDS.ACTION]))

    def pyglet_play_sound(self, sound):
        player = pyglet.media.Player()
        player.queue(sound['media'])
        player.volume = sound['volume'] / 100
        player.play()

        # prevent garbage collection
        self.pyglet_players.append(player)

        def remove_player_reference():
            self.pyglet_players.remove(player)

        player.on_player_eos = remove_player_reference

    def vlc_play_sound(self, sound):
        player = vlc.MediaPlayer()
        player.set_media(sound['media'])
        player.audio_set_volume(int(sound['volume']))
        player.play()

        def free_player():
            player.release()

        # Add 0.1 seconds by precaution
        reactor.callLater(sound['duration'] + 0.1, free_player)

    def set_volume(self, delay, volume, duration=0, ease='easeInOutSine'):
        if not isinstance(volume, int):
            logger.error('Volume must be an int (received={}): aborting'.format(volume))
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

        if self.master_volume is None:
            logger.error("Master volume has not been initialized properly: skipping")
        else:
            reactor.callLater(delay, self.master_volume.fade_volume, volume, duration, ease)
