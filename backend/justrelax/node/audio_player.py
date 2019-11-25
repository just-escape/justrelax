import time

import vlc
import pytweening

from twisted.internet import reactor

from justrelax.common.logging import logger
from justrelax.node.service import JustSockNodeClientService


class VolumeFaderMixin:
    def __init__(self, initial_volume=0, update_frequency=0.01):
        self.current_volume = initial_volume
        self.target_volume = initial_volume

        self.update_frequency = update_frequency

    def fade_volume(self, volume, duration=0, ease=pytweening.easeInOutSine):
        if duration == 0:
            self.current_volume += volume
            self.target_volume += volume
            self.set_volume()
        else:
            self._fade_volume(volume, duration, ease=ease)

    def _fade_volume(self, volume, duration, ease=pytweening.easeInOutSine):
        t_start = time.time()
        current_volume_diff = 0
        target_volume_diff = volume - self.target_volume
        self.target_volume = self.target_volume + target_volume_diff

        def update():
            now = time.time()
            progression = (now - t_start) * 1000 / duration

            nonlocal current_volume_diff
            if progression < 1:
                eased_progression = ease(progression)
                reactor.callLater(self.update_frequency, update)
            else:
                eased_progression = 1

            new_volume_diff = target_volume_diff * eased_progression - current_volume_diff
            self.current_volume += new_volume_diff
            current_volume_diff += new_volume_diff

            self.set_volume()

        reactor.callLater(self.update_frequency, update)

    def set_volume(self):
        pass


class GlobalVolume(VolumeFaderMixin):
    def __init__(self, initial_volume):
        super(GlobalVolume, self).__init__(initial_volume=initial_volume)
        self.track_handlers = []

    def set_volume(self):
        for th in self.track_handlers:
            th.set_volume()


class TrackHandler(VolumeFaderMixin):
    def __init__(self, audio_path, initial_volume=0, global_volume=None):
        if global_volume:
            self.global_volume = global_volume
        else:
            self.global_volume = GlobalVolume(initial_volume=100)
        self.global_volume.track_handlers.append(self)

        self.player = vlc.MediaPlayer(audio_path)

        super(TrackHandler, self).__init__(initial_volume=initial_volume)

        self.set_volume()

    def play(self):
        self.player.play()

    def pause(self):
        self.player.pause()

    def stop(self):
        self.player.stop()

    def set_volume(self):
        volume = int(
            self.global_volume.current_volume * self.current_volume / 100)
        self.player.audio_set_volume(volume)


class LoopingTrackHandler(TrackHandler):
    def __init__(self, audio_path, loop_a, loop_b, initial_volume=0, global_volume=None):
        super(LoopingTrackHandler, self).__init__(
            audio_path,
            initial_volume=initial_volume,
            global_volume=global_volume,
        )
        self.loop_a = loop_a
        self.loop_b = loop_b
        self.looping_task = None

    def play(self):
        if not self.player.is_playing():
            player_time = self.player.get_time()
            if player_time == -1:
                logger.debug('Player has not been started yet')
                self._play()
            else:
                logger.debug('Player had already been started')
                self._resume()
        else:
            logger.debug('Player is already playing: nothing to do')

    def _play(self):
        logger.debug('Playing track')
        self.player.play()
        logger.debug('Scheduling going to loop_a in {} seconds'.format(self.loop_b))
        self.looping_task = reactor.callLater(self.loop_b, self.go_to_loop_a)

    def go_to_loop_a(self):
        time_before_loop = self.loop_b - self.loop_a
        logger.debug('Scheduling going to loop_a in {} seconds'.format(time_before_loop))
        self.looping_task = reactor.callLater(time_before_loop, self.go_to_loop_a)

        logger.debug('Setting player time to {}'.format(self.loop_a))
        self.player.set_time(int(self.loop_a * 1000))

    def pause(self):
        if not self.player.can_pause():
            # at the beginning or after a stop
            logger.debug('Player cannot be paused: nothing to do')
            return

        if self.player.is_playing():
            logger.debug('Player is playing: pausing')
            self._pause()
        else:
            logger.debug('Player is playing: resuming')
            self._resume()

    def _pause(self):
        try:
            logger.debug('Cancelling looping task')
            self.looping_task.cancel()
        except Exception as e:
            logger.warning("Could not cancel looping task (reason={})".format(e))
        logger.debug('Pausing player')
        self.player.pause()

    def _resume(self):
        logger.debug('Resuming')
        current_time = self.player.get_time() / 1000
        time_before_loop = self.loop_b - current_time
        self.player.pause()
        logger.debug('Scheduling going to loop_a in {} seconds'.format(time_before_loop))
        self.looping_task = reactor.callLater(time_before_loop, self.go_to_loop_a)

    def stop(self):
        try:
            logger.debug('Cancelling looping task')
            self.looping_task.cancel()
        except Exception as e:
            logger.warning("Could not cancel looping task (reason={})".format(e))
        logger.debug('Stopping player')
        self.player.stop()


