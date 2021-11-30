import json
import time
import uuid

from twisted.internet import reactor

from justrelax.core.logging_utils import logger
from justrelax.core.node import MagicNode, on_event

STATE_NOT_STARTED = 'not_started'
STATE_TICKING = 'ticking'
STATE_PAUSED = 'paused'


class Timer:
    def __init__(self, delay, repeat=False, callback=None, *args, **kwargs):
        self.delay = delay
        self.repeat = repeat
        self.callback = callback
        self.callback_args = args
        self.callback_kwargs = kwargs

        self.task = None
        self.last_computed_delay = 0.
        self.last_schedule_timestamp = 0.
        self.manual_pause = False

    def get_remaining_time(self):
        if not self.task or not self.task.active():
            return 0.

        remaining_time = self.last_schedule_timestamp + self.last_computed_delay - time.monotonic()

        return round(remaining_time, 2)

    def start(self):
        now = time.monotonic()

        self.cancel()
        self.manual_pause = False

        self.last_computed_delay = self.delay
        self.last_schedule_timestamp = now
        self.task = reactor.callLater(self.delay, self.perform_task)

    def manual_pause(self):
        self.manual_pause = True
        self._pause()

    def session_pause(self):
        self._pause()

    def _pause(self):
        if self.task and self.task.active():
            now = time.monotonic()
            delta_since_last_schedule = now - self.last_schedule_timestamp
            if delta_since_last_schedule > self.last_computed_delay:
                logger.warning(
                    "Timer precision issue (now={}, last_schedule_timestamp={}, delta={}, last_computed_delay={}): "
                    "rounding last_computed_delay to 0".format(
                        now, self.last_schedule_timestamp, delta_since_last_schedule, self.last_computed_delay
                    )
                )
                self.last_computed_delay = 0
            else:
                self.last_computed_delay -= delta_since_last_schedule
            self.task.cancel()

    def manual_resume(self):
        self.manual_pause = False
        self._resume()

    def session_resume(self):
        self._resume()

    def _resume(self):
        if self.task and not self.task.active() and not self.manual_pause:
            now = time.monotonic()
            self.last_schedule_timestamp = now
            self.task = reactor.callLater(self.last_computed_delay, self.perform_task)

    def cancel(self):
        if self.task and self.task.active():
            self.task.cancel()
            self.task = None

    def perform_task(self):
        if self.repeat:
            self.start()
        else:
            self.task = None

        self.callback(*self.callback_args, **self.callback_kwargs)


class SessionTimer:
    def __init__(self, tic_tac_callback=None):
        self.tic_tac_callback = tic_tac_callback

        self.tic_tac_period = 1  # seconds

        self.state = STATE_NOT_STARTED
        self.session_time = 0.

        self.task = None
        self.last_computed_delay = 0.
        self.last_schedule_timestamp = 0.

    def start(self):
        if self.state == STATE_NOT_STARTED:
            self.last_schedule_timestamp = time.monotonic()
            self.schedule_next_tic_tac()
            self.state = STATE_TICKING

    def schedule_next_tic_tac(self):
        now = time.monotonic()
        delta_since_last_schedule = now - self.last_schedule_timestamp
        self.last_schedule_timestamp = now

        self.session_time += delta_since_last_schedule
        delay_before_next_call = self.tic_tac_period - self.session_time % self.tic_tac_period
        self.task = reactor.callLater(delay_before_next_call, self.tic_tac)

    def pause(self):
        if self.state == STATE_TICKING:
            delta_since_last_schedule = time.monotonic() - self.last_schedule_timestamp
            self.last_computed_delay = self.tic_tac_period - delta_since_last_schedule
            self.session_time += delta_since_last_schedule
            self.task.cancel()
            self.state = STATE_PAUSED
        elif self.state == STATE_NOT_STARTED:
            self.state = STATE_PAUSED

    def resume(self):
        if self.state == STATE_PAUSED:
            now = time.monotonic()
            self.last_schedule_timestamp = now
            self.task = reactor.callLater(self.last_computed_delay, self.tic_tac)
            self.state = STATE_TICKING

    def cancel(self):
        if self.state == STATE_PAUSED:
            self.session_time = 0.
            self.state = STATE_NOT_STARTED

    def tic_tac(self):
        self.schedule_next_tic_tac()
        if self.tic_tac_callback:
            self.tic_tac_callback(self.session_time)