class AudioPlayer(JustSockNodeClientService):
    EASE_MAPPING = {
        'easeInSine': pytweening.easeInSine,
        'easeOutSine': pytweening.easeOutSine,
        'easeInOutSine': pytweening.easeInOutSine,
        'easeInCubic': pytweening.easeInCubic,
        'easeOutCubic': pytweening.easeOutCubic,
        'easeInOutCubic': pytweening.easeInOutCubic,
        'easeInQuint': pytweening.easeInQuint,
        'easeOutQuint': pytweening.easeOutQuint,
        'easeInOutQuint': pytweening.easeInOutQuint,
        'easeInCirc': pytweening.easeInCirc,
        'easeOutCirc': pytweening.easeOutCirc,
        'easeInOutCirc': pytweening.easeInOutCirc,
        'easeInElastic': pytweening.easeInElastic,
        'easeOutElastic': pytweening.easeOutElastic,
        'easeInOutElastic': pytweening.easeInOutElastic,
        'easeInQuad': pytweening.easeInQuad,
        'easeOutQuad': pytweening.easeOutQuad,
        'easeInOutQuad': pytweening.easeInOutQuad,
        'easeInQuart': pytweening.easeInQuart,
        'easeOutQuart': pytweening.easeOutQuart,
        'easeInExpo': pytweening.easeInExpo,
        'easeOutExpo': pytweening.easeOutExpo,
        'easeInOutExpo': pytweening.easeInOutExpo,
        'easeInBack': pytweening.easeInBack,
        'easeOutBack': pytweening.easeOutBack,
        'easeInOutBack': pytweening.easeInOutBack,
        'easeInBounce': pytweening.easeInBounce,
        'easeOutBounce': pytweening.easeOutBounce,
        'easeInOutBounce': pytweening.easeInOutBounce,
        'linear': pytweening.linear,
    }

    class COMMANDS:
        ACTION = "action"

        ACTION_PLAY_SOUND = "play_sound"
        SOUND_ID = "sound_id"

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
        self.global_volume = GlobalVolume(initial_volume=100)

        self.tracks = {}
        for track in self.service_params['tracks']:
            mode = track.get('mode', 'one_shot')
            if mode == 'loop':
                handler = LoopingTrackHandler(
                    audio_path=track['path'],
                    loop_a=track['loop_a'],
                    loop_b=track['loop_b'],
                    initial_volume=70,
                    global_volume=self.global_volume,
                )
            else:
                handler = TrackHandler(
                    audio_path=track['path'],
                    initial_volume=70,
                    global_volume=self.global_volume,
                )
            self.tracks[track['id']] = handler

        self.sounds = {}
        for sound in self.service_params['sounds']:
            media = vlc.Media(sound['path'])
            media.parse()
            # / 1000 because we will be interested by the value in seconds
            duration = media.get_duration() / 1000
            self.sounds[sound['id']] = {
                'path': sound['path'],
                'duration': duration,
            }

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

        elif message[self.COMMANDS.ACTION] == self.COMMANDS.ACTION_PLAY_SOUND:
            if self.COMMANDS.SOUND_ID not in message:
                logger.error("Play sound action has no sound_id: skipping")
                return

            sound_id = message[self.COMMANDS.SOUND_ID]
            logger.info("Playing sound id={}".format(sound_id))

            reactor.callLater(delay, self.play_sound, sound_id)

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

    def play_sound(self, sound_id):
        sound = self.sounds.get(sound_id, None)
        if sound is None:
            logger.error("Unknown sound id={}: aborting".format(sound_id))
            return

        player = vlc.MediaPlayer(sound['path'])
        player.audio_set_volume(int(self.global_volume.current_volume))
        player.play()

        def free_player():
            player.release()

        # Add 0.1 seconds by precaution
        reactor.callLater(sound['duration'] + 0.1, free_player)

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

        if ease not in self.EASE_MAPPING:
            logger.error('Unknown easing function (received={}): aborting'.format(ease))
            return

        volume = min(volume, 100)
        volume = max(0, volume)

        duration = max(0, duration)

        ease = self.EASE_MAPPING[ease]

        if track_id is None:
            callable_ = self.global_volume.fade_volume
        else:
            callable_ = self.tracks[track_id].fade_volume

        reactor.callLater(delay, callable_, volume, duration, ease)