class Scenario(MagicNode):
    DIFFICULTIES = {'easy', 'normal', 'hard'}

    MS_PEPPER_INTRO_DURATION = 35
    NIRYO_BUGGED_ANIMATION_DURATION = 23

    PERSISTENT_SCENARIO_SETTINGS = [
        'niryo_animation',
        'ms_pepper_intro',
        'epileptic_mode',
        'final_by_refectory',
        'dry_print',
    ]

    def __init__(self, *args, **kwargs):
        super(Scenario, self).__init__(*args, **kwargs)

        self.publication_channel_prefix = self.config['publication_channel_prefix']

        self.niryo_animation_duration = self.config['niryo_animation_duration']
        self.niryo_end_conveyor_duration = self.config['niryo_end_conveyor_duration']
        self.oven_cooking_duration = self.config['oven_cooking_duration']
        self.first_waffle_init_conveyor_duration = self.config['first_waffle_init_conveyor_duration']
        self.first_pattern_print_duration = self.config['first_pattern_print_duration']
        self.first_waffle_end_conveyor_duration = self.config['first_waffle_end_conveyor_duration']
        self.basket_led_blinking_time = self.config['basket_led_blinking_time']
        self.delay_before_ms_pepper_says_thanks = self.config['delay_before_ms_pepper_says_thanks']

        self.session_timer = SessionTimer(self.tic_tac_callback)
        self.session_time = None
        self.session_data = {}

        self.initial_difficulty = 'normal'

        # Those delayed calls are canceled on a room reset
        self.registered_delayed_tasks = {}

        with open(self.config['persistent_settings'], 'r') as fh:
            self.persistent_settings = json.load(fh)

        self.timers = {
            'modify_fx': Timer(0, False, self.modify_fx),  # 0 because the delay is computed in start_room
            'track1_light_animation_1_first_trigger': Timer(21.25, False, self.track1_light_animation_1),
            'track1_light_animation_1_second_trigger': Timer(220.107125, False, self.track1_light_animation_1),
            'track1_light_animation_1_loop_trigger': Timer(120.678563, False, self.track1_light_animation_1),
            'track1_light_animation_2_first_trigger': Timer(29.75, False, self.track1_light_animation_2),
            'track1_light_animation_2_second_trigger': Timer(228.607125, False, self.track1_light_animation_2),
            'track1_light_animation_2_loop_trigger': Timer(129.178563, False, self.track1_light_animation_2),
            'track1_light_animation_3_first_trigger': Timer(51.75, False, self.track1_light_animation_3),
            'track1_light_animation_3_second_trigger': Timer(250.607125, False, self.track1_light_animation_3),
            'track1_light_animation_3_loop_trigger': Timer(151.178563, False, self.track1_light_animation_3),
            'track1_light_animation_4_first_trigger': Timer(82.25, False, self.track1_light_animation_4),
            'track1_light_animation_4_second_trigger': Timer(281.107125, False, self.track1_light_animation_4),
            'track1_light_animation_4_loop_trigger': Timer(181.678563, False, self.track1_light_animation_4),
            'track1_light_animation_5_first_trigger': Timer(90, False, self.track1_light_animation_5),
            'track1_light_animation_5_second_trigger': Timer(288.857125, False, self.track1_light_animation_5),
            'track1_light_animation_5_loop_trigger': Timer(189.428563, False, self.track1_light_animation_5),
            'track1_light_animation_6_first_trigger': Timer(161.5, False, self.track1_light_animation_6),
            'track1_light_animation_6_loop_trigger': Timer(62.071438, False, self.track1_light_animation_6),
            'track1_light_animation_7_first_trigger': Timer(182.5, False, self.track1_light_animation_7),
            'track1_light_animation_7_loop_trigger': Timer(83.071438, False, self.track1_light_animation_7),
            'light_service_success_animation': Timer(1, False, self.light_service_success_animation),
            'stop_track_alarm': Timer(1, False, self.stop_track_alarm)
        }

        self.track1_light_first_timers = [
            'track1_light_animation_1_first_trigger',
            'track1_light_animation_1_second_trigger',
            'track1_light_animation_2_first_trigger',
            'track1_light_animation_2_second_trigger',
            'track1_light_animation_3_first_trigger',
            'track1_light_animation_3_second_trigger',
            'track1_light_animation_4_first_trigger',
            'track1_light_animation_4_second_trigger',
            'track1_light_animation_5_first_trigger',
            'track1_light_animation_5_second_trigger',
            'track1_light_animation_6_first_trigger',
            'track1_light_animation_7_first_trigger',
        ]

        self.track1_light_loop_timers = [
            'track1_light_animation_1_loop_trigger',
            'track1_light_animation_2_loop_trigger',
            'track1_light_animation_3_loop_trigger',
            'track1_light_animation_4_loop_trigger',
            'track1_light_animation_5_loop_trigger',
            'track1_light_animation_6_loop_trigger',
            'track1_light_animation_7_loop_trigger',
        ]

        self.holomenu_slide = None
        self.holomenu_x = None
        self.holomenu_y = None
        self.holomenu_error = None
        self.holomenu_slides_mapping = [
            [
                'salade_flamande', 'protobulle', 'insectosteak', 'steakfie'
            ],
            [
                'pizzalgue', 'cambraisienne', 'pizzaliere', 'pizzage'
            ],
            [
                'algaufre', 'nano_gaufre', 'spider_gaufre', 'gaufresque'
            ],
            [
                'flubber', 'chtite_gelee', 'potjevleesch', 'puddy_puddy'
            ],
        ]

        self.is_control_panel_in_manual_mode = False

    def publish_prefix(self, event, channel):
        self.publish(event, "{}{}".format(self.publication_channel_prefix, channel))

    def register_delayed_task(self, delay, callable, *callable_args, **callable_kwargs):
        task_id = str(uuid.uuid4())

        def unregistered_and_call():
            self.registered_delayed_tasks.pop(task_id)
            callable(*callable_args, **callable_kwargs)

        self.registered_delayed_tasks[task_id] = reactor.callLater(delay, unregistered_and_call)

    def tic_tac_callback(self, seconds):
        self.session_time = int(seconds) if seconds else seconds
        self.publish_prefix({'category': 'set_session_time', 'seconds': self.session_time}, 'street_display')
        self.publish_game_time_to_webmin()

    def on_first_connection(self):
        for key in self.PERSISTENT_SCENARIO_SETTINGS:
            self._record_session_data(key, self.persistent_settings[key])
        self.publish_prefix({'category': 'request_node_session_data'}, 'broadcast')

    @on_event(filter={'from': 'webmin', 'widget_id': 'start_stop', 'action': 'run'})
    def run_room_from_webmin(self):
        self.run_room()

    @on_event(filter={'from': 'street_display', 'category': 'play'})
    def run_room_from_street_display(self):
        self.run_room()

    @on_event(filter={'widget_id': 'start_synchronized'})
    def start_synchronized(self):
        self.set_session_data('ms_pepper_intro', True)
        if self.session_timer.state == STATE_NOT_STARTED:
            self.start_room()

    @on_event(filter={'widget_id': 'play_ms_pepper_here_you_are'})
    def play_ms_pepper_here_you_are(self):
        self.publish_prefix(
            {
                'category': 'pause',
                'video_id': 'ads_glitch'  # if self.initial_difficulty == 'hard' else 'waffresco_ad_loop',
            },
            'advertiser'
        )
        self.publish_prefix({'category': 'play', 'video_id': 'ms_pepper_here_you_are'}, 'advertiser')

        self.register_delayed_task(
            self.MS_PEPPER_INTRO_DURATION, self.publish_prefix,
            {
                'category': 'play',
                'video_id': 'ads_glitch'  # if self.initial_difficulty == 'hard' else 'waffresco_ad_loop',
            },
            'advertiser'
        )

    def run_room(self):
        if self.session_timer.state == STATE_NOT_STARTED:
            self.start_room()
        elif self.session_timer.state == STATE_PAUSED:
            self.resume_room()

    def start_room(self):
        def after_ms_pepper_here_you_are():
            self.publish_prefix(
                {
                    'category': 'play',
                    'video_id': 'ads_glitch'  # if self.initial_difficulty == 'hard' else 'waffresco_ad_loop',
                },
                'advertiser'
            )
            self.publish_prefix({'category': 'set_volume', 'track_id': 'track1', 'volume': 75}, 'music_player')
            self.publish_prefix({'category': 'play', 'track_id': 'track1'}, 'music_player')
            self.publish_prefix({'category': 'play', 'track_id': 'chaotic_atmosphere'}, 'music_player')

        def open_the_door():
            self.publish_prefix({'category': 'play', 'sound_id': 'front_door_open'}, 'sound_player')
            self.publish_prefix({'category': 'unlock', 'relock': True}, 'front_door_magnet')
            self.session_timer.start()

        self.publish_prefix({'category': 'calibrate'}, 'load_cells')
        self.publish_prefix({'category': 'on', 'color': 'orange'}, 'refectory_lights')
        self.publish_prefix({'category': 'on', 'color': 'green'}, 'refectory_lights')
        self.publish_prefix({'category': 'on', 'color': 'red'}, 'refectory_lights')
        self.publish_prefix({'category': 'on', 'color': 'pink'}, 'refectory_lights')
        self.publish_prefix({'category': 'glitch', 'color': 'blue'}, 'refectory_lights')
        self.publish_prefix({'category': 'glitch', 'color': 'pink'}, 'refectory_lights')
        self.publish_prefix({'category': 'glitch', 'color': 'red'}, 'refectory_lights')
        self.publish_prefix({'category': 'glitch', 'color': 'green'}, 'refectory_lights')
        self.publish_prefix({'category': 'glitch', 'color': 'orange'}, 'refectory_lights')

        self.publish_prefix(
            {
                'category': 'pause',
                'video_id': 'ads_glitch'  # if self.initial_difficulty == 'hard' else 'waffresco_ad_loop',
            },
            'advertiser'
        )

        if self.persistent_settings['ms_pepper_intro']:
            self.publish_prefix({'category': 'play', 'video_id': 'ms_pepper_here_you_are'}, 'advertiser')

        real_intro_duration = self.MS_PEPPER_INTRO_DURATION if self.persistent_settings['ms_pepper_intro'] else 0
        self.timers['modify_fx'].delay = real_intro_duration + 18.285
        self.register_delayed_task(real_intro_duration, after_ms_pepper_here_you_are)
        self.register_delayed_task(real_intro_duration + 3, open_the_door)

        self.timers['modify_fx'].start()

    def modify_fx(self):
        self.schedule_track1_light_animations()
        self.publish_prefix({'category': 'on', 'color': 'blue'}, 'refectory_lights')
        self.publish_prefix(
            {'category': 'set_volume', 'track_id': 'track1', 'volume': 50, 'duration': 30}, 'music_player')
        self.register_delayed_task(
            85,
            self.publish_prefix,
            {'category': 'set_volume', 'track_id': 'track1', 'volume': 40, 'duration': 60},
            'music_player'
        )

    def schedule_track1_light_animations(self):
        for timer in self.track1_light_first_timers:
            logger.info("triggering in {} seconds".format(self.timers[timer].delay))
            self.timers[timer].start()

    def cancel_track1_light_animations(self):
        self.timers['modify_fx'].cancel()

        for timer in self.track1_light_first_timers:
            self.timers[timer].cancel()

        for timer in self.track1_light_loop_timers:
            self.timers[timer].cancel()

    @on_event(filter={'category': 'track_loop', 'track_id': 'track1'})
    def track_1_has_looped(self):
        for timer in self.track1_light_loop_timers:
            self.timers[timer].start()

    @on_event(filter={'category': 'track_pause', 'track_id': 'track1'})
    def track_1_has_paused(self):
        for timer in self.track1_light_first_timers:
            self.timers[timer].pause()

        for timer in self.track1_light_loop_timers:
            self.timers[timer].pause()

    @on_event(filter={'category': 'track_stop', 'track_id': 'track1'})
    def track_1_has_stopped(self):
        for timer in self.track1_light_first_timers:
            self.timers[timer].cancel()

        for timer in self.track1_light_loop_timers:
            self.timers[timer].cancel()

    @on_event(filter={'category': 'track_resume', 'track_id': 'track1'})
    def track_1_has_resumed(self):
        for timer in self.track1_light_first_timers:
            self.timers[timer].resume()

        for timer in self.track1_light_loop_timers:
            self.timers[timer].resume()

    def track1_light_animation_1(self):
        if not self.persistent_settings['epileptic_mode']:
            self.publish_prefix(
                {'category': 'play_animation', 'name': 'glitch1', 'color': 'all_but_white', 'duration': 2.01},
                'refectory_lights')

    def track1_light_animation_2(self):
        if not self.persistent_settings['epileptic_mode']:
            self.publish_prefix(
                {'category': 'play_animation', 'name': 'glitch_off_on', 'color': 'all_but_white', 'duration': 1.75},
                'refectory_lights')

    def track1_light_animation_3(self):
        if not self.persistent_settings['epileptic_mode']:
            self.publish_prefix(
                {'category': 'play_animation', 'name': 'glitch_off_on', 'color': 'all_but_white', 'duration': 2.5},
                'refectory_lights')

    def track1_light_animation_4(self):
        if not self.persistent_settings['epileptic_mode']:
            self.publish_prefix(
                {'category': 'play_animation', 'name': 'glitch2', 'color': 'all_but_white', 'duration': 1.01},
                'refectory_lights')

    def track1_light_animation_5(self):
        if not self.persistent_settings['epileptic_mode']:
            self.publish_prefix(
                {'category': 'play_animation', 'name': 'glitch3', 'color': 'all_but_white', 'duration': 1.01},
                'refectory_lights')

    def track1_light_animation_6(self):
        if not self.persistent_settings['epileptic_mode']:
            self.publish_prefix(
                {'category': 'play_animation', 'name': 'glitch_off_on', 'color': 'all_but_white', 'duration': 0.5},
                'refectory_lights')

    def track1_light_animation_7(self):
        if not self.persistent_settings['epileptic_mode']:
            self.publish_prefix(
                {'category': 'play_animation', 'name': 'glitch4', 'color': 'all_but_white', 'duration': 1.01},
                'refectory_lights')

    def resume_room(self):
        self.session_timer.resume()
        for timer_name, timer in self.timers.items():
            timer.session_resume()

    @on_event(filter={'from': 'webmin', 'widget_id': 'start_stop', 'action': 'halt'})
    def halt_room(self):
        if self.session_timer.state in [STATE_NOT_STARTED, STATE_TICKING]:
            for timer_name, timer in self.timers.items():
                timer.session_pause()
            self.session_timer.pause()

    @on_event(filter={'from': 'webmin', 'widget_id': 'start_stop', 'action': 'reset'})
    def reset_room(self):
        if self.session_timer.state != STATE_PAUSED:
            return

        for timer_name, timer in self.timers.items():
            timer.cancel()
        self.session_timer.cancel()
        self.session_time = None

        registered_delayed_task_ids = list(self.registered_delayed_tasks)
        for registered_delayed_task_id in registered_delayed_task_ids:
            task = self.registered_delayed_tasks.pop(registered_delayed_task_id)
            task.cancel()

        self.publish_game_time_to_webmin()

        # Note: the table is not automatically reset
        self.publish_prefix({'category': 'reset'}, 'broadcast')

        self.holomenu_slide = None
        self.holomenu_x = None
        self.holomenu_y = None
        self.holomenu_error = None

    @on_event(filter={'from': 'webmin', 'category': 'request_session_data_for_webmin'})
    def on_request_session_data(self):
        self.publish_game_time_to_webmin()
        for key, value in self.session_data.items():
            self.publish_prefix({"category": "set_session_data", "key": key, "data": value}, "webmin")

    def publish_game_time_to_webmin(self):
        self.publish_prefix({'category': 'set_session_data', 'key': 'game_time', 'data': self.session_time}, 'webmin')

    @on_event(filter={'category': 'set_session_data'})
    def set_session_data(self, key: str, data):
        self._record_session_data(key, data)

        if key in self.PERSISTENT_SCENARIO_SETTINGS:
            self.persistent_settings[key] = data
            with open(self.config['persistent_settings'], 'w') as fh:
                json.dump(self.persistent_settings, fh)

    def _record_session_data(self, key, data):
        self.session_data[key] = data
        self.publish_prefix(
            {"category": "set_session_data", "key": key, "data": data}, "webmin")

    @on_event(filter={'from': 'street_display', 'category': 'unlock_front_door'})
    def street_display_event_unlock_front_door(self):
        self.publish_prefix({'category': 'play', 'sound_id': 'front_door_open'}, 'sound_player')
        self.publish_prefix({'category': 'unlock', 'relock': True}, 'front_door_magnet')

    @on_event(filter={'from': 'chopsticks', 'category': 'set_color'})
    def chopsticks_event_set_color(self, new_color: str):
        if new_color == 'blue':
            self.publish_prefix({'category': 'play', 'sound_id': 'ambiant_light_blue'}, 'sound_player')
        elif new_color == 'orange':
            self.publish_prefix({'category': 'play', 'sound_id': 'ambiant_light_orange'}, 'sound_player')

    @on_event(filter={'from': 'chopsticks', 'category': 'success'})
    def chopsticks_event_success(self):
        self.publish_prefix({'category': 'set_status', 'status': 'playing'}, 'control_panel')

    @on_event(filter={'from': 'control_panel', 'category': 'first_manual_mode'})
    def control_panel_event_manual_mode(self):
        self.cancel_track1_light_animations()
        self.publish_prefix({'category': 'stop', 'track_id': 'track1'}, 'music_player')
        self.publish_prefix({'category': 'stop', 'track_id': 'chaotic_atmosphere'}, 'music_player')
        self.publish_prefix({'category': 'play', 'track_id': 'track2'}, 'music_player')
        self.register_delayed_task(
            5, self.publish_prefix, {'category': 'play', 'track_id': 'atmosphere'}, 'music_player')
        self.publish_prefix({'category': 'play', 'sound_id': 'on_manual_mode'}, 'sound_player')
        self.publish_prefix({'category': 'play_overlay_video', 'video_id': 'glitching_less'}, 'orders')
        self.publish_prefix({'category': 'stop_overlay_video'}, 'synchronizer')
        self.publish_prefix({'category': 'play', 'video_id': 'ads_loop'}, 'advertiser')
        self.publish_prefix({'category': 'stop', 'video_id': 'ads_glitch'}, 'advertiser')
        self.publish_prefix({'category': 'stop', 'video_id': 'waffresco_ad_loop'}, 'advertiser')

        self.publish_prefix({'category': 'restaurant_in_manual_mode'}, 'synchronizer')
        self.publish_prefix(
            {
                'category': 'light_log',
                'message': 'lights_have_been_reset',
                'level': 'warning',
                'use_locale': True,
                'with_sound': False,
            },
            'synchronizer'
        )
        self.publish_prefix(
            {
                'category': 'light_log',
                'message': 'lights_have_been_turned_off',
                'level': 'info',
                'use_locale': True,
                'with_sound': False,
            },
            'synchronizer'
        )
        self.publish_prefix(
            {
                'category': 'light_log',
                'message': 'lights_can_be_turned_on_manually',
                'level': 'info',
                'use_locale': True,
                'with_sound': False,
            },
            'synchronizer'
        )
        self.publish_prefix(
            {
                'category': 'light_log',
                'message': 'waiting_lights_to_be_resync',
                'level': 'info',
                'use_locale': True,
                'with_sound': False,
            },
            'synchronizer'
        )
        self.publish_prefix(
            {
                'category': 'menu_log',
                'message': 'menu_is_messed_up',
                'level': 'warning',
                'use_locale': True,
                'with_sound': False,
            },
            'synchronizer'
        )
        self.publish_prefix(
            {
                'category': 'menu_log',
                'message': 'waiting_dishes_to_be_configured',
                'level': 'info',
                'use_locale': True,
                'with_sound': False,
            },
            'synchronizer'
        )

        self.register_delayed_task(0.2, self.publish_prefix, {'category': 'off', 'color': 'all'}, 'refectory_lights')
        self.register_delayed_task(
            0.2, self.publish_prefix, {'category': 'stop_glitch', 'color': 'blue'}, 'refectory_lights')
        self.register_delayed_task(
            0.2, self.publish_prefix, {'category': 'stop_glitch', 'color': 'pink'}, 'refectory_lights')
        self.register_delayed_task(
            0.2, self.publish_prefix, {'category': 'stop_glitch', 'color': 'red'}, 'refectory_lights')
        self.register_delayed_task(
            0.2, self.publish_prefix, {'category': 'stop_glitch', 'color': 'green'}, 'refectory_lights')
        self.register_delayed_task(
            0.2, self.publish_prefix, {'category': 'stop_glitch', 'color': 'orange'}, 'refectory_lights')

    @on_event(filter={'from': 'synchronizer', 'category': 'set_menu_entry'})
    def synchronizer_event_set_menu_entry(self, dish: str, index: int, on_manual_mode: bool):
        if not on_manual_mode:
            self.register_delayed_task(0.1, self.publish_prefix, {'category': 'play', 'sound_id': 'hologram_set_slide'}, 'sound_player')
        self.publish_prefix({'category': 'set_slide', 'chapter_id': dish, 'slide_index': index}, 'holographic_menu')

    def light_service_success_animation(self):
        if not self.persistent_settings['epileptic_mode']:
            self.publish_prefix(
                {'category': 'play_animation', 'name': 'refectory_repaired', 'color': 'all_but_white'},
                'refectory_lights')
            self.publish_prefix({'category': 'off', 'color': 'white'}, 'refectory_lights')

        else:
            self.publish_prefix({'category': 'on', 'color': 'all_but_white'}, 'refectory_lights')
            self.publish_prefix({'category': 'off', 'color': 'white'}, 'refectory_lights')

    @on_event(filter={'from': 'synchronizer', 'category': 'light_service_success'})
    def synchronizer_event_light_service_success(self):
        self.timers['light_service_success_animation'].start()
        self.publish_prefix({'category': 'set_lights_service_status', 'repaired': True}, 'control_panel')

    @on_event(filter={'from': 'synchronizer', 'category': 'menu_service_success'})
    def synchronizer_event_menu_service_success(self):
        self.publish_prefix({'category': 'set_menu_service_status', 'repaired': True}, 'control_panel')

    @on_event(filter={'from': 'synchronizer', 'category': 'services_synchronization_success'})
    def synchronizer_event_services_synchronization_success(self):
        self.publish_prefix({'category': 'play', 'sound_id': 'on_restaurant_start'}, 'sound_player')

        if self.timers['light_service_success_animation'].task:
            self.timers['light_service_success_animation'].cancel()
            if not self.persistent_settings['epileptic_mode']:
                self.register_delayed_task(
                    5, self.publish_prefix,
                    {'category': 'play_animation', 'name': 'refectory_repaired', 'color': 'all'}, 'refectory_lights')
            else:
                self.register_delayed_task(
                    5, self.publish_prefix, {'category': 'on', 'color': 'all'}, 'refectory_lights')
        else:
            if not self.persistent_settings['epileptic_mode']:
                self.register_delayed_task(
                    5, self.publish_prefix,
                    {'category': 'play_animation', 'name': 'refectory_repaired', 'color': 'white'}, 'refectory_lights')
            else:
                self.register_delayed_task(
                    5, self.publish_prefix, {'category': 'on', 'color': 'white'}, 'refectory_lights')

        self.publish_prefix({'category': 'stop_glitch', 'color': 'blue'}, 'street_lights')
        self.publish_prefix({'category': 'stop_glitch', 'color': 'orange'}, 'street_lights')

        self.publish_prefix(
            {'category': 'set_volume', 'track_id': 'track2', 'volume': 0, 'duration': 5}, 'music_player')
        self.register_delayed_task(10, self.publish_prefix, {'category': 'stop', 'track_id': 'track2'}, 'music_player')

        self.publish_prefix({'category': 'set_volume', 'track_id': 'track3', 'volume': 30}, 'music_player')
        self.register_delayed_task(
            6, self.publish_prefix,
            {'category': 'set_volume', 'track_id': 'track3', 'volume': 50, 'duration': 3}, 'music_player')
        self.register_delayed_task(6, self.publish_prefix, {'category': 'play', 'track_id': 'track3'}, 'music_player')

        self.register_delayed_task(
            8, self.publish_prefix, {'category': 'set_status', 'status': 'playing'}, 'payment_module')
        self.register_delayed_task(8, self.publish_prefix, {'category': 'stop_overlay_video'}, 'orders')

        self.register_delayed_task(
            6, self.publish_prefix, {'category': 'play_overlay_video', 'video_id': 'ads_loop'}, 'synchronizer')

    @on_event(filter={'from': 'holographic_menu', 'category': 'play_slide'})
    def holographic_menu_event_play_slide(self, slide: int):
        self.publish_prefix({'category': 'set_menu_cursor_position', 'position': slide}, 'synchronizer')

    @on_event(filter={'from': 'load_cells', 'category': 'load_cell'})
    def load_cells_event_load_cell(self, color: str, id: int, activated: bool):
        self.publish_prefix({'category': 'load_cell', 'color': color, 'id': id, 'activated': activated}, 'synchronizer')

    @on_event(filter={'from': 'synchronizer', 'category': 'on'})
    def synchronizer_event_on(self, color: str):
        self.publish_prefix({'category': 'on', 'color': color}, 'refectory_lights')

    @on_event(filter={'from': 'synchronizer', 'category': 'off'})
    def synchronizer_event_off(self, color: str):
        self.publish_prefix({'category': 'off', 'color': color}, 'refectory_lights')

    @on_event(filter={'from': 'orders', 'category': 'first_order'})
    def orders_first_order(self):
        self.publish_prefix(
            {'category': 'set_volume', 'track_id': 'track3', 'volume': 0, 'duration': 2}, 'music_player')
        self.register_delayed_task(
            1, self.publish_prefix, {'category': 'light_on', 'led_id': 'niryo'}, 'waffle_factory')
        self.register_delayed_task(
            1, self.publish_prefix, {'category': 'play', 'track_id': 'track5'}, 'music_player')

        self.register_delayed_task(
            1.5, self.publish_prefix, {'category': 'off', 'color': 'white'}, 'refectory_lights')
        self.register_delayed_task(
            1.5, self.publish_prefix, {'category': 'off', 'color': 'blue'}, 'refectory_lights')

        self.register_delayed_task(
            6, self.publish_prefix, {'category': 'play_animation', 'animation': 'bugged_animation'}, 'niryo')
        self.register_delayed_task(
            6, self.publish_prefix, {'category': 'play_animation', 'animation': 'niryo_init'}, 'waffle_factory')

        self.register_delayed_task(
            self.NIRYO_BUGGED_ANIMATION_DURATION + 6, self.publish_prefix,
            {'category': 'set_volume', 'track_id': 'track3', 'volume': 35, 'duration': 1}, 'music_player')
        self.register_delayed_task(
            self.NIRYO_BUGGED_ANIMATION_DURATION + 6, self.publish_prefix,
            {'category': 'set_volume', 'track_id': 'track5', 'volume': 0, 'duration': 1}, 'music_player')
        self.register_delayed_task(
            self.NIRYO_BUGGED_ANIMATION_DURATION + 6.5,
            self.publish_prefix, {'category': 'on', 'color': 'white'}, 'refectory_lights')
        self.register_delayed_task(
            self.NIRYO_BUGGED_ANIMATION_DURATION + 6.5,
            self.publish_prefix, {'category': 'on', 'color': 'blue'}, 'refectory_lights')
        self.register_delayed_task(
            self.NIRYO_BUGGED_ANIMATION_DURATION + 6 + 1, self.publish_prefix,
            {'category': 'stop', 'track_id': 'track5'}, 'music_player')
        self.register_delayed_task(
            self.NIRYO_BUGGED_ANIMATION_DURATION + 7, self.publish_prefix,
            {'category': 'play_overlay_video', 'video_id': 'ms_pepper_stock'}, 'orders')
        self.register_delayed_task(
            self.NIRYO_BUGGED_ANIMATION_DURATION + 7, self.publish_prefix,
            {'category': 'play_ms_pepper_overlay_video', 'video_id': 'ms_pepper_stock'}, 'synchronizer')
        self.register_delayed_task(
            self.NIRYO_BUGGED_ANIMATION_DURATION + 6, self.publish_prefix,
            {'category': 'stop', 'video_id': 'street_idle'}, 'advertiser')
        self.register_delayed_task(
            self.NIRYO_BUGGED_ANIMATION_DURATION + 7, self.publish_prefix,
            {'category': 'play', 'video_id': 'ms_pepper_stock'}, 'advertiser')
        ms_pepper_tells_to_go_in_stock_duration = 27.25
        self.register_delayed_task(
            self.NIRYO_BUGGED_ANIMATION_DURATION + ms_pepper_tells_to_go_in_stock_duration + 7 + 1,  # + 1 to be sure
            self.publish_prefix, {'category': 'play', 'video_id': 'street_idle'}, 'advertiser')

    @on_event(filter={'from': 'orders', 'category': 'ms_pepper_has_told_to_go_in_stock'})
    def ms_pepper_has_told_to_go_in_stock(self):
        def post_delay():
            self.publish_prefix({'category': 'set_status', 'status': 'playing'}, 'ventilation_panel')

            self.publish_prefix(
                {'category': 'set_volume', 'track_id': 'track3', 'volume': 0, 'duration': 5}, 'music_player')

            self.publish_prefix({'category': 'set_volume', 'track_id': 'track35', 'volume': 0}, 'music_player')
            self.register_delayed_task(
                2.5, self.publish_prefix, {'category': 'play', 'track_id': 'track35'}, 'music_player')
            self.register_delayed_task(
                2.5, self.publish_prefix,
                {'category': 'set_volume', 'track_id': 'track35', 'volume': 40, 'duration': 1}, 'music_player')

        self.register_delayed_task(1, post_delay)

        self.publish_prefix(
            {
                "category": "log",
                "use_locale": True,
                "message": "waffresco_order",
                "level": "warning",
                "with_sound": False
            },
            "inventory"
        )
        self.publish_prefix(
            {
                "category": "log",
                "use_locale": True,
                "message": "analysis",
                "level": "info",
                "with_sound": False
            },
            "inventory"
        )
        self.publish_prefix(
            {
                "category": "log",
                "use_locale": True,
                "message": "temperature_control_ok",
                "level": "info",
                "with_sound": False
            },
            "inventory"
        )
        self.publish_prefix(
            {
                "category": "log",
                "use_locale": True,
                "message": "humidity_control_ok",
                "level": "info",
                "with_sound": False
            },
            "inventory"
        )
        self.publish_prefix(
            {
                "category": "log",
                "use_locale": True,
                "message": "stocks_control_error",
                "level": "warning",
                "with_sound": False
            },
            "inventory"
        )
        self.publish_prefix(
            {
                "category": "log",
                "use_locale": True,
                "message": "nutrients_missing",
                "level": "warning",
                "with_sound": False
            },
            "inventory"
        )
        self.publish_prefix(
            {
                "category": "log",
                "use_locale": True,
                "message": "human_intervention_required",
                "level": "info",
                "with_sound": False
            },
            "inventory"
        )

    @on_event(filter={'from': 'orders', 'category': 'resume_order'})
    def orders_resume_order(self):
        self.register_delayed_task(
            0.5, self.publish_prefix,
            {'category': 'set_volume', 'track_id': 'track3', 'volume': 0, 'duration': 2}, 'music_player')
        self.register_delayed_task(
            1, self.publish_prefix,
            {'category': 'play', 'track_id': 'track5'}, 'music_player')
        self.register_delayed_task(
            1, self.publish_prefix,
            {'category': 'set_volume', 'track_id': 'track5', 'volume': 55, 'duration': 1}, 'music_player')

        self.register_delayed_task(
            1.5, self.publish_prefix, {'category': 'off', 'color': 'white'}, 'refectory_lights')
        self.register_delayed_task(
            1.5, self.publish_prefix, {'category': 'off', 'color': 'blue'}, 'refectory_lights')

        delay = 4
        self.register_delayed_task(
            delay, self.publish_prefix, {'category': 'play_animation', 'animation': 'animation'}, 'niryo')

        delay += self.niryo_animation_duration
        self.register_delayed_task(
            delay, self.publish_prefix, {'category': 'play_animation', 'animation': 'niryo_end'}, 'waffle_factory')

        delay += self.niryo_end_conveyor_duration
        self.register_delayed_task(
            delay, self.publish_prefix, {'category': 'oven_turn_on'}, 'waffle_factory')

        delay += self.oven_cooking_duration
        self.register_delayed_task(
            delay, self.publish_prefix, {'category': 'oven_turn_off'}, 'waffle_factory')
        self.register_delayed_task(
            max(0, delay - 1), self.publish_prefix, {'category': 'light_on', 'led_id': 'printer'}, 'waffle_factory')
        self.register_delayed_task(
            delay + 0.5, self.publish_prefix,
            {'category': 'play_animation', 'animation': 'first_waffle_init'}, 'waffle_factory')

        delay += self.first_waffle_init_conveyor_duration
        if self.persistent_settings['dry_print'] is False:
            self.register_delayed_task(
                delay, self.publish_prefix,
                {'category': 'print_pattern', 'pattern': 'a'}, 'waffle_factory')

        delay += self.first_pattern_print_duration
        self.register_delayed_task(
            delay, self.publish_prefix,
            {'category': 'play_animation', 'animation': 'waffle_end'}, 'waffle_factory')

        delay += self.first_waffle_end_conveyor_duration
        self.register_delayed_task(
            delay, self.publish_prefix,
            {'category': 'basket_led_blink'}, 'waffle_factory')

        self.register_delayed_task(
            delay + self.basket_led_blinking_time, self.publish_prefix,
            {'category': 'basket_led_off'}, 'waffle_factory')

        delay += self.delay_before_ms_pepper_says_thanks
        self.register_delayed_task(
            delay - 1.5, self.publish_prefix,
            {'category': 'set_volume', 'track_id': 'track5', 'volume': 0, 'duration': 1}, 'music_player')
        self.register_delayed_task(
            delay - 1.5 + 0.5, self.publish_prefix,
            {'category': 'on', 'color': 'white'}, 'refectory_lights')
        self.register_delayed_task(
            delay - 1.5 + 0.5, self.publish_prefix,
            {'category': 'on', 'color': 'blue'}, 'refectory_lights')
        self.register_delayed_task(
            delay, self.publish_prefix,
            {'category': 'play', 'track_id': 'track62'}, 'music_player')

        self.register_delayed_task(
            delay, self.publish_prefix,
            {'category': 'play_overlay_video', 'video_id': 'ms_pepper_says_thanks'}, 'orders')
        self.register_delayed_task(
            delay, self.publish_prefix,
            {'category': 'play_ms_pepper_overlay_video', 'video_id': 'ms_pepper_says_thanks'}, 'synchronizer')
        self.register_delayed_task(
            delay - 1, self.publish_prefix,
            {'category': 'stop', 'video_id': 'street_idle'}, 'advertiser')
        self.register_delayed_task(
            delay, self.publish_prefix,
            {'category': 'play', 'video_id': 'ms_pepper_says_thanks'}, 'advertiser')

        ms_pepper_says_thanks_duration = 17
        self.register_delayed_task(
            delay + ms_pepper_says_thanks_duration + 1,  # + 1 just to be sure
            self.publish_prefix, {'category': 'play', 'video_id': 'street_idle'}, 'advertiser')

        self.register_delayed_task(
            delay + 1, self.publish_prefix,
            {'category': 'set_restaurant_status', 'closed': True}, 'orders')
        self.register_delayed_task(
            delay + 1, self.publish_prefix,
            {'category': 'reset_order'}, 'orders')  # Empty the cart

    @on_event(filter={'from': 'orders', 'category': 'ms_pepper_has_said_thanks'})
    def orders_ms_pepper_has_said_thanks(self):
        self.publish_prefix(
            {'category': 'set_volume', 'track_id': 'track62', 'volume': 0, 'duration': 10}, 'music_player')
        self.register_delayed_task(1.5, self.publish_prefix, {'category': 'play', 'track_id': 'track7'}, 'music_player')
        self.register_delayed_task(
            37.5 + 1.5, self.publish_prefix,
            {'category': 'set_volume', 'track_id': 'track7', 'volume': 55, 'duration': 1}, 'music_player')
        self.register_delayed_task(
            37.5 + 25 + 1.5, self.publish_prefix,
            {'category': 'set_volume', 'track_id': 'track7', 'volume': 45, 'duration': 10}, 'music_player')

    @on_event(filter={'from': 'orders', 'category': 'marmitron_has_asked_for_help'})
    def orders_marmitron_has_asked_for_help(self):
        self.publish_prefix({'category': 'enable'}, 'digital_lock')
        self.publish_prefix({'category': 'calibrate'}, 'secure_floor')
        self.register_delayed_task(3, self.publish_prefix, {'category': 'send_fog', 'duration': 20}, 'fog_machine')
        self.register_delayed_task(
            10, self.publish_prefix, {'category': 'set_display_order_recap_notification', 'value': True}, 'orders')

    @on_event(filter={'from': 'payment_module', 'category': 'set_credits'})
    def payment_module_event_set_credits(self, value):
        self.publish_prefix({'category': 'set_credits', 'value': value}, 'orders')

    @on_event(filter={'from': 'ventilation_panel', 'category': 'good_connection'})
    def ventilation_panel_event_good_connection(self, sequence_cursor: int):
        if 0 <= sequence_cursor <= 8:
            self.publish_prefix(
                {'category': 'play', 'sound_id': f'ventilation_combo_{sequence_cursor}'}, 'sound_player')

    @on_event(filter={'from': 'ventilation_panel', 'category': 'bad_move'})
    def ventilation_panel_event_bad_move(self):
        self.publish_prefix({'category': 'play', 'sound_id': 'ventilation_error'}, 'sound_player')

    @on_event(filter={'from': 'ventilation_panel', 'category': 'round_complete'})
    def ventilation_panel_event_round_complete(self):
        self.register_delayed_task(
            0.5, self.publish_prefix, {'category': 'play', 'sound_id': 'ventilation_round_success'}, 'sound_player')

    @on_event(filter={'from': 'ventilation_panel', 'category': 'start_new_round'})
    def ventilation_panel_event_start_new_round(self, round: int):
        self.publish_prefix({'category': 'set_ventilation_panel_round', 'round': round}, 'orders')

    @on_event(filter={'from': 'ventilation_panel', 'category': 'set_status'})
    def ventilation_panel_event_set_status(self, status: str):
        if status == 'playing':
            self.publish_prefix({'category': 'set_documentation_visibility', 'show': True}, 'orders')
        else:
            self.publish_prefix({'category': 'set_documentation_visibility', 'show': False}, 'orders')

    @on_event(filter={'from': 'ventilation_panel', 'category': 'notify_instruction'})
    def ventilation_panel_notify_instruction(self, instruction):
        self.publish_prefix(
            {'category': 'set_documentation_current_instruction', 'message': instruction, 'use_locale': True},
            'orders'
        )

    @on_event(filter={'from': 'ventilation_panel', 'category': 'success'})
    def ventilation_panel_success(self):
        self.publish_prefix({'category': 'on'}, 'fog_machine')
        self.publish_prefix({'category': 'unlock'}, 'vents_locker')
        self.publish_prefix({'category': 'display_black_screen', 'display': False}, 'inventory')

        self.register_delayed_task(1, self.publish_prefix, {'category': 'stop', 'track_id': 'track35'}, 'music_player')
        self.register_delayed_task(1, self.publish_prefix, {'category': 'play', 'track_id': 'track4'}, 'music_player')

        self.register_delayed_task(4, self.publish_prefix, {'category': 'high'}, 'stock_lights')

    @on_event(filter={'from': 'orders', 'category': 'restart_round'})
    def ventilation_panel_restart_round(self):
        self.publish_prefix({'category': 'restart_round'}, 'ventilation_panel')

    @on_event(filter={'from': 'sokoban_controls', 'category': 'control'})
    def sokoban_controls_event(self, name: str, pressed: bool):
        self.publish_prefix({'category': 'control', 'name': name, 'pressed': pressed}, 'inventory')

    @on_event(filter={'from': 'cylinders', 'category': 'tag'})
    def cylinder_tag(self, tag):
        if tag:
            self.publish_prefix({'category': 'play', 'sound_id': 'cylinder_scan'}, 'sound_player')

    @on_event(filter={'from': 'cylinders', 'category': 'check_availability_scan'})
    def cylinder_check_availability_scan(self):
        self.publish_prefix({'category': 'play', 'sound_id': 'cylinder_scan'}, 'sound_player')

    @on_event(filter={'from': 'cylinders', 'category': 'success'})
    def cylinders_success(self):
        self.publish_prefix(
            {
                "category": "log",
                "use_locale": True,
                "message": "stocks_control_ok",
                "level": "info",
                "with_sound": True
            },
            "inventory"
        )
        self.publish_prefix(
            {
                "category": "log",
                "use_locale": True,
                "message": "orders_can_resume",
                "level": "info",
                "with_sound": False
            },
            "inventory"
        )
        self.publish_prefix(
            {
                "category": "log",
                "use_locale": True,
                "message": "waiting_customer_validation",
                "level": "info",
                "with_sound": False
            },
            "inventory"
        )
        self.publish_prefix({"category": "set_stocks_status", "status": True}, "inventory")
        self.publish_prefix({'category': 'set_display_resume_order_notification', 'value': True}, 'orders')

        self.publish_prefix(
            {'category': 'set_volume', 'track_id': 'track4', 'volume': 0, 'duration': 10}, 'music_player')
        self.register_delayed_task(10, self.publish_prefix, {'category': 'stop', 'track_id': 'track4'}, 'music_player')

        self.register_delayed_task(
            4, self.publish_prefix,
            {'category': 'set_volume', 'track_id': 'track3', 'volume': 53, 'duration': 6},
            'music_player')
        self.register_delayed_task(6, self.publish_prefix, {'category': 'low'}, 'stock_lights')

    @on_event(filter={'from': 'digital_lock', 'category': 'success'})
    def digital_lock_success(self):
        self.publish_prefix({'category': 'set_status', 'status': 'playing'}, 'secure_floor')
        self.publish_prefix({'category': 'playing'}, 'laser_maze')
        self.publish_prefix({'category': 'playing'}, 'human_authenticator')

        self.publish_prefix(
            {'category': 'set_volume', 'track_id': 'track7', 'volume': 0, 'duration': 5}, 'music_player')
        self.register_delayed_task(5, self.publish_prefix, {'category': 'stop', 'track_id': 'track7'}, 'music_player')
        self.register_delayed_task(
            0.3, self.publish_prefix, {'category': 'set_volume', 'track_id': 'track8', 'volume': 75}, 'music_player')
        self.register_delayed_task(1, self.publish_prefix, {'category': 'play', 'track_id': 'track8'}, 'music_player')
        self.register_delayed_task(
            0.3, self.publish_prefix,
            {'category': 'set_volume', 'track_id': 'track8', 'volume': 50, 'duration': 30}, 'music_player')
        self.register_delayed_task(
            0.6, self.publish_prefix, {'category': 'low'}, 'stock_lights')
        self.register_delayed_task(
            1, self.publish_prefix, {'category': 'unlock', 'magnet_id': 'stock_to_machine'}, 'emergency_exit')
        self.register_delayed_task(
            1, self.publish_prefix, {'category': 'play', 'sound_id': 'server_door_open'}, 'sound_player')
        self.register_delayed_task(
            5, self.publish_prefix, {'category': 'set_display_order_recap_notification', 'value': False}, 'orders')

        # Disable the payment module at this point for players not to think it could be useful in the last room with
        # other human authenticators
        self.register_delayed_task(
            10, self.publish_prefix, {'category': 'set_status', 'status': 'disabled'}, 'payment_module')

    @on_event(filter={'from': 'secure_floor', 'category': 'clear'})
    def secure_floor_event_clear(self):
        self.publish_prefix({'category': 'playing'}, 'laser_maze')
        self.publish_prefix({'category': 'set_status', 'status': 'playing'}, 'human_authenticator')
        self.publish_prefix({'category': 'set_volume', 'track_id': 'alarm', 'volume': 0, 'duration': 1}, 'music_player')
        self.publish_prefix({'category': 'display_alarm_window', 'display': False}, 'root_server')
        self.publish_prefix({'category': 'display_alarm_window', 'display': False}, 'digital_lock')
        self.timers['stop_track_alarm'].start()

    def stop_track_alarm(self):
        self.publish_prefix({'category': 'stop', 'track_id': 'alarm'}, 'music_player')

    @on_event(filter={'from': 'laser_maze', 'category': 'alarm'})
    def laser_maze_event_alarm(self):
        self.publish_prefix({'category': 'stop_playing'}, 'laser_maze')
        self.publish_prefix({'category': 'set_status', 'status': 'alarm'}, 'secure_floor')
        self.publish_prefix({'category': 'set_status', 'status': 'disabled'}, 'human_authenticator')
        self.publish_prefix({'category': 'play', 'sound_id': 'laser_trigger'}, 'sound_player')
        self.timers['stop_track_alarm'].cancel()
        self.publish_prefix({'category': 'set_volume', 'track_id': 'alarm', 'volume': 40}, 'music_player')
        self.publish_prefix({'category': 'play', 'track_id': 'alarm'}, 'music_player')
        self.publish_prefix({'category': 'display_alarm_window', 'display': True}, 'root_server')
        self.publish_prefix({'category': 'display_alarm_window', 'display': True}, 'digital_lock')

    @on_event(filter={'from': 'human_authenticator', 'category': 'success'})
    def human_authenticator_event_success(self):
        self.publish_prefix({'category': 'set_success', 'value': True}, 'laser_maze')
        self.publish_prefix({'category': 'success'}, 'secure_floor')
        self.publish_prefix({'category': 'show_ui'}, 'root_server')
        self.publish_prefix({'category': 'display_alarm_window', 'display': False}, 'root_server')
        self.publish_prefix({'category': 'display_alarm_window', 'display': False}, 'digital_lock')
        self.register_delayed_task(
            3, self.publish_prefix, {'category': 'display_password_window'}, 'root_server')
        self.register_delayed_task(
            4.5, self.publish_prefix, {'category': 'play_animation', 'animation': 'reponse'}, 'root_server')

    @on_event(filter={'from': 'root_server', 'category': 'check_availability'})
    def root_server_check_availability(self, id: str):
        self.publish_prefix({'category': 'check_availability', 'id': id}, 'cylinders')

    @on_event(filter={'from': 'cylinders', 'category': 'availability'})
    def cylinders_availability(self, id: str, missing_ingredients: int):
        self.publish_prefix(
            {'category': 'availability', 'id': id, 'missing_ingredients': missing_ingredients}, 'root_server')

    @on_event(filter={'from': 'root_server', 'category': 'success'})
    def root_server_event_success(self):
        self.publish_prefix(
            {'category': 'set_volume', 'track_id': 'track8', 'volume': 35, 'duration': 5}, 'music_player')
        self.register_delayed_task(
            16, self.publish_prefix, {'category': 'set_volume', 'track_id': 'track8', 'volume': 0, 'duration': 10},
            'music_player')
        self.register_delayed_task(26, self.publish_prefix, {'category': 'stop', 'track_id': 'track8'}, 'music_player')

        # Note: track91 will stop by itself since it's not configured in loop mode
        self.publish_prefix(
            {'category': 'set_volume', 'track_id': 'track91', 'volume': 0, 'duration': 0}, 'music_player')
        self.publish_prefix({'category': 'play', 'track_id': 'track91'}, 'music_player')
        self.publish_prefix(
            {'category': 'set_volume', 'track_id': 'track91', 'volume': 60, 'duration': 5}, 'music_player')

        self.register_delayed_task(
            16, self.publish_prefix, {'category': 'set_volume', 'track_id': 'track92', 'volume': 0, 'duration': 0},
            'music_player')
        self.register_delayed_task(
            16, self.publish_prefix, {'category': 'set_volume', 'track_id': 'track92', 'volume': 55, 'duration': 2},
            'music_player')
        self.register_delayed_task(
            16, self.publish_prefix, {'category': 'play', 'track_id': 'track92'}, 'music_player')

        self.register_delayed_task(
            50, self.publish_prefix, {'category': 'set_volume', 'track_id': 'track92', 'volume': 0, 'duration': 5},
            'music_player')
        self.register_delayed_task(
            55, self.publish_prefix, {'category': 'stop', 'track_id': 'track92'}, 'music_player')

        def post_delay():
            self.publish_prefix({'category': 'set_marmitron_visibility', 'show': False}, 'orders')
            self.publish_prefix({'category': 'final_animation'}, 'root_server')

        self.register_delayed_task(2, post_delay)

    @on_event(filter={'from': 'root_server', 'category': 'ms_pepper_mad_end'})
    def root_server_event_ms_pepper_mad_end(self):
        self.publish_prefix({'category': 'display_danger_window'}, 'synchronizer')
        self.publish_prefix({'category': 'display_danger_window'}, 'orders')
        self.publish_prefix({'category': 'display_danger_window'}, 'inventory')
        self.publish_prefix({'category': 'display_danger_window'}, 'root_server')
        self.publish_prefix({'category': 'alarm', 'activated': True}, 'relays')
        self.publish_prefix({'category': 'forced_alarm'}, 'secure_floor')
        self.publish_prefix({'category': 'set_status', 'status': 'disabled'}, 'human_authenticator')
        self.publish_prefix({'category': 'send_fog', 'duration': 10}, 'fog_machine')
        self.publish_prefix({'category': 'play', 'sound_id': 'gaz'}, 'sound_player')
        self.register_delayed_task(2, self.publish_prefix, {'category': 'play', 'track_id': 'alarm'}, 'music_player')
        self.register_delayed_task(
            30, self.publish_prefix, {'category': 'set_volume', 'track_id': 'alarm', 'volume': 0, 'duration': 5},
            'music_player')
        self.register_delayed_task(
            35, self.publish_prefix, {'category': 'stop', 'track_id': 'alarm'}, 'music_player')

        if self.persistent_settings['final_by_refectory']:
            self.register_delayed_task(
                10, self.publish_prefix, {'category': 'play', 'sound_id': 'front_door_open'}, 'sound_player')
            self.register_delayed_task(
                10, self.publish_prefix, {'category': 'unlock', 'relock': True}, 'front_door_magnet')
        else:
            self.publish_prefix({'category': 'unlock', 'magnet_id': 'to_outside', 'relock': True}, 'emergency_exit')

        self.session_timer.pause()

    @on_event(filter={'widget_id': 'front_door_open'})
    def button_front_door_open(self):
        self.publish_prefix({'category': 'play', 'sound_id': 'front_door_open'}, 'sound_player')
        self.publish_prefix({'category': 'unlock'}, 'front_door_magnet')

    @on_event(filter={'widget_id': 'front_door_close'})
    def button_front_door_close(self):
        self.publish_prefix({'category': 'lock'}, 'front_door_magnet')

    @on_event(filter={'widget_id': 'street_display_reset'})
    def button_street_display_reset(self):
        self.publish_prefix({'category': 'reset'}, 'street_display')

    @on_event(filter={'widget_id': 'advertiser_play_ms_pepper_here_you_are'})
    def button_advertiser_play_ms_pepper_here_you_are(self):
        self.publish_prefix({'category': 'play', 'video_id': 'ms_pepper_here_you_are'}, 'advertiser')

    @on_event(filter={'widget_id': 'advertiser_stop_ms_pepper_here_you_are'})
    def button_advertiser_stop_ms_pepper_here_you_are(self):
        self.publish_prefix({'category': 'stop', 'video_id': 'ms_pepper_here_you_are'}, 'advertiser')

    @on_event(filter={'widget_id': 'advertiser_play_ads_loop'})
    def button_advertiser_play_ads_loop(self):
        self.publish_prefix({'category': 'play', 'video_id': 'ads_loop'}, 'advertiser')

    @on_event(filter={'widget_id': 'advertiser_stop_ads_loop'})
    def button_advertiser_stop_ads_loop(self):
        self.publish_prefix({'category': 'stop', 'video_id': 'ads_loop'}, 'advertiser')

    @on_event(filter={'widget_id': 'advertiser_play_ads_glitch'})
    def button_advertiser_play_ads_glitch(self):
        self.publish_prefix({'category': 'play', 'video_id': 'ads_glitch'}, 'advertiser')

    @on_event(filter={'widget_id': 'advertiser_stop_ads_glitch'})
    def button_advertiser_stop_ads_glitch(self):
        self.publish_prefix({'category': 'stop', 'video_id': 'ads_glitch'}, 'advertiser')

    @on_event(filter={'widget_id': 'advertiser_play_waffresco_ad_loop'})
    def button_advertiser_play_waffresco_ad_loop(self):
        self.publish_prefix({'category': 'play', 'video_id': 'waffresco_ad_loop'}, 'advertiser')

    @on_event(filter={'widget_id': 'advertiser_stop_waffresco_ad_loop'})
    def button_advertiser_stop_waffresco_ad_loop(self):
        self.publish_prefix({'category': 'stop', 'video_id': 'waffresco_ad_loop'}, 'advertiser')

    @on_event(filter={'widget_id': 'advertiser_play_street_idle'})
    def button_advertiser_play_street_idle(self):
        self.publish_prefix({'category': 'play', 'video_id': 'street_idle'}, 'advertiser')

    @on_event(filter={'widget_id': 'advertiser_stop_street_idle'})
    def button_advertiser_stop_street_idle(self):
        self.publish_prefix({'category': 'stop', 'video_id': 'street_idle'}, 'advertiser')

    @on_event(filter={'widget_id': 'orders_play_ms_pepper_says_thanks'})
    def button_orders_play_ms_pepper_says_thanks(self):
        self.publish_prefix({'category': 'play_overlay_video', 'video_id': 'ms_pepper_says_thanks'}, 'orders')

    @on_event(filter={'widget_id': 'orders_play_ms_pepper_stock'})
    def button_orders_play_ms_pepper_stock(self):
        self.publish_prefix({'category': 'play_overlay_video', 'video_id': 'ms_pepper_stock'}, 'orders')

    @on_event(filter={'widget_id': 'orders_play_glitching'})
    def button_orders_play_glitching(self):
        self.publish_prefix({'category': 'play_overlay_video', 'video_id': 'glitching'}, 'orders')

    @on_event(filter={'widget_id': 'orders_play_glitching_less'})
    def button_orders_play_glitching_less(self):
        self.publish_prefix({'category': 'play_overlay_video', 'video_id': 'glitching_less'}, 'orders')

    @on_event(filter={'widget_id': 'orders_set_restaurant_open'})
    def button_orders_set_restaurant_open(self):
        self.publish_prefix({'category': 'set_restaurant_status', 'closed': False}, 'orders')

    @on_event(filter={'widget_id': 'orders_set_restaurant_closed'})
    def button_orders_set_restaurant_closed(self):
        self.publish_prefix({'category': 'set_restaurant_status', 'closed': True}, 'orders')

    @on_event(filter={'widget_id': 'orders_hide_marmitron'})
    def button_orders_hide_marmitron(self):
        self.publish_prefix({'category': 'set_marmitron_visibility', 'show': False}, 'orders')

    @on_event(filter={'widget_id': 'set_synchronizer_difficulty_easy'})
    def button_set_synchronizer_difficulty_easy(self):
        self.publish_prefix({'category': 'set_difficulty', 'difficulty': 'easy'}, 'synchronizer')

    @on_event(filter={'widget_id': 'set_synchronizer_difficulty_normal'})
    def button_set_synchronizer_difficulty_normal(self):
        self.publish_prefix({'category': 'set_difficulty', 'difficulty': 'normal'}, 'synchronizer')

    @on_event(filter={'widget_id': 'set_synchronizer_difficulty_hard'})
    def button_set_synchronizer_difficulty_hard(self):
        self.publish_prefix({'category': 'set_difficulty', 'difficulty': 'hard'}, 'synchronizer')

    @on_event(filter={'widget_id': 'reset_synchronizer'})
    def button_reset_synchronizer(self):
        self.publish_prefix({'category': 'reset'}, 'synchronizer')

    @on_event(filter={'widget_id': 'synchronizer_overlay_video_glitch'})
    def button_synchronizer_overlay_video_gltich(self):
        self.publish_prefix({'category': 'play_overlay_video', 'video_id': 'glitching'}, 'synchronizer')

    @on_event(filter={'widget_id': 'synchronizer_overlay_video_ads'})
    def button_synchronizer_overlay_video_ads(self):
        self.publish_prefix({'category': 'play_overlay_video', 'video_id': 'ads_loop'}, 'synchronizer')

    @on_event(filter={'widget_id': 'synchronizer_success_lights'})
    def button_synchronizer_success_lights(self):
        self.publish_prefix({'category': 'force_light_success'}, 'synchronizer')

    @on_event(filter={'widget_id': 'synchronizer_success_menu'})
    def button_synchronizer_success_menu(self):
        self.publish_prefix({'category': 'force_menu_success'}, 'synchronizer')

    @on_event(filter={'widget_id': 'stop_synchronizer_overlay_video'})
    def button_stop_synchronizer_overlay_video(self):
        self.publish_prefix({'category': 'stop_overlay_video'}, 'synchronizer')

    @on_event(filter={'widget_id': 'display_synchronizer_danger_window'})
    def button_display_synchronizer_danger_window(self):
        self.publish_prefix({'category': 'display_danger_window'}, 'synchronizer')

    @on_event(filter={'widget_id': 'maze_playing'})
    def button_maze_playing(self):
        self.publish_prefix({'category': 'set_status', 'status': 'playing'}, 'secure_floor')
        self.publish_prefix({'category': 'playing'}, 'laser_maze')
        self.publish_prefix({'category': 'playing'}, 'human_authenticator')

    @on_event(filter={'widget_id': 'maze_alarm'})
    def button_maze_alarm(self):
        self.publish_prefix({'category': 'set_status', 'status': 'alarm'}, 'secure_floor')
        self.publish_prefix({'category': 'stop_playing'}, 'laser_maze')
        self.publish_prefix({'category': 'set_status', 'status': 'disabled'}, 'human_authenticator')

    @on_event(filter={'widget_id': 'secure_floor_calibrate'})
    def button_secure_floor_calibrate(self):
        self.publish_prefix({'category': 'calibrate'}, 'secure_floor')

    @on_event(filter={'widget_id': 'maze_success'})
    def button_maze_success(self):
        self.publish_prefix({'category': 'success'}, 'secure_floor')
        self.publish_prefix({'category': 'set_success', 'value': True}, 'laser_maze')
        self.publish_prefix({'set_status': 'category', 'status': 'success'}, 'human_authenticator')

    @on_event(filter={'widget_id': 'maze_reset'})
    def button_maze_reset(self):
        self.publish_prefix({'category': 'reset'}, 'laser_maze')
        self.publish_prefix({'category': 'reset'}, 'secure_floor')
        self.publish_prefix({'category': 'reset'}, 'human_authenticator')
        self.publish_prefix({'category': 'set_volume', 'track_id': 'alarm', 'volume': 0}, 'music_player')
        self.publish_prefix({'category': 'display_alarm_window', 'display': False}, 'root_server')
        self.publish_prefix({'category': 'display_alarm_window', 'display': False}, 'digital_lock')

    @on_event(filter={'widget_id': 'set_lasers_difficulty_easy'})
    def button_set_lasers_difficulty_easy(self):
        self.publish_prefix({'category': 'set_difficulty', 'difficulty': 'easy'}, 'laser_maze')

    @on_event(filter={'widget_id': 'set_lasers_difficulty_normal'})
    def button_set_lasers_difficulty_normal(self):
        self.publish_prefix({'category': 'set_difficulty', 'difficulty': 'normal'}, 'laser_maze')

    @on_event(filter={'widget_id': 'set_lasers_difficulty_hard'})
    def button_set_lasers_difficulty_hard(self):
        self.publish_prefix({'category': 'set_difficulty', 'difficulty': 'hard'}, 'laser_maze')

    @on_event(filter={'widget_id': 'emergency_exit_unlock_to_outside'})
    def button_emergency_exit_unlock_to_outside(self):
        self.publish_prefix({'category': 'unlock', 'magnet_id': 'to_outside'}, 'emergency_exit')

    @on_event(filter={'widget_id': 'emergency_exit_unlock_stock_to_machine'})
    def button_emergency_exit_unlock_stock_to_machine(self):
        self.publish_prefix({'category': 'play', 'sound_id': 'server_door_open'}, 'sound_player')
        self.publish_prefix({'category': 'unlock', 'magnet_id': 'stock_to_machine'}, 'emergency_exit')

    @on_event(filter={'widget_id': 'emergency_exit_unlock'})
    def button_emergency_exit_unlock(self):
        self.publish_prefix({'category': 'unlock'}, 'emergency_exit')

    @on_event(filter={'widget_id': 'emergency_exit_lock'})
    def button_emergency_exit_lock(self):
        self.publish_prefix({'category': 'lock'}, 'emergency_exit')

    @on_event(filter={'widget_id': 'stock_lights_high'})
    def button_stock_lights_high(self):
        self.publish_prefix({'category': 'high'}, 'stock_lights')

    @on_event(filter={'widget_id': 'stock_lights_low'})
    def button_stock_lights_low(self):
        self.publish_prefix({'category': 'low'}, 'stock_lights')

    @on_event(filter={'widget_id': 'stock_lights_off'})
    def button_stock_lights_off(self):
        self.publish_prefix({'category': 'off'}, 'stock_lights')

    @on_event(filter={'widget_id': 'sokoban_control_left'})
    def button_sokoban_control_left(self):
        self.publish_prefix({'category': 'control', 'name': 'left', 'pressed': True}, 'inventory')

    @on_event(filter={'widget_id': 'sokoban_control_down'})
    def button_sokoban_control_down(self):
        self.publish_prefix({'category': 'control', 'name': 'down', 'pressed': True}, 'inventory')

    @on_event(filter={'widget_id': 'sokoban_control_right'})
    def button_sokoban_control_right(self):
        self.publish_prefix({'category': 'control', 'name': 'right', 'pressed': True}, 'inventory')

    @on_event(filter={'widget_id': 'sokoban_control_up'})
    def button_sokoban_control_up(self):
        self.publish_prefix({'category': 'control', 'name': 'up', 'pressed': True}, 'inventory')

    @on_event(filter={'widget_id': 'sokoban_control_reset'})
    def button_sokoban_control_reset(self):
        self.publish_prefix({'category': 'control', 'name': 'reset', 'pressed': True}, 'inventory')

    @on_event(filter={'widget_id': 'fog_machine_turn_on'})
    def button_fog_machine_turn_on(self):
        self.publish_prefix({'category': 'on'}, 'fog_machine')

    @on_event(filter={'widget_id': 'fog_machine_turn_off'})
    def button_fog_machine_turn_off(self):
        self.publish_prefix({'category': 'off'}, 'fog_machine')

    @on_event(filter={'widget_id': 'fog_machine_send_fog'})
    def button_fog_machine_send_fog(self):
        self.publish_prefix({'category': 'send_fog'}, 'fog_machine')

    @on_event(filter={'widget_id': 'fog_machine_continuous_fog'})
    def button_fog_machine_continuous_fog(self):
        self.publish_prefix({'category': 'send_fog_forever'}, 'fog_machine')

    @on_event(filter={'widget_id': 'fog_machine_stop_fog'})
    def button_fog_machine_stop_fog(self):
        self.publish_prefix({'category': 'stop_sending_fog_forever'}, 'fog_machine')

    @on_event(filter={'widget_id': 'control_force_manual_mode'})
    def button_control_force_manual_mode(self):
        self.publish_prefix({'category': 'force_manual_mode'}, 'control_panel')

    @on_event(filter={'widget_id': 'synchronizer_restaurant_in_manual_mode'})
    def button_synchronizer_restaurant_in_manual_mode(self):
        self.publish_prefix({'category': 'restaurant_in_manual_mode'}, 'synchronizer')

    @on_event(filter={'widget_id': 'control_menu_set_status_repaired_0'})
    def button_control_menu_set_status_repaired_0(self):
        self.publish_prefix({'category': 'set_menu_service_status', 'repaired': False}, 'control_panel')

    @on_event(filter={'widget_id': 'control_menu_set_status_repaired_1'})
    def button_control_menu_set_status_repaired_1(self):
        self.publish_prefix({'category': 'set_menu_service_status', 'repaired': True}, 'control_panel')

    @on_event(filter={'widget_id': 'control_lights_set_status_repaired_0'})
    def button_control_lights_set_status_repaired_0(self):
        self.publish_prefix({'category': 'set_lights_service_status', 'repaired': False}, 'control_panel')

    @on_event(filter={'widget_id': 'control_lights_set_status_repaired_1'})
    def button_control_lights_set_status_repaired_1(self):
        self.publish_prefix({'category': 'set_lights_service_status', 'repaired': True}, 'control_panel')

    @on_event(filter={'widget_id': 'control_set_status_inactive'})
    def button_control_set_status_inactive(self):
        self.publish_prefix({'category': 'set_status', 'status': 'inactive'}, 'control_panel')

    @on_event(filter={'widget_id': 'control_set_status_playing'})
    def button_control_set_status_playing(self):
        self.publish_prefix({'category': 'set_status', 'status': 'playing'}, 'control_panel')

    @on_event(filter={'widget_id': 'server_room_lock_reset'})
    def button_server_room_lock_reset(self):
        self.publish_prefix({'category': 'reset'}, 'digital_lock')

    @on_event(filter={'widget_id': 'server_room_lock_enable'})
    def button_server_room_lock_enable(self):
        self.publish_prefix({'category': 'enable'}, 'digital_lock')

    @on_event(filter={'widget_id': 'music_player'})
    def buttons_music_player(self, action: str, track_id: str):
        self.publish_prefix({'category': action, 'track_id': track_id}, 'music_player')

    @on_event(filter={'widget_id': 'music_player_set_volume'})
    def buttons_music_player_set_volume(self, track_id: str, volume: int):
        self.publish_prefix({'category': 'set_volume', 'track_id': track_id, 'volume': volume, 'duration': 10}, 'music_player')

    @on_event(filter={'widget_id': 'music_player_set_master_volume'})
    def buttons_music_player_set_master_volume(self, volume: int):
        self.publish_prefix({'category': 'set_volume', 'volume': volume, 'duration': 10}, 'music_player')

    @on_event(filter={'widget_id': 'set_inventory_difficulty_easy'})
    def button_set_inventory_difficulty_easy(self):
        self.publish_prefix({'category': 'set_difficulty', 'difficulty': 'easy'}, 'inventory')

    @on_event(filter={'widget_id': 'set_inventory_difficulty_normal'})
    def button_set_inventory_difficulty_normal(self):
        self.publish_prefix({'category': 'set_difficulty', 'difficulty': 'normal'}, 'inventory')

    @on_event(filter={'widget_id': 'set_inventory_difficulty_hard'})
    def button_set_inventory_difficulty_hard(self):
        self.publish_prefix({'category': 'set_difficulty', 'difficulty': 'hard'}, 'inventory')

    @on_event(filter={'widget_id': 'reset_inventory'})
    def button_reset_inventory(self):
        self.publish_prefix({'category': 'reset'}, 'inventory')

    @on_event(filter={'widget_id': 'display_inventory_danger_window'})
    def button_inventory_display_danger_window(self):
        self.publish_prefix({'category': 'display_danger_window'}, 'inventory')

    @on_event(filter={'widget_id': 'inventory_black_screen'})
    def buttons_inventory_black_screen(self, display: bool):
        self.publish_prefix({'category': 'display_black_screen', 'display': display}, 'inventory')

    @on_event(filter={'widget_id': 'reset_orders'})
    def button_reset_orders(self):
        self.publish_prefix({'category': 'reset'}, 'orders')

    @on_event(filter={'widget_id': 'stop_orders_overlay_video'})
    def button_stop_orders_overlay_video(self):
        self.publish_prefix({'category': 'stop_overlay_video'}, 'orders')

    @on_event(filter={'widget_id': 'display_orders_danger_window'})
    def button_display_orders_danger_window(self):
        self.publish_prefix({'category': 'display_danger_window'}, 'orders')

    @on_event(filter={'widget_id': 'set_ventilation_panel_difficulty_easy'})
    def button_set_ventilation_panel_difficulty_easy(self):
        self.publish_prefix({'category': 'set_difficulty', 'difficulty': 'easy'}, 'ventilation_panel')

    @on_event(filter={'widget_id': 'set_ventilation_panel_difficulty_normal'})
    def button_set_ventilation_panel_difficulty_normal(self):
        self.publish_prefix({'category': 'set_difficulty', 'difficulty': 'normal'}, 'ventilation_panel')

    @on_event(filter={'widget_id': 'set_ventilation_panel_difficulty_hard'})
    def button_set_ventilation_panel_difficulty_hard(self):
        self.publish_prefix({'category': 'set_difficulty', 'difficulty': 'hard'}, 'ventilation_panel')

    @on_event(filter={'widget_id': 'set_ventilation_panel_status_inactive'})
    def button_set_ventilation_panel_status_inactive(self):
        self.publish_prefix({'category': 'set_status', 'status': 'inactive'}, 'ventilation_panel')

    @on_event(filter={'widget_id': 'set_ventilation_panel_status_playing'})
    def button_set_ventilation_panel_status_playing(self):
        self.publish_prefix({'category': 'set_status', 'status': 'playing'}, 'ventilation_panel')

    @on_event(filter={'widget_id': 'set_ventilation_panel_status_success'})
    def button_set_ventilation_panel_status_success(self):
        self.publish_prefix({'category': 'set_status', 'status': 'success'}, 'ventilation_panel')

    @on_event(filter={'widget_id': 'control_table_up'})
    def button_control_table_up(self):
        self.publish_prefix({'category': 'table_up'}, 'control_panel')

    @on_event(filter={'widget_id': 'control_table_down'})
    def button_control_table_down(self):
        self.publish_prefix({'category': 'table_down'}, 'control_panel')

    @on_event(filter={'widget_id': 'control_table_stop'})
    def button_control_table_stop(self):
        self.publish_prefix({'category': 'table_stop'}, 'control_panel')

    @on_event(filter={'widget_id': 'load_cells_calibrate'})
    def button_load_cells_calibrate(self):
        self.publish_prefix({'category': 'calibrate'}, 'load_cells')

    @on_event(filter={'widget_id': 'refectory_lights'})
    def buttons_refectory_lights(self, color: str, on: bool):
        self.publish_prefix({'category': 'on' if on else 'off', 'color': color}, 'refectory_lights')

    @on_event(filter={'widget_id': 'refectory_lights_glitch'})
    def buttons_refectory_lights_glitch(self, color: str):
        self.publish_prefix({'category': 'glitch', 'color': color}, 'refectory_lights')

    @on_event(filter={'widget_id': 'refectory_lights_stop_glitch'})
    def buttons_refectory_lights_stop_glitch(self, color: str):
        self.publish_prefix({'category': 'stop_glitch', 'color': color}, 'refectory_lights')

    @on_event(filter={'widget_id': 'waffle_factory_light'})
    def buttons_waffle_factory_light(self, led_id: str, on: bool):
        if on:
            self.publish_prefix({'category': 'light_on', 'led_id': led_id}, 'waffle_factory')
        else:
            self.publish_prefix({'category': 'light_off', 'led_id': led_id}, 'waffle_factory')

    @on_event(filter={'widget_id': 'waffle_factory_basket_led'})
    def buttons_waffle_factory_led(self, action):
        if action == 'on':
            self.publish_prefix({'category': 'basket_led_on'}, 'waffle_factory')
        elif action == 'off':
            self.publish_prefix({'category': 'basket_led_off'}, 'waffle_factory')
        elif action == 'blink':
            self.publish_prefix({'category': 'basket_led_blink'}, 'waffle_factory')

    @on_event(filter={'widget_id': 'waffle_trapdoor_open'})
    def buttons_waffle_trapdoor_open(self):
        self.publish_prefix({'category': 'low'}, 'waffle_trapdoor')

    @on_event(filter={'widget_id': 'waffle_trapdoor_close'})
    def buttons_waffle_trapdoor_close(self):
        self.publish_prefix({'category': 'high'}, 'waffle_trapdoor')

    @on_event(filter={'widget_id': 'printer_instructions'})
    def widget_printer_instructions(self, value: str):
        instructions = value.split('\n')
        self.publish_prefix({'category': 'printer_instructions', 'instructions': instructions}, 'waffle_factory')

    @on_event(filter={'widget_id': 'waffle_factory_print_pattern'})
    def buttons_waffle_print_pattern(self, pattern: str):
        self.publish_prefix({'category': 'print_pattern', 'pattern': pattern}, 'waffle_factory')

    @on_event(filter={'widget_id': 'waffle_factory_printer'})
    def buttons_waffle_printer(self, action: str):
        if action == 'halt':
            self.publish_prefix({'category': 'printer_halt'}, 'waffle_factory')
        elif action == 'resume':
            self.publish_prefix({'category': 'printer_resume'}, 'waffle_factory')
        elif action == 'stop':
            self.publish_prefix({'category': 'printer_stop'}, 'waffle_factory')

    @on_event(filter={'widget_id': 'printer_homing'})
    def button_printer_homing(self):
        self.publish_prefix({'category': 'printer_homing'}, 'waffle_factory')

    @on_event(filter={'widget_id': 'chopsticks_success'})
    def buttons_chopsticks_success(self):
        self.publish_prefix({'category': 'force_success'}, 'chopsticks')

    @on_event(filter={'widget_id': 'chopsticks_reset'})
    def buttons_chopsticks_reset(self):
        self.publish_prefix({'category': 'reset'}, 'chopsticks')

    @on_event(filter={'widget_id': 'set_chopsticks_difficulty'})
    def buttons_chopsticks_set_difficulty(self, difficulty: str):
        self.publish_prefix({'category': 'set_difficulty', 'difficulty': difficulty}, 'chopsticks')

    @on_event(filter={'widget_id': 'chopsticks_emulate_plug'})
    def buttons_chopsticks_emulate_plug(self, letter_index: int):
        self.publish_prefix({'category': 'emulate_chopstick_plug', 'letter_index': letter_index}, 'chopsticks')

    @on_event(filter={'widget_id': 'chopsticks_emulate_unplug'})
    def buttons_chopsticks_emulate_unplug(self, letter_index: int):
        self.publish_prefix({'category': 'emulate_chopstick_unplug', 'letter_index': letter_index}, 'chopsticks')

    @on_event(filter={'widget_id': 'oven_turn_on'})
    def button_oven_turn_on(self):
        self.publish_prefix({'category': 'oven_turn_on'}, 'waffle_factory')

    @on_event(filter={'widget_id': 'oven_turn_off'})
    def button_oven_turn_off(self):
        self.publish_prefix({'category': 'oven_turn_off'}, 'waffle_factory')

    @on_event(filter={'widget_id': 'street_lights_on'})
    def button_street_lights_on(self):
        self.publish_prefix({'category': 'on', 'color': 'all'}, 'street_lights')

    @on_event(filter={'widget_id': 'street_lights_off'})
    def button_street_lights_off(self):
        self.publish_prefix({'category': 'off', 'color': 'all'}, 'street_lights')

    @on_event(filter={'widget_id': 'street_lights_glitch'})
    def button_street_lights_glitch(self):
        self.publish_prefix({'category': 'glitch', 'color': 'blue'}, 'street_lights')
        self.publish_prefix({'category': 'glitch', 'color': 'orange'}, 'street_lights')

    @on_event(filter={'widget_id': 'street_lights_stop_glitch'})
    def button_street_lights_stop_glitch(self):
        self.publish_prefix({'category': 'stop_glitch', 'color': 'blue'}, 'street_lights')
        self.publish_prefix({'category': 'stop_glitch', 'color': 'orange'}, 'street_lights')

    @on_event(filter={'widget_id': 'waffle_factory_play_animation'})
    def button_waffle_factory_play_animation(self, animation: str):
        self.publish_prefix({'category': 'play_animation', 'animation': animation}, 'waffle_factory')

    @on_event(filter={'widget_id': 'waffle_factory_pause_animation'})
    def button_waffle_factory_pause_animation(self):
        self.publish_prefix({'category': 'pause_animation'}, 'waffle_factory')

    @on_event(filter={'widget_id': 'holomenu_set_part'})
    def buttons_holomenu_set_part(self, part: str, **kwargs):
        if part == 'slide':
            self.holomenu_slide = kwargs['slide']
        elif part == 'x':
            self.holomenu_x = kwargs['x']
        elif part == 'y':
            self.holomenu_y = kwargs['y']
        elif part == 'error':
            self.holomenu_error = True

        if self.holomenu_slide is not None:
            if self.holomenu_error is not None:
                self.publish_prefix({'category': 'play', 'sound_id': 'hologram_set_slide'}, 'sound_player')

                self.publish_prefix(
                    {
                        'category': 'set_slide',
                        'slide_index': self.holomenu_slide,
                        'chapter_id': 'error',
                    },
                    'holographic_menu'
                )
                self.holomenu_slide = None
                self.holomenu_x = None
                self.holomenu_y = None
                self.holomenu_error = None

            if self.holomenu_x is not None and self.holomenu_y is not None:
                self.publish_prefix({'category': 'play', 'sound_id': 'hologram_set_slide'}, 'sound_player')

                chapter_id = self.holomenu_slides_mapping[self.holomenu_x][self.holomenu_y]
                self.publish_prefix(
                    {
                        'category': 'set_slide',
                        'slide_index': self.holomenu_slide,
                        'chapter_id': chapter_id,
                    },
                    'holographic_menu'
                )
                self.holomenu_slide = None
                self.holomenu_x = None
                self.holomenu_y = None
                self.holomenu_error = None

    @on_event(filter={'widget_id': 'niryo_magnetize'})
    def button_niryo_magnetize(self, value: bool):
        self.publish_prefix({'category': 'electromagnet', 'magnetize': value}, 'niryo')

    @on_event(filter={'widget_id': 'payment_authenticate'})
    def button_payment_authenticate(self):
        # 't': 0, for tag=0 is a value that is not supposed to be possible if real rings are used. It acts as a new
        # ring being authenticated, triggering a new credit value to be provided on the order interface.
        self.publish_prefix({'c': 'a', 't': 0}, 'payment_module')

    @on_event(filter={'widget_id': 'payment_cancel_authentication'})
    def button_payment_cancel_authentication(self):
        self.publish_prefix({'c': 'c'}, 'payment_module')

    @on_event(filter={'widget_id': 'payment_status'})
    def buttons_payment_status(self, status: str):
        self.publish_prefix({'category': 'set_status', 'status': status}, 'payment_module')

    @on_event(filter={'widget_id': 'synchronizer_display_price'})
    def buttons_synchronizer_display_price(self, display: bool):
        self.publish_prefix({'category': 'display_price', 'display': display}, 'synchronizer')

    @on_event(filter={'widget_id': 'auto_validate_dishes'})
    def buttons_auto_validate_dishes(self, value: bool):
        self.publish_prefix({'category': 'set_auto_validate_dishes', 'value': value}, 'synchronizer')

    @on_event(filter={'widget_id': 'vents_locker'})
    def buttons_vents_locker(self, lock: bool):
        self.publish_prefix({'category': 'lock' if lock else 'unlock'}, 'vents_locker')

    @on_event(filter={'widget_id': 'alarm_relays'})
    def buttons_alarm_relays(self, activated: bool):
        self.publish_prefix({'category': 'alarm', 'activated': activated}, 'relays')

    @on_event(filter={'category': 'localize'})
    def localize(self, value: str):
        self.publish_prefix({'category': 'set_locale', 'locale': value}, 'broadcast')

    @on_event(filter={'category': 'process_log'})
    def process_log(self, with_sound: bool):
        if with_sound:
            self.publish_prefix({'category': 'play', 'sound_id': 'typing'}, 'sound_player')

    @on_event(filter={'widget_type': 'log_prompt'})
    def log_prompt(self, message: str, level: str, use_locale: bool, widget_id: str, with_sound: bool = True):
        if widget_id == 'light_log':
            category = 'light_log'
            channel = 'synchronizer'
        elif widget_id == 'menu_log':
            category = 'menu_log'
            channel = 'synchronizer'
        elif widget_id == 'inventory_log':
            category = 'log'
            channel = 'inventory'
        elif widget_id == 'root_server_log':
            category = 'log'
            channel = 'root_server'
        else:
            return

        self.publish_prefix(
            {
                'category': category,
                'message': message,
                'level': level,
                'use_locale': use_locale,
                'with_sound': with_sound,
            },
            channel
        )

    @on_event(filter={'widget_type': 'instruction_prompt'})
    def instruction_prompt(self, message: str, use_locale: bool):
        self.publish_prefix(
            {
                'category': 'set_documentation_current_instruction',
                'message': message,
                'use_locale': use_locale,
            },
            'orders'
        )
        if message:
            self.publish_prefix({'category': 'play', 'sound_id': 'typing'}, 'sound_player')

    @on_event(filter={'category': 'get_session_time'})
    def get_session_time(self):
        # Could be more personalized but it's ok for now
        self.tic_tac_callback(self.session_time)

    @on_event(filter={'widget_type': 'lasers'})
    def toggle_permanent_laser_activation(self, action: str, laser_maze_channel: str, laser_index: int):
        self.publish_prefix({'category': action, 'index': laser_index}, laser_maze_channel)

    @on_event(filter={'widget_type': 'waffle_factory', 'action': 'motor_forward'})
    def waffle_factory_motor_forward(
            self, motor_channel: str, motor_id: str,
            n_pulses: int, step_delay: int, liminary_n_pulses: int, liminary_step_delay: int,
    ):
        self.publish_prefix({
            'category': 'motor_forward',
            'motor_id': motor_id,
            'n_pulses': n_pulses,
            'step_delay': step_delay,
            'liminary_n_pulses': liminary_n_pulses,
            'liminary_step_delay': liminary_step_delay,
        }, motor_channel)

    @on_event(filter={'widget_type': 'waffle_factory', 'action': 'motor_homing'})
    def waffle_factory_motor_homing(
            self, motor_channel: str, motor_id: str,
            n_pulses: int, step_delay: int, liminary_n_pulses: int, liminary_step_delay: int,
    ):
        self.publish_prefix({
            'category': 'motor_homing',
            'motor_id': motor_id,
            'n_pulses': n_pulses,
            'step_delay': step_delay,
            'liminary_n_pulses': liminary_n_pulses,
            'liminary_step_delay': liminary_step_delay,
        }, motor_channel)

    @on_event(filter={'widget_type': 'waffle_factory', 'action': 'motor_backward'})
    def waffle_factory_motor_backward(
            self, motor_channel: str, motor_id: str,
            n_pulses: int, step_delay: int, liminary_n_pulses: int, liminary_step_delay: int,
    ):
        self.publish_prefix({
            'category': 'motor_backward',
            'motor_id': motor_id,
            'n_pulses': n_pulses,
            'step_delay': step_delay,
            'liminary_n_pulses': liminary_n_pulses,
            'liminary_step_delay': liminary_step_delay,
        }, motor_channel)

    @on_event(filter={'widget_type': 'waffle_factory', 'action': 'motor_stop'})
    def waffle_factory_motor_stop(self, motor_channel: str, motor_id: str):
        self.publish_prefix({
            'category': 'motor_stop',
            'motor_id': motor_id,
        }, motor_channel)

    @on_event(filter={'widget_type': 'waffle_factory', 'action': 'dxl_torque_on'})
    def waffle_factory_dxl_torque_on(self, dxl_id: str):
        self.publish_prefix({
            'category': 'dxl_torque_on',
            'dxl_id': dxl_id,
        }, 'niryo')

    @on_event(filter={'widget_type': 'waffle_factory', 'action': 'dxl_torque_off'})
    def waffle_factory_dxl_torque_off(self, dxl_id: str):
        self.publish_prefix({
            'category': 'dxl_torque_off',
            'dxl_id': dxl_id,
        }, 'niryo')

    @on_event(filter={'widget_type': 'waffle_factory', 'action': 'dxl_reboot'})
    def waffle_factory_dxl_reboot(self, dxl_id: str):
        self.publish_prefix({
            'category': 'dxl_reboot',
            'dxl_id': dxl_id,
        }, 'niryo')

    @on_event(filter={'widget_type': 'waffle_factory', 'action': 'dxl_get_position'})
    def waffle_factory_dxl_get_position(self, dxl_id: str):
        self.publish_prefix({
            'category': 'dxl_get_position',
            'dxl_id': dxl_id,
        }, 'niryo')

    @on_event(filter={'widget_type': 'waffle_factory', 'action': 'dxl_move'})
    def waffle_factory_dxl_move(self, dxl_id: str, position: int):
        self.publish_prefix({
            'category': 'dxl_move',
            'dxl_id': dxl_id,
            'position': position,
        }, 'niryo')

    @on_event(filter={'widget_id': 'root_server_reset'})
    def root_server_reset(self):
        self.publish_prefix({'category': 'reset'}, 'root_server')

    @on_event(filter={'widget_id': 'root_server_show_ui'})
    def root_server_show_ui(self):
        self.publish_prefix({'category': 'show_ui'}, 'root_server')
        self.register_delayed_task(
            3, self.publish_prefix, {'category': 'display_password_window'}, 'root_server')

    @on_event(filter={'widget_id': 'root_server_success'})
    def root_server_success(self):
        self.publish_prefix({'category': 'force_success'}, 'root_server')

    @on_event(filter={'widget_id': 'root_server_display_danger_window'})
    def root_server_display_danger_window(self):
        self.publish_prefix({'category': 'display_danger_window'}, 'root_server')

    @on_event(filter={'widget_id': 'root_server_play_animation'})
    def root_server_play_animation(self, animation_id: str):
        self.publish_prefix({'category': 'play_animation', 'animation': animation_id}, 'root_server')

    @on_event(filter={'widget_type': 'session_data', 'action': 'set'})
    def widget_session_data_set_data(self, key: str, value):
        self.set_session_data(key, value)

    @on_event(filter={'widget_id': 'niryo_animation'})
    def niryo_animation(self, animation: str):
        self.publish_prefix({'category': 'play_animation', 'animation': animation}, 'niryo')

    @on_event(filter={'widget_id': 'niryo_pause_animation'})
    def niryo_pause_animation(self):
        self.publish_prefix({'category': 'pause_animation'}, 'niryo')

    @on_event(filter={'widget_type': 'synchronizer_lights', 'action': 'set_disabled'})
    def synchronizer_lights_set_disabled(self, color: str, disabled: bool):
        self.publish_prefix({'category': 'set_color_disabled', 'color': color, 'is_disabled': disabled}, 'synchronizer')

    @on_event(filter={'widget_id': 'play_sound'})
    def buttons_play_sound(self, sound_id: str):
        self.publish_prefix({'category': 'play', 'sound_id': sound_id}, 'sound_player')

    @on_event(filter={'widget_id': 'set_cylinders_difficulty'})
    def buttons_cylinders_set_difficulty(self, difficulty: str):
        self.publish_prefix({'category': 'set_difficulty', 'difficulty': difficulty}, 'cylinders')

    @on_event(filter={'widget_id': 'reset_cylinders'})
    def button_cylinders_reset(self):
        self.publish_prefix({'category': 'reset'}, 'cylinders')

    @on_event(filter={'widget_id': 'force_cylinders_success'})
    def button_force_cylinders_success(self):
        self.publish_prefix({'category': 'force_success'}, 'cylinders')

    @on_event(filter={'widget_id': 'check_cylinders_availability'})
    def buttons_cylinders_check_availability(self, id: str):
        self.publish_prefix({'category': 'check_availability', 'id': id}, 'cylinders')


class ScenarioD1(Scenario):
    pass


class ScenarioD2(Scenario):
    pass

