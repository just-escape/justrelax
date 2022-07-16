from enum import Enum
import json
import time
import uuid
from datetime import datetime, timezone

from coolname import generate_slug
from twisted.internet import reactor

from justrelax.core.logging_utils import logger
from justrelax.core.node import MagicNode, on_event


class TimerState(Enum):
    NOT_STARTED = 'NOT_STARTED'
    TICKING = 'TICKING'
    PAUSED = 'PAUSED'


class Timer:
    def __init__(self, delay, callback=None, *args, **kwargs):
        self.delay = delay
        self.callback = callback
        self.callback_args = args
        self.callback_kwargs = kwargs

        self.state = TimerState.NOT_STARTED
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
        self.task = reactor.callLater(self.delay, self.execute_callback)

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
            self.task = reactor.callLater(self.last_computed_delay, self.execute_callback)

    def cancel(self):
        if self.task and self.task.active():
            self.task.cancel()
            self.task = None

    def execute_callback(self):
        self.task = None
        self.callback(*self.callback_args, **self.callback_kwargs)


class TickingTimer:
    def __init__(self):
        self.elapsed_time = 0.
        self.tic_tac_period = 1  # seconds

        self.state = TimerState.NOT_STARTED
        self.task = None
        self.last_computed_delay = 0.
        self.last_schedule_timestamp = 0.

    def start(self):
        if self.state == TimerState.NOT_STARTED:
            self.last_schedule_timestamp = time.monotonic()
            self.schedule_next_tic_tac()
            self.state = TimerState.TICKING

    def schedule_next_tic_tac(self):
        now = time.monotonic()
        delta_since_last_schedule = now - self.last_schedule_timestamp
        self.last_schedule_timestamp = now

        self.elapsed_time += delta_since_last_schedule
        delay_before_next_call = self.tic_tac_period - self.elapsed_time % self.tic_tac_period
        self.task = reactor.callLater(delay_before_next_call, self.tic_tac)

    def tic_tac(self):
        self.schedule_next_tic_tac()
        self.on_tic_tac()

    def on_tic_tac(self):
        pass

    def pause(self):
        if self.state == TimerState.TICKING:
            delta_since_last_schedule = time.monotonic() - self.last_schedule_timestamp
            self.last_computed_delay = self.tic_tac_period - delta_since_last_schedule
            self.elapsed_time += delta_since_last_schedule
            if self.task and self.task.active():
                self.task.cancel()
            self.state = TimerState.PAUSED
            self.on_pause()
        elif self.state == TimerState.NOT_STARTED:
            self.state = TimerState.PAUSED

    def on_pause(self):
        pass

    def resume(self):
        if self.state == TimerState.PAUSED:
            now = time.monotonic()
            self.last_schedule_timestamp = now
            self.task = reactor.callLater(self.last_computed_delay, self.tic_tac)
            self.state = TimerState.TICKING
            self.on_resume()

    def on_resume(self):
        pass

    def cancel(self):
        if self.state == TimerState.PAUSED:
            self.elapsed_time = 0.
            self.last_computed_delay = 0.
            self.last_schedule_timestamp = 0.
            self.state = TimerState.NOT_STARTED
            self.on_cancel()

    def on_cancel(self):
        pass


class SessionTimer(TickingTimer):
    def __init__(self, tic_tac_callback=None):
        TickingTimer.__init__(self)
        self.tic_tac_callback = tic_tac_callback

    def on_tic_tac(self):
        if self.tic_tac_callback:
            self.tic_tac_callback(self)


class TrackedTimer(TickingTimer):
    def __init__(self, delay, name, scenario, callback=None, *callback_args, **callback_kwargs):
        TickingTimer.__init__(self)
        self.delay = delay
        self.name = name
        self.scenario = scenario
        self.callback = callback
        self.callback_args = callback_args
        self.callback_kwargs = callback_kwargs

        self.remaining_time = round(self.delay)
        self.is_manually_paused = False
        self.executed = None

        self.scenario.register_tracked_timer(self)

    def on_start(self):
        self.executed = None

    def manual_pause(self):
        self.is_manually_paused = True
        logger.info(f"man pause {self.name}")
        self.pause()
        self.on_pause()  # Just to be sure to update the manual_pause property

    def on_pause(self):
        self.scenario.update_tracked_timer(self)

    def manual_resume(self):
        self.is_manually_paused = False
        self.resume()

    def on_cancel(self):
        self.remaining_time = round(self.delay)
        self.is_manually_paused = False
        self.scenario.update_tracked_timer(self)

    def on_tic_tac(self):
        self.remaining_time = round(self.delay - self.elapsed_time)

        if self.remaining_time <= 0:
            self.execute_callback()
        else:
            self.scenario.update_tracked_timer(self)

    def execute_callback(self):
        self.remaining_time = 0
        if self.task and self.task.active():
            self.task.cancel()
        if self.callback:
            self.callback(*self.callback_args, **self.callback_kwargs)
        self.executed = self.scenario.session_time or 0

        self.scenario.update_tracked_timer(self)


class Scenario(MagicNode):
    DIFFICULTIES = {'easy', 'normal', 'hard'}

    MS_PEPPER_INTRO_DURATION = 35
    NIRYO_BUGGED_ANIMATION_DURATION = 23 - 10  # - 10 in order to trigger Ms Pepper's speech earlier

    PERSISTENT_SCENARIO_SETTINGS = [
        'niryo_animation',
        'ms_pepper_intro',
        'epileptic_mode',
        'final_by_refectory',
        'dry_print',
        'order_with_niryo_and_printer',
        'autostart_timers',
    ]

    EXPECTED_MENU = [
        "potjevleesch",
        "salade_flamande",
        "cambraisienne",
        "gaufresque",
    ]

    def __init__(self, *args, **kwargs):
        super(Scenario, self).__init__(*args, **kwargs)

        self.publication_channel_prefix = self.config['publication_channel_prefix']

        self.chopsticks_voice_clue_1_delay = self.config['chopsticks_voice_clue_1_delay']
        self.chopsticks_voice_clue_2_delay = self.config['chopsticks_voice_clue_2_delay']

        self.ventilation_panel_skip_delay = self.config['ventilation_panel_skip_delay']

        self.niryo_animation_duration = self.config['niryo_animation_duration']
        self.niryo_end_conveyor_duration = self.config['niryo_end_conveyor_duration']
        self.oven_cooking_duration = self.config['oven_cooking_duration']
        self.first_waffle_init_conveyor_duration = self.config['first_waffle_init_conveyor_duration']
        self.first_pattern_print_duration = self.config['first_pattern_print_duration']
        self.basket_led_blink_delay = self.config['basket_led_blink_delay']
        self.basket_led_blinking_time = self.config['basket_led_blinking_time']
        self.ms_pepper_says_thanks_delay = self.config['ms_pepper_says_thanks_delay']
        self.second_waffle_init_conveyor_duration = self.config['second_waffle_init_conveyor_duration']

        self.initial_fog_duration = self.config['initial_fog_duration']
        self.boost_fog_delay = self.config['boost_fog_delay']
        self.boost_fog_duration = self.config['boost_fog_duration']

        self.session_timer = SessionTimer(self.tic_tac_callback)
        self.session_time = None
        self.session_data = {}

        self.initial_difficulty = 'normal'

        # Those delayed calls are canceled on a room reset
        self.registered_delayed_tasks = {}

        with open(self.config['persistent_settings'], 'r') as fh:
            self.persistent_settings = json.load(fh)

        self._timers = {}
        self.chopsticks_voice_clue_1 = TrackedTimer(
            self.chopsticks_voice_clue_1_delay, 'chopsticks_voice_clue_1', self, self.play_sound, "pepper_1", True)
        self.chopsticks_voice_clue_2 = TrackedTimer(
            self.chopsticks_voice_clue_2_delay, 'chopsticks_voice_clue_2', self, self.play_sound, "pepper_2", True)
        self.ventilation_panel_skip = TrackedTimer(
            self.ventilation_panel_skip_delay, 'ventilation_panel_skip_timer', self, self.set_ventilation_panel_skip)
        self.boost_fog_timer = TrackedTimer(
            self.boost_fog_delay, 'boost_fog_timer', self, self.boost_fog)

        self.second_waffle_print_timing = 0

        self.modify_fx_task = None

        self.track1_light_animation_1_first_task = None
        self.track1_light_animation_1_second_task = None
        self.track1_light_animation_2_first_task = None
        self.track1_light_animation_2_second_task = None
        self.track1_light_animation_3_first_task = None
        self.track1_light_animation_3_second_task = None
        self.track1_light_animation_4_first_task = None
        self.track1_light_animation_4_second_task = None
        self.track1_light_animation_5_first_task = None
        self.track1_light_animation_5_second_task = None
        self.track1_light_animation_6_first_task = None
        self.track1_light_animation_7_first_task = None

        self.track1_light_animation_1_loop_task = None
        self.track1_light_animation_2_loop_task = None
        self.track1_light_animation_3_loop_task = None
        self.track1_light_animation_4_loop_task = None
        self.track1_light_animation_5_loop_task = None
        self.track1_light_animation_6_loop_task = None
        self.track1_light_animation_7_loop_task = None

        self.light_service_success_animation_task = None
        self.synchronizer_light_service_repaired = False

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

        self.menu_last_log_hint_time = time.monotonic()
        self.wrong_dishes_counter = -3
        self.all_dishes_are_good_but_wrong_price_counter = -1
        self.displaying_ads_loop = False
        self.display_multiple_ads = False

        self.set_session_data('locale', 'fr')
        self.set_session_data('ventilation_panel_skip', False)
        self.set_session_data('sokoban_first_move_time_0', None)
        self.set_session_data('sokoban_first_move_time_1', None)
        self.set_session_data('sokoban_first_move_time_2', None)
        self.set_session_data('sokoban_success_time_0', None)
        self.set_session_data('sokoban_success_time_1', None)
        self.set_session_data('sokoban_success_time_2', None)

    def new_session_id(self):
        session_id = generate_slug(3)
        self.set_session_data('session_id', session_id)

    def ping(self):
        # Not useful to ping something because session data cannot exist if this node is not up
        pass

    def publish_prefix(self, event, channel, log=True):
        event['sid'] = self.session_data.get('session_id', None)
        self.publish(event, "{}{}".format(self.publication_channel_prefix, channel), log=log)

    def register_delayed_task(self, delay, callable, *callable_args, **callable_kwargs):
        task_id = str(uuid.uuid4())

        def unregistered_and_call():
            self.registered_delayed_tasks.pop(task_id)
            callable(*callable_args, **callable_kwargs)

        self.registered_delayed_tasks[task_id] = reactor.callLater(delay, unregistered_and_call)
        return task_id

    def cancel_delayed_task(self, task_id):
        if task_id in self.registered_delayed_tasks:
            task = self.registered_delayed_tasks.pop(task_id)
            task.cancel()

    def tic_tac_callback(self, session_timer):
        elapsed_time = session_timer.elapsed_time
        self.session_time = round(elapsed_time) if elapsed_time else None
        self.publish_prefix({'category': 'set_session_time', 'seconds': self.session_time}, 'street_display')
        self.publish_game_time_to_webmin()

    def register_tracked_timer(self, timer):
        self._timers[timer.name] = timer

    def update_tracked_timer(self, timer):
        timer_data = {
            "remaining_time": timer.remaining_time,
            "manually_paused": timer.is_manually_paused,
            "executed": timer.executed,
            "delay": timer.delay,
            "state": timer.state.value,
        }
        self.set_session_data(timer.name, timer_data)

    def on_first_connection(self):
        for key in self.PERSISTENT_SCENARIO_SETTINGS:
            self._record_session_data(key, self.persistent_settings[key])
        for timer_name, timer in self._timers.items():
            self.update_tracked_timer(timer)

        self.set_session_data('session_id', None)

        self.publish_prefix({'category': 'request_node_session_data'}, 'broadcast')

    @on_event(filter={'from_': 'webmin', 'widget_id': 'start_stop', 'action': 'run'})
    def run_room_from_webmin(self):
        self.run_room()

    @on_event(filter={'from_': 'street_display', 'category': 'play'})
    def run_room_from_street_display(self):
        self.run_room()

    def get_locale_suffix(self):
        return f"_{self.session_data['locale']}"

    @on_event(filter={'widget_id': 'play_ms_pepper_here_you_are'})
    def play_ms_pepper_here_you_are(self):
        self.publish_prefix(
            {
                'category': 'pause',
                'video_id': 'ads_glitch'  # if self.initial_difficulty == 'hard' else 'waffresco_ad_loop',
            },
            'advertiser'
        )
        self.publish_prefix(
            {
                'category': 'play',
                'video_id': f"""ms_pepper_here_you_are_{self.session_data["locale"]}"""
            },
            'advertiser'
        )

        self.register_delayed_task(
            self.MS_PEPPER_INTRO_DURATION, self.publish_prefix,
            {
                'category': 'play',
                'video_id': 'ads_glitch'  # if self.initial_difficulty == 'hard' else 'waffresco_ad_loop',
            },
            'advertiser'
        )

    def run_room(self):
        if self.session_timer.state == TimerState.NOT_STARTED:
            self.start_room()
        elif self.session_timer.state == TimerState.PAUSED:
            self.resume_room()

    def start_room(self):
        self.new_session_id()

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
            if self.persistent_settings['autostart_timers']:
                self.chopsticks_voice_clue_1.start()
                self.chopsticks_voice_clue_2.start()
                self.ventilation_panel_skip.start()

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
        self.publish_prefix({'category': 'set_status', 'status': 'auto_control'}, 'laser_maze')

        self.publish_prefix(
            {
                'category': 'pause',
                'video_id': 'ads_glitch'  # if self.initial_difficulty == 'hard' else 'waffresco_ad_loop',
            },
            'advertiser'
        )

        if self.persistent_settings['ms_pepper_intro']:
            self.publish_prefix(
                {
                    'category': 'play',
                    'video_id': f"""ms_pepper_here_you_are_{self.session_data["locale"]}""",
                },
                'advertiser'
            )

        real_intro_duration = self.MS_PEPPER_INTRO_DURATION if self.persistent_settings['ms_pepper_intro'] else 0
        self.modify_fx_task = self.register_delayed_task(real_intro_duration + 18.285, self.modify_fx)
        self.register_delayed_task(real_intro_duration, after_ms_pepper_here_you_are)
        self.register_delayed_task(real_intro_duration + 3, open_the_door)

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
        self.track1_light_animation_1_first_task = (
            self.register_delayed_task(21.25, self.track1_light_animation_1)
        )
        self.track1_light_animation_1_second_task = (
            self.register_delayed_task(220.107125, self.track1_light_animation_1)
        )
        self.track1_light_animation_2_first_task = (
            self.register_delayed_task(29.75, self.track1_light_animation_2)
        )
        self.track1_light_animation_2_second_task = (
            self.register_delayed_task(228.607125, self.track1_light_animation_2)
        )
        self.track1_light_animation_3_first_task = (
            self.register_delayed_task(51.75, self.track1_light_animation_3)
        )
        self.track1_light_animation_3_second_task = (
            self.register_delayed_task(151.178563, self.track1_light_animation_3)
        )
        self.track1_light_animation_4_first_task = (
            self.register_delayed_task(82.25, self.track1_light_animation_4)
        )
        self.track1_light_animation_4_second_task = (
            self.register_delayed_task(281.107125, self.track1_light_animation_4)
        )
        self.track1_light_animation_5_first_task = (
            self.register_delayed_task(90, self.track1_light_animation_5)
        )
        self.track1_light_animation_5_second_task = (
            self.register_delayed_task(288.857125, self.track1_light_animation_5)
        )
        self.track1_light_animation_6_first_task = (
            self.register_delayed_task(161.5, self.track1_light_animation_6)
        )
        self.track1_light_animation_7_first_task = (
            self.register_delayed_task(182.5, self.track1_light_animation_7)
        )

    @on_event(filter={'category': 'track_loop', 'track_id': 'track1'})
    def track_1_has_looped(self):
        self.track1_light_animation_1_loop_task = (
            self.register_delayed_task(120.678563, self.track1_light_animation_1)
        )
        self.track1_light_animation_2_loop_task = (
            self.register_delayed_task(129.178563, self.track1_light_animation_2)
        )
        self.track1_light_animation_3_loop_task = (
            self.register_delayed_task(151.178563, self.track1_light_animation_3)
        )
        self.track1_light_animation_4_loop_task = (
            self.register_delayed_task(181.678563, self.track1_light_animation_4)
        )
        self.track1_light_animation_5_loop_task = (
            self.register_delayed_task(189.428563, self.track1_light_animation_5)
        )
        self.track1_light_animation_6_loop_task = (
            self.register_delayed_task(62.071438, self.track1_light_animation_6)
        )
        self.track1_light_animation_7_loop_task = (
            self.register_delayed_task(83.071438, self.track1_light_animation_7)
        )

    @on_event(filter={'category': 'track_stop', 'track_id': 'track1'})
    def track_1_has_stopped(self):
        self.cancel_delayed_task(self.track1_light_animation_1_first_task)
        self.cancel_delayed_task(self.track1_light_animation_1_second_task)
        self.cancel_delayed_task(self.track1_light_animation_2_first_task)
        self.cancel_delayed_task(self.track1_light_animation_2_second_task)
        self.cancel_delayed_task(self.track1_light_animation_3_first_task)
        self.cancel_delayed_task(self.track1_light_animation_3_second_task)
        self.cancel_delayed_task(self.track1_light_animation_4_first_task)
        self.cancel_delayed_task(self.track1_light_animation_4_second_task)
        self.cancel_delayed_task(self.track1_light_animation_5_first_task)
        self.cancel_delayed_task(self.track1_light_animation_5_second_task)
        self.cancel_delayed_task(self.track1_light_animation_6_first_task)
        self.cancel_delayed_task(self.track1_light_animation_7_first_task)

        self.cancel_delayed_task(self.track1_light_animation_1_loop_task)
        self.cancel_delayed_task(self.track1_light_animation_2_loop_task)
        self.cancel_delayed_task(self.track1_light_animation_3_loop_task)
        self.cancel_delayed_task(self.track1_light_animation_4_loop_task)
        self.cancel_delayed_task(self.track1_light_animation_5_loop_task)
        self.cancel_delayed_task(self.track1_light_animation_6_loop_task)
        self.cancel_delayed_task(self.track1_light_animation_7_loop_task)

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
        for timer_name, timer in self._timers.items():
            timer.resume()

    @on_event(filter={'from_': 'webmin', 'widget_id': 'start_stop', 'action': 'halt'})
    def halt_room(self):
        if self.session_timer.state in [TimerState.NOT_STARTED, TimerState.TICKING]:
            for timer_name, timer in self._timers.items():
                timer.pause()
            self.session_timer.pause()

    @on_event(filter={'from_': 'webmin', 'widget_id': 'start_stop', 'action': 'reset'})
    def reset_room(self):
        if self.session_timer.state != TimerState.PAUSED:
            return

        for timer_name, timer in self._timers.items():
            timer.cancel()
        self.session_timer.cancel()
        self.session_time = None

        registered_delayed_task_ids = list(self.registered_delayed_tasks)
        for registered_delayed_task_id in registered_delayed_task_ids:
            task = self.registered_delayed_tasks.pop(registered_delayed_task_id)
            task.cancel()

        self.second_waffle_print_timing = 0

        self.publish_game_time_to_webmin()

        # Note: the table is not automatically reset, as well as the Niryo and the printer
        self.publish_prefix({'category': 'reset'}, 'broadcast')

        self.set_session_data('session_id', None)

        self.synchronizer_light_service_repaired = False
        self.holomenu_slide = None
        self.holomenu_x = None
        self.holomenu_y = None
        self.holomenu_error = None

        self.wrong_dishes_counter = -3
        self.all_dishes_are_good_but_wrong_price_counter = -1
        self.displaying_ads_loop = False

        self.set_session_data('locale', 'fr')
        self.set_session_data('ventilation_panel_skip', False)
        self.set_session_data('sokoban_first_move_time_0', None)
        self.set_session_data('sokoban_first_move_time_1', None)
        self.set_session_data('sokoban_first_move_time_2', None)
        self.set_session_data('sokoban_success_time_0', None)
        self.set_session_data('sokoban_success_time_1', None)
        self.set_session_data('sokoban_success_time_2', None)

    @on_event(filter={'category': 'start_tidy'})
    def start_tidy_room(self):
        self.reset_room()
        self.register_delayed_task(1, self.front_door_open)
        self.register_delayed_task(1, self.emergency_exit_unlock_to_outside)
        self.register_delayed_task(1, self.emergency_exit_unlock_stock_to_machine)
        self.register_delayed_task(1, self.waffle_trapdoor_open)
        self.register_delayed_task(
            1, self.publish_prefix, {'category': 'light_on', 'led_id': 'niryo'}, 'waffle_factory')
        self.register_delayed_task(
            1, self.publish_prefix, {'category': 'light_on', 'led_id': 'printer'}, 'waffle_factory')
        self.register_delayed_task(1, self.publish_prefix, {'category': 'high'}, 'stock_lights')
        self.register_delayed_task(1, self.set_cursor_visibility, True)

    @on_event(filter={'category': 'end_tidy'})
    def end_tidy_room(self):
        self.register_delayed_task(1, self.set_cursor_visibility, False)
        self.publish_prefix({'category': 'table_up'}, 'control_panel')
        self.publish_prefix({'category': 'play_animation', 'animation': 'reset'}, 'waffle_factory')
        self.halt_room()
        self.reset_room()

    @on_event(filter={'from_': 'webmin', 'category': 'request_session_data_for_webmin'})
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
        if key == "node_register":
            log = False
        else:
            log = True
        self.publish_prefix(
            {"category": "set_session_data", "key": key, "data": data}, "webmin", log=log)

    @on_event(filter={'category': 'ping'})
    def event_ping(self, from_: str):
        node_register = self.session_data.get("node_register", {})
        node_register[from_] = datetime.now(tz=timezone.utc).isoformat()
        self._record_session_data("node_register", node_register)

    @on_event(filter={'from_': 'street_display', 'category': 'unlock_front_door'})
    def street_display_event_unlock_front_door(self):
        self.publish_prefix({'category': 'play', 'sound_id': 'front_door_open'}, 'sound_player')
        self.publish_prefix({'category': 'unlock', 'relock': True}, 'front_door_magnet')

    @on_event(filter={'from_': 'chopsticks', 'category': 'reset'})
    def chopsticks_reset(self):
        self.set_session_data('chopsticks_success_time', None)
        self.set_session_data('chopsticks_first_move_time', None)

        self.chopsticks_voice_clue_1.pause()
        self.chopsticks_voice_clue_1.cancel()
        self.chopsticks_voice_clue_2.pause()
        self.chopsticks_voice_clue_2.cancel()

    @on_event(filter={'from_': 'chopsticks', 'category': 'first_move'})
    def chopsticks_first_move(self):
        self.set_session_data('chopsticks_first_move_time', self.session_time or 0)
        self.chopsticks_voice_clue_1.pause()
        self.chopsticks_voice_clue_2.pause()

    @on_event(filter={'from_': 'chopsticks', 'category': 'set_color'})
    def chopsticks_event_set_color(self, new_color: str):
        if new_color == 'blue':
            self.publish_prefix({'category': 'play', 'sound_id': 'ambiant_light_blue'}, 'sound_player')
        elif new_color == 'orange':
            self.publish_prefix({'category': 'play', 'sound_id': 'ambiant_light_orange'}, 'sound_player')

    @on_event(filter={'from_': 'chopsticks', 'category': 'success'})
    def chopsticks_event_success(self):
        # In case the success is forced
        self.chopsticks_voice_clue_1.pause()
        self.chopsticks_voice_clue_2.pause()

        self.set_session_data('chopsticks_success_time', self.session_time or 0)
        self.publish_prefix({'category': 'set_status', 'status': 'playing'}, 'control_panel')

    @on_event(filter={'from_': 'control_panel', 'category': 'first_manual_mode'})
    def control_panel_event_manual_mode(self):
        self.cancel_delayed_task(self.modify_fx_task)
        self.publish_prefix({'category': 'stop', 'track_id': 'track1'}, 'music_player')
        self.publish_prefix({'category': 'stop', 'track_id': 'chaotic_atmosphere'}, 'music_player')
        self.publish_prefix({'category': 'play', 'track_id': 'track2'}, 'music_player')
        self.register_delayed_task(
            5, self.publish_prefix, {'category': 'play', 'track_id': 'atmosphere'}, 'music_player')
        self.publish_prefix({'category': 'play', 'sound_id': 'on_manual_mode'}, 'sound_player')
        self.publish_prefix({'category': 'play_overlay_video', 'video_id': 'glitching_less'}, 'orders')
        self.publish_prefix({'category': 'stop_overlay_video'}, 'synchronizer')
        self.play_ads()

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

    def play_ads(self):
        self.displaying_ads_loop = True
        self.register_delayed_task(  # One second later to avoid seeing rpi's desktop during loading time
            1, self.publish_prefix, {'category': 'stop', 'video_id': 'ads_glitch'}, 'advertiser')

        if self.display_multiple_ads:
            self.publish_prefix(
                {
                    'category': 'play',
                    'video_id': 'ads_loop'
                },
                'advertiser'
            )

        else:
            self.publish_prefix(
                {
                    'category': 'play',
                    'video_id': f'waffresco_ad_loop{self.get_locale_suffix()}'
                },
                'advertiser'
            )

    @on_event(filter={'from_': 'synchronizer', 'category': 'set_menu_entry'})
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

    @on_event(filter={'from_': 'synchronizer', 'category': 'light_service_success'})
    def synchronizer_event_light_service_success(self):
        self.synchronizer_light_service_repaired = True
        self.light_service_success_animation_task = self.register_delayed_task(1, self.light_service_success_animation)
        self.publish_prefix({'category': 'set_lights_service_status', 'repaired': True}, 'control_panel')

    @on_event(filter={'from_': 'synchronizer', 'category': 'menu_service_success'})
    def synchronizer_event_menu_service_success(self):
        self.publish_prefix({'category': 'set_menu_service_status', 'repaired': True}, 'control_panel')

    @on_event(filter={'from_': 'synchronizer', 'category': 'services_synchronization_success'})
    def synchronizer_event_services_synchronization_success(self):
        self.publish_prefix({'category': 'play', 'sound_id': 'on_restaurant_start'}, 'sound_player')

        if self.synchronizer_light_service_repaired:
            self.cancel_delayed_task(self.light_service_success_animation_task)
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
            6, self.publish_prefix, {
                'category': 'play_overlay_video',
                'video_id': 'ads_loop'
            },
            'synchronizer'
        )

    @on_event(filter={'from_': 'holographic_menu', 'category': 'play_slide'})
    def holographic_menu_event_play_slide(self, slide: int):
        self.publish_prefix({'category': 'set_menu_cursor_position', 'position': slide}, 'synchronizer')

    @on_event(filter={'from_': 'synchronizer', 'category': 'check_for_menu_hint_log'})
    def check_for_menu_hint_log(self, dishes: list, auto_validate_dishes: bool):
        now = time.monotonic()

        if now - self.menu_last_log_hint_time < 40:
            return

        good_dishes_wrong_price_counter = 0
        for dish in dishes:
            if dish in self.EXPECTED_MENU:
                good_dishes_wrong_price_counter += 1

        hint = None
        if good_dishes_wrong_price_counter < 4:
            self.wrong_dishes_counter += 1
            modulus = 8 if auto_validate_dishes else 3
            threshold = 1 if auto_validate_dishes else 0
            if self.wrong_dishes_counter % modulus == 0 and self.wrong_dishes_counter >= threshold:
                if good_dishes_wrong_price_counter == 0:
                    self.menu_last_log_hint_time = time.monotonic()
                    hint = 'no_dishes_can_be_produced'
                else:
                    self.menu_last_log_hint_time = time.monotonic()
                    hint = 'some_dishes_cannot_be_produced'
        else:
            self.all_dishes_are_good_but_wrong_price_counter += 1
            if self.all_dishes_are_good_but_wrong_price_counter % 3 == 0:
                self.menu_last_log_hint_time = time.monotonic()
                hint = 'dishes_need_to_have_good_prices'

        if hint:
            self.publish_prefix(
                {
                    'category': 'menu_log',
                    'message': hint,
                    'level': 'warning',
                    'use_locale': True,
                    'with_sound': True,
                },
                'synchronizer',
            )

    @on_event(filter={'from_': 'load_cells', 'category': 'load_cell'})
    def load_cells_event_load_cell(self, color: str, id: int, activated: bool):
        self.publish_prefix({'category': 'load_cell', 'color': color, 'id': id, 'activated': activated}, 'synchronizer')

    @on_event(filter={'from_': 'synchronizer', 'category': 'on'})
    def synchronizer_event_on(self, color: str):
        self.publish_prefix({'category': 'on', 'color': color}, 'refectory_lights')

    @on_event(filter={'from_': 'synchronizer', 'category': 'off'})
    def synchronizer_event_off(self, color: str):
        self.publish_prefix({'category': 'off', 'color': color}, 'refectory_lights')

    def first_order_niryo_light_on(self):
        self.register_delayed_task(
            1, self.publish_prefix, {'category': 'light_on', 'led_id': 'niryo'}, 'waffle_factory')

    @on_event(filter={'from_': 'orders', 'category': 'first_order'})
    def orders_first_order(self):
        if self.persistent_settings['order_with_niryo_and_printer']:
            self.publish_prefix(
                {'category': 'set_volume', 'track_id': 'track3', 'volume': 0, 'duration': 2}, 'music_player')
            self.first_order_niryo_light_on()
            self.register_delayed_task(
                1, self.publish_prefix, {'category': 'play', 'track_id': 'track5'}, 'music_player')

            self.register_delayed_task(
                0.5, self.publish_prefix, {'category': 'set_display_processing_order_notification', 'value': True},
                'orders')
            self.register_delayed_task(
                0.5, self.publish_prefix, {'category': 'off', 'color': 'white'}, 'refectory_lights')
            self.register_delayed_task(
                0.5, self.publish_prefix, {'category': 'off', 'color': 'blue'}, 'refectory_lights')

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
                self.NIRYO_BUGGED_ANIMATION_DURATION + 6 + 1, self.publish_prefix,
                {'category': 'set_display_processing_order_notification', 'value': False}, 'orders')
            delay = self.NIRYO_BUGGED_ANIMATION_DURATION + 6
        else:
            delay = 1
            self.register_delayed_task(
                0.5, self.publish_prefix,
                {'category': 'set_volume', 'track_id': 'track3', 'volume': 40, 'duration': 2}, 'music_player')

        self.register_delayed_task(
            delay, self.publish_prefix,
            {'category': 'play_overlay_video', 'video_id': 'ms_pepper_stock'}, 'orders')
        self.register_delayed_task(
            delay, self.publish_prefix,
            {'category': 'play_ms_pepper_overlay_video', 'video_id': 'ms_pepper_stock'}, 'synchronizer')
        self.register_delayed_task(
            delay - 1, self.publish_prefix,
            {'category': 'stop', 'video_id': 'street_idle'}, 'advertiser')
        self.register_delayed_task(
            delay, self.publish_prefix,
            {'category': 'play', 'video_id': 'ms_pepper_stock'}, 'advertiser')
        ms_pepper_tells_to_go_in_stock_duration = 27.25
        self.register_delayed_task(
            delay + ms_pepper_tells_to_go_in_stock_duration + 1,  # + 1 to be sure
            self.publish_prefix, {'category': 'play', 'video_id': 'street_idle'}, 'advertiser')

    @on_event(filter={'from_': 'orders', 'category': 'ms_pepper_has_told_to_go_in_stock'})
    def ms_pepper_has_told_to_go_in_stock(self):
        def post_delay():
            self.ventilation_panel_skip.pause()

            self.publish_prefix(
                {'category': 'set_volume', 'track_id': 'track3', 'volume': 0, 'duration': 5}, 'music_player')

            if not self.session_data['ventilation_panel_skip']:
                self.publish_prefix({'category': 'set_status', 'status': 'playing'}, 'ventilation_panel')

                self.publish_prefix({'category': 'set_volume', 'track_id': 'track35', 'volume': 0}, 'music_player')
                self.register_delayed_task(
                    2.5, self.publish_prefix, {'category': 'play', 'track_id': 'track35'}, 'music_player')
                self.register_delayed_task(
                    2.5, self.publish_prefix,
                    {'category': 'set_volume', 'track_id': 'track35', 'volume': 40, 'duration': 1}, 'music_player')
            else:
                self.ventilation_panel_success()

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

    def resume_order_niryo_catch_attention(self):
        pass

    @on_event(filter={'from_': 'orders', 'category': 'resume_order'})
    def orders_resume_order(self):
        self.register_delayed_task(
            0.5, self.publish_prefix,
            {'category': 'set_volume', 'track_id': 'track3', 'volume': 0, 'duration': 2}, 'music_player')

        self.publish_prefix(
            {
                "category": "log",
                "use_locale": True,
                "message": "resume_order",
                "level": "info",
                "with_sound": False,
            },
            "inventory"
        )

        if self.persistent_settings['order_with_niryo_and_printer']:
            self.publish_prefix(
                {
                    "category": "log",
                    "use_locale": True,
                    "message": "robotic_arm_activation",
                    "level": "info",
                    "with_sound": False,
                },
                "inventory"
            )
            self.publish_prefix(
                {
                    "category": "log",
                    "use_locale": True,
                    "message": "printer_activation",
                    "level": "info",
                    "with_sound": False,
                },
                "inventory"
            )

            self.register_delayed_task(
                1, self.publish_prefix, {'category': 'set_display_processing_order_notification', 'value': True},
                'orders')

            self.register_delayed_task(
                1, self.publish_prefix,
                {'category': 'play', 'track_id': 'track5'}, 'music_player')
            self.register_delayed_task(
                1, self.publish_prefix,
                {'category': 'set_volume', 'track_id': 'track5', 'volume': 55, 'duration': 1}, 'music_player')

            self.resume_order_niryo_catch_attention()

            self.register_delayed_task(
                0.5, self.publish_prefix, {'category': 'off', 'color': 'white'}, 'refectory_lights')
            self.register_delayed_task(
                0.5, self.publish_prefix, {'category': 'off', 'color': 'blue'}, 'refectory_lights')

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
                    {'category': 'print_pattern', 'pattern': 'heart'}, 'waffle_factory')

            delay += self.first_pattern_print_duration
            self.register_delayed_task(
                delay, self.publish_prefix,
                {'category': 'play_animation', 'animation': 'waffle_end'}, 'waffle_factory')

            basket_led_blink_delay = delay + self.basket_led_blink_delay
            self.register_delayed_task(
                basket_led_blink_delay, self.publish_prefix,
                {'category': 'basket_led_blink'}, 'waffle_factory')

            self.register_delayed_task(
                basket_led_blink_delay + self.basket_led_blinking_time, self.publish_prefix,
                {'category': 'basket_led_off'}, 'waffle_factory')

            delay += self.ms_pepper_says_thanks_delay
            self.register_delayed_task(
                delay - 1.5, self.publish_prefix,
                {'category': 'set_volume', 'track_id': 'track5', 'volume': 0, 'duration': 1}, 'music_player')

            self.register_delayed_task(
                delay + 1, self.publish_prefix, {'category': 'set_display_processing_order_notification',
                'value': False}, 'orders')

        else:
            delay = self.ms_pepper_says_thanks_delay + 1

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

    @on_event(filter={'from_': 'orders', 'category': 'ms_pepper_has_said_thanks'})
    def orders_ms_pepper_has_said_thanks(self):
        def print_m():
            self.publish_prefix({'category': 'print_pattern', 'pattern': 'M'}, 'waffle_factory')
            self.second_waffle_print_timing = self.session_time or 0

        self.publish_prefix(
            {'category': 'set_volume', 'track_id': 'track62', 'volume': 0, 'duration': 10}, 'music_player')
        self.register_delayed_task(1.5, self.publish_prefix, {'category': 'play', 'track_id': 'track7'}, 'music_player')
        self.register_delayed_task(
            37.5 + 1.5, self.publish_prefix,
            {'category': 'set_volume', 'track_id': 'track7', 'volume': 55, 'duration': 1}, 'music_player')
        if self.persistent_settings['order_with_niryo_and_printer']:
            self.register_delayed_task(
                37.5 + 1.5 + 2, self.publish_prefix,
                {'category': 'play_animation', 'animation': 'second_waffle_init'}, 'waffle_factory')
            if self.persistent_settings['dry_print'] is False:
                self.register_delayed_task(
                    37.5 + 1.5 + 2 + self.second_waffle_init_conveyor_duration,
                    print_m)
        self.register_delayed_task(
            37.5 + 25 + 1.5, self.publish_prefix,
            {'category': 'set_volume', 'track_id': 'track7', 'volume': 45, 'duration': 10}, 'music_player')

    def boost_fog(self):
        self.publish_prefix({'category': 'send_fog', 'duration': self.boost_fog_duration}, 'fog_machine')
        self.boost_fog_timer.pause()
        self.boost_fog_timer.cancel()
        self.boost_fog_timer.start()

    @on_event(filter={'from_': 'orders', 'category': 'marmitron_has_asked_for_help'})
    def orders_marmitron_has_asked_for_help(self):
        self.publish_prefix({'category': 'enable'}, 'digital_lock')
        self.publish_prefix({'category': 'calibrate'}, 'secure_floor')
        self.register_delayed_task(
            3, self.publish_prefix,
            {'category': 'send_fog', 'duration': self.initial_fog_duration}, 'fog_machine')
        self.boost_fog_timer.start()

        if self.persistent_settings['order_with_niryo_and_printer'] and not self.persistent_settings['dry_print']:
            display_order_recap_delay = self.config['display_order_recap_delay']
        else:
            display_order_recap_delay = 1
        self.register_delayed_task(
            display_order_recap_delay, self.publish_prefix,
            {'category': 'set_display_order_recap_notification', 'value': True}, 'orders')

    @on_event(filter={'from_': 'payment_module', 'category': 'set_credits'})
    def payment_module_event_set_credits(self, value):
        self.publish_prefix({'category': 'set_credits', 'value': value}, 'orders')

    def set_ventilation_panel_skip(self):
        self.set_session_data('ventilation_panel_skip', True)

    @on_event(filter={'widget_id': 'ventilation_panel', 'action': 'set_round_difficulty'})
    def ventilation_panel_set_difficulty(self, round_: int, difficulty_index: int, instruction_set_index: int):
        self.publish_prefix(
            {
                'category': 'set_round_difficulty',
                'round_': round_,
                'difficulty_index': difficulty_index,
                'instruction_set_index': instruction_set_index,
            },
            'ventilation_panel'
        )

    @on_event(filter={'from_': 'ventilation_panel', 'category': 'good_connection'})
    def ventilation_panel_event_good_connection(self, sequence_cursor: int):
        if 0 <= sequence_cursor <= 8:
            self.publish_prefix(
                {'category': 'play', 'sound_id': f'ventilation_combo_{sequence_cursor}'}, 'sound_player')

    @on_event(filter={'from_': 'ventilation_panel', 'category': 'bad_move'})
    def ventilation_panel_event_bad_move(self):
        self.publish_prefix({'category': 'play', 'sound_id': 'ventilation_error'}, 'sound_player')

    @on_event(filter={'from_': 'ventilation_panel', 'category': 'round_complete'})
    def ventilation_panel_event_round_complete(self):
        self.register_delayed_task(
            0.5, self.publish_prefix, {'category': 'play', 'sound_id': 'ventilation_round_success'}, 'sound_player')

    @on_event(filter={'from_': 'ventilation_panel', 'category': 'start_new_round'})
    def ventilation_panel_event_start_new_round(self, round):
        # Ventilation panel rounds are 0, 1, 2. Documentation rounds are 1, 2, 3
        if round is not None:
            self.publish_prefix({'category': 'set_ventilation_panel_round', 'round': round + 1}, 'orders')
        self.set_session_data('ventilation_panel_round', round)

    @on_event(filter={'from_': 'ventilation_panel', 'category': 'set_status'})
    def ventilation_panel_event_set_status(self, status: str):
        if status == 'playing':
            self.publish_prefix({'category': 'set_documentation_visibility', 'show': True}, 'orders')
        else:
            self.publish_prefix({'category': 'set_documentation_visibility', 'show': False}, 'orders')

    @on_event(filter={'from_': 'ventilation_panel', 'category': 'notify_instruction'})
    def ventilation_panel_notify_instruction(self, instruction):
        self.publish_prefix(
            {'category': 'set_documentation_current_instruction', 'message': instruction, 'use_locale': True},
            'orders'
        )

    @on_event(filter={'from_': 'ventilation_panel', 'category': 'success'})
    def ventilation_panel_success(self):
        self.publish_prefix({'category': 'on'}, 'fog_machine')
        self.publish_prefix({'category': 'unlock'}, 'vents_locker')
        self.publish_prefix({'category': 'display_black_screen', 'display': False}, 'inventory')
        self.publish_prefix({'category': 'set_playing', 'value': True}, 'cylinders')

        self.register_delayed_task(1, self.publish_prefix, {'category': 'stop', 'track_id': 'track35'}, 'music_player')
        self.register_delayed_task(1, self.publish_prefix, {'category': 'play', 'track_id': 'track4'}, 'music_player')

        self.register_delayed_task(4, self.publish_prefix, {'category': 'high'}, 'stock_lights')

    @on_event(filter={'widget_id': 'ventilation_panel', 'action': 'restart_round'})
    def ventilation_panel_restart_round_from_webmin(self):
        self.publish_prefix({'category': 'restart_round'}, 'ventilation_panel')

    @on_event(filter={'from_': 'orders', 'category': 'restart_round'})
    def ventilation_panel_restart_round(self):
        self.publish_prefix({'category': 'restart_round'}, 'ventilation_panel')

    @on_event(filter={'from_': 'sokoban_controls', 'category': 'control'})
    def sokoban_controls_event(self, name: str, pressed: bool):
        self.publish_prefix({'category': 'control', 'name': name, 'pressed': pressed}, 'inventory')

    @on_event(filter={'widget_id': 'sokoban', 'action': 'set_difficulty'})
    def sokoban_set_difficulty(self, difficulty: str):
        self.publish_prefix({'category': 'set_difficulty', 'difficulty': difficulty}, 'inventory')

    @on_event(filter={'widget_id': 'sokoban', 'action': 'queue_moves'})
    def sokoban_queue_moves(self, moves: list):
        self.publish_prefix({'category': 'queue_moves', 'moves': moves}, 'inventory')

    @on_event(filter={'from_': 'inventory', 'category': 'sokoban_start_level'})
    def sokoban_start_level(self, level: int):
        self.set_session_data(f'sokoban_first_move_time_{level}', self.session_time or 0)
        if level > 0:
            self.set_session_data(f'sokoban_success_time_{level - 1}', self.session_time or 0)

    @on_event(filter={'from_': 'inventory', 'category': 'success'})
    def sokoban_success(self):
        self.set_session_data('sokoban_success_time_2', self.session_time or 0)
        self.set_session_data('sokoban_success', True)
        self.publish_prefix({'category': 'is_sokoban_cleared', 'value': True}, 'cylinders')

    @on_event(filter={'from_': 'inventory', 'category': 'first_face_change'})
    def sokoban_first_face_change(self):
        # TODO: cancel timer
        pass

    @on_event(filter={'from_': 'cylinders', 'category': 'tag'})
    def cylinder_tag(self, tag, ok: bool, chamber: int):
        if tag:
            self.publish_prefix({'category': 'play', 'sound_id': 'cylinder_scan'}, 'sound_player')
        self.set_session_data(f'cylinders_chamber_{chamber}', {'inserted': tag is not None, 'ok': ok})

    @on_event(filter={'from_': 'cylinders', 'category': 'check_availability_scan'})
    def cylinder_check_availability_scan(self):
        self.publish_prefix({'category': 'play', 'sound_id': 'cylinder_scan'}, 'sound_player')

    @on_event(filter={'from_': 'cylinders', 'category': 'availability'})
    def cylinders_availability(self):
        self.publish_prefix({'category': 'availability'}, 'root_server')

    @on_event(filter={'from_': 'cylinders', 'category': 'success'})
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

    @on_event(filter={'from_': 'digital_lock', 'category': 'success'})
    def digital_lock_success(self):
        self.publish_prefix({'category': 'set_status', 'status': 'playing'}, 'secure_floor')
        self.publish_prefix({'category': 'set_status', 'status': 'playing'}, 'laser_maze')
        self.publish_prefix({'category': 'playing'}, 'human_authenticator')

        # If players rush the puzzle, the printer doesn't have enough time to finish printing. So we make sure
        # players have waited enough time to send the waffle immediately, or we wait at least 5 seconds.
        print_delta_time = (self.session_time or 0) - self.second_waffle_print_timing
        safe_delay = max(48 - print_delta_time, 0)

        if self.persistent_settings['order_with_niryo_and_printer']:
            self.register_delayed_task(
                safe_delay,
                self.publish_prefix, {'category': 'play_animation', 'animation': 'waffle_end'}, 'waffle_factory')

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

    @on_event(filter={'from_': 'secure_floor', 'category': 'clear'})
    def secure_floor_event_clear(self):
        self.publish_prefix({'category': 'set_status', 'status': 'playing'}, 'laser_maze')
        self.publish_prefix({'category': 'set_status', 'status': 'playing'}, 'human_authenticator')
        self.publish_prefix({'category': 'set_volume', 'track_id': 'alarm', 'volume': 0, 'duration': 1}, 'music_player')
        self.publish_prefix({'category': 'display_alarm_window', 'display': False}, 'root_server')
        self.publish_prefix({'category': 'display_alarm_window', 'display': False}, 'digital_lock')
        self.publish_prefix({'category': 'stop', 'track_id': 'alarm'}, 'music_player')

    @on_event(filter={'category': 'laser_alarm'})
    def laser_maze_event_alarm(self):
        self.publish_prefix({'category': 'set_status', 'status': 'stop_playing'}, 'laser_maze')
        self.publish_prefix({'category': 'set_status', 'status': 'alarm'}, 'secure_floor')
        self.publish_prefix({'category': 'set_status', 'status': 'disabled'}, 'human_authenticator')
        self.publish_prefix({'category': 'play', 'sound_id': 'laser_trigger'}, 'sound_player')
        self.publish_prefix({'category': 'set_volume', 'track_id': 'alarm', 'volume': 40}, 'music_player')
        self.publish_prefix({'category': 'play', 'track_id': 'alarm'}, 'music_player')
        self.publish_prefix({'category': 'display_alarm_window', 'display': True}, 'root_server')
        self.publish_prefix({'category': 'display_alarm_window', 'display': True}, 'digital_lock')

    @on_event(filter={'from_': 'human_authenticator', 'category': 'success'})
    def human_authenticator_event_success(self):
        self.boost_fog_timer.pause()
        self.boost_fog_timer.cancel()
        self.publish_prefix({'category': 'set_status', 'status': 'success'}, 'laser_maze')
        self.publish_prefix({'category': 'success'}, 'secure_floor')
        self.publish_prefix({'category': 'show_ui'}, 'root_server')
        self.publish_prefix({'category': 'display_alarm_window', 'display': False}, 'root_server')
        self.publish_prefix({'category': 'display_alarm_window', 'display': False}, 'digital_lock')
        self.publish_prefix({'category': 'off', 'color': 'all'}, 'refectory_lights')
        self.register_delayed_task(
            1,
            self.publish_prefix, {'category': 'stop', 'video_id': 'ads_loop'},
            'advertiser'
        )
        self.register_delayed_task(
            1,
            self.publish_prefix, {'category': 'stop', 'video_id': 'waffresco_ad_loop_fr'},
            'advertiser'
        )
        self.register_delayed_task(
            1,
            self.publish_prefix, {'category': 'stop', 'video_id': 'waffresco_ad_loop_en'},
            'advertiser'
        )
        self.register_delayed_task(
            1, self.publish_prefix, {'category': 'stop', 'video_id': 'ads_glitch'}, 'advertiser')
        self.publish_prefix({'category': 'play', 'video_id': 'blackscreen'}, 'advertiser')
        self.publish_prefix({'category': 'light_off', 'led_id': 'niryo'}, 'waffle_factory')
        self.publish_prefix({'category': 'light_off', 'led_id': 'printer'}, 'waffle_factory')
        self.publish_prefix({'category': 'display_black_screen', 'display': True}, 'synchronizer')
        self.publish_prefix({'category': 'display_black_screen', 'display': True}, 'orders')
        self.register_delayed_task(
            3, self.publish_prefix, {'category': 'display_password_window'}, 'root_server')
        self.register_delayed_task(
            4.5, self.publish_prefix, {'category': 'play_animation', 'animation': 'reponse'}, 'root_server')

    @on_event(filter={'widget_id': 'synchronizer', 'action': 'set'})
    def widget_synchronizer(self, key: str, value):
        if key == 'synchronizer_auto_validate_dishes':
            self.publish_prefix({'category': 'set_auto_validate_dishes', 'value': value}, 'synchronizer')
        elif key == 'synchronizer_display_price':
            self.publish_prefix({'category': 'display_price', 'display': value}, 'synchronizer')
        elif key == 'synchronizer_price_matters':
            self.publish_prefix({'category': 'set_price_matters', 'value': value}, 'synchronizer')
        elif key == 'synchronizer_display_menu_explicit_instruction':
            self.publish_prefix({'category': 'set_display_menu_explicit_instruction', 'value': value}, 'synchronizer')
        elif key == 'synchronizer_strict_loading_mode':
            self.publish_prefix({'category': 'set_strict_loading_mode', 'value': value}, 'synchronizer')
        elif key == 'synchronizer_display_light_explicit_instruction':
            self.publish_prefix({'category': 'set_display_light_explicit_instruction', 'value': value}, 'synchronizer')
        elif key == 'synchronizer_explain_on_dish_changed_counter':
            self.publish_prefix(
                {'category': 'set_explain_on_dish_changed_counter', 'value': value}, 'synchronizer')

    @on_event(filter={'widget_id': 'cylinders', 'action': 'set'})
    def widget_cylinders_set(self, key: str, value: bool):
        if key == 'cylinders_playing':
            self.publish_prefix({'category': 'set_playing', 'value': value}, 'cylinders')
        elif key == 'cylinders_reveal_mistakes':
            self.publish_prefix({'category': 'set_reveal_mistakes', 'value': value}, 'cylinders')
        elif key == 'cylinders_success' and value:
            self.publish_prefix({'category': 'force_success'}, 'cylinders')

    @on_event(filter={'widget_id': 'cylinders', 'action': 'reset'})
    def widget_cylinders_reset(self):
        self.publish_prefix({'category': 'reset'}, 'cylinders')

    @on_event(filter={'widget_id': 'root_server', 'action': 'set'})
    def root_server_set_session_data_value(self, key: str, value: bool):
        if key == 'root_server_simplified_ui':
            self.publish_prefix({'category': 'set_simplified_ui', 'value': value}, 'root_server')
        elif key == 'root_server_display_ingredients':
            self.publish_prefix({'category': 'set_display_ingredients', 'value': value}, 'root_server')
        elif key == 'root_server_pulsate_check_availability_button':
            self.publish_prefix({'category': 'set_pulsate_check_availability_button', 'value': value}, 'root_server')

    @on_event(filter={'from_': 'root_server', 'category': 'check_availability'})
    def root_server_check_availability(self, id: str):
        self.publish_prefix({'category': 'check_availability', 'id': id}, 'cylinders')

    @on_event(filter={'from_': 'root_server', 'category': 'success'})
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

        self.session_timer.pause()

    @on_event(filter={'from_': 'root_server', 'category': 'ms_pepper_mad_end'})
    def root_server_event_ms_pepper_mad_end(self):
        self.publish_prefix({'category': 'display_danger_window'}, 'synchronizer')
        self.publish_prefix({'category': 'display_danger_window'}, 'orders')
        self.publish_prefix({'category': 'display_danger_window'}, 'inventory')
        self.publish_prefix({'category': 'display_danger_window'}, 'root_server')
        self.publish_prefix({'category': 'alarm', 'activated': True}, 'relays')
        self.publish_prefix({'category': 'forced_alarm'}, 'secure_floor')
        self.publish_prefix({'category': 'set_status', 'status': 'disabled'}, 'human_authenticator')
        self.publish_prefix({'category': 'send_fog', 'duration': 10}, 'fog_machine')
        self.register_delayed_task(15, self.publish_prefix, {'category': 'off'}, 'fog_machine')
        self.publish_prefix({'category': 'play', 'sound_id': 'gaz'}, 'sound_player')
        self.register_delayed_task(2, self.publish_prefix, {'category': 'play', 'track_id': 'alarm'}, 'music_player')
        self.register_delayed_task(
            30, self.publish_prefix, {'category': 'set_volume', 'track_id': 'alarm', 'volume': 0, 'duration': 5},
            'music_player')
        self.register_delayed_task(
            10, self.publish_prefix, {'category': 'set_volume', 'track_id': 'atmosphere', 'volume': 0, 'duration': 5},
            'music_player')
        self.register_delayed_task(
            35, self.publish_prefix, {'category': 'stop', 'track_id': 'alarm'}, 'music_player')

        if self.persistent_settings['final_by_refectory']:
            self.register_delayed_task(
                5, self.play_sound, 'marmitron_7', True)
            self.register_delayed_task(
                8, self.publish_prefix, {'category': 'play', 'sound_id': 'front_door_open'}, 'sound_player')
            self.register_delayed_task(
                8, self.publish_prefix, {'category': 'unlock', 'relock': True}, 'front_door_magnet')
        else:
            self.register_delayed_task(
                2, self.play_sound, 'marmitron_7', True)
            self.register_delayed_task(
                5, self.publish_prefix,
                {'category': 'unlock', 'magnet_id': 'to_outside', 'relock': True}, 'emergency_exit')
            self.register_delayed_task(
                5, self.publish_prefix, {'category': 'unlock', 'relock': True}, 'front_door_magnet')

        self.publish_prefix({'category': 'on', 'color': 'all_but_white'}, 'refectory_lights')
        self.register_delayed_task(
            1, self.publish_prefix, {'category': 'stop', 'video_id': 'blackscreen'}, 'advertiser')
        self.play_ads()
        self.publish_prefix({'category': 'light_on', 'led_id': 'niryo'}, 'waffle_factory')
        self.publish_prefix({'category': 'light_on', 'led_id': 'printer'}, 'waffle_factory')
        self.publish_prefix({'category': 'display_black_screen', 'display': False}, 'synchronizer')
        self.publish_prefix({'category': 'display_black_screen', 'display': False}, 'orders')

    @on_event(filter={'widget_type': 'timer', 'action': 'start'})
    def tracked_timer_start(self, name: str):
        if name in self._timers:
            if self._timers[name].state == TimerState.NOT_STARTED:
                self._timers[name].start()
            elif self._timers[name].state == TimerState.PAUSED:
                self._timers[name].manual_resume()

    @on_event(filter={'widget_type': 'timer', 'action': 'pause'})
    def tracked_timer_pause(self, name: str):
        if name in self._timers:
            self._timers[name].manual_pause()

    @on_event(filter={'widget_type': 'timer', 'action': 'cancel'})
    def tracked_timer_cancel(self, name: str):
        if name in self._timers:
            self._timers[name].cancel()

    @on_event(filter={'widget_type': 'timer', 'action': 'execute'})
    def tracked_timer_execute(self, name: str):
        if name in self._timers:
            self._timers[name].execute_callback()

    @on_event(filter={'widget_id': 'front_door_open'})
    def front_door_open(self, with_sound: bool = False):
        if with_sound:
            self.publish_prefix({'category': 'play', 'sound_id': 'front_door_open'}, 'sound_player')
        self.publish_prefix({'category': 'unlock', 'relock': True}, 'front_door_magnet')

    @on_event(filter={'widget_id': 'street_display_reset'})
    def button_street_display_reset(self):
        self.publish_prefix({'category': 'reset'}, 'street_display')

    @on_event(filter={'widget_id': 'advertiser_play_ms_pepper_here_you_are'})
    def button_advertiser_play_ms_pepper_here_you_are(self):
        self.publish_prefix(
            {
                'category': 'play',
                'video_id': f"""ms_pepper_here_you_are_{self.session_data["locale"]}""",
            },
            'advertiser'
        )

    @on_event(filter={'widget_id': 'advertiser_stop_ms_pepper_here_you_are'})
    def button_advertiser_stop_ms_pepper_here_you_are(self):
        self.publish_prefix(
            {
                'category': 'stop',
                'video_id': f"""ms_pepper_here_you_are_{self.session_data["locale"]}""",
            },
            'advertiser'
        )

    @on_event(filter={'widget_id': 'advertiser_play_ads_loop'})
    def button_advertiser_play_ads_loop(self):
        self.play_ads()

    @on_event(filter={'widget_id': 'advertiser_stop_ads_loop'})
    def button_advertiser_stop_ads_loop(self):
        self.publish_prefix(
            {
                'category': 'stop',
                'video_id': f'ads_loop'
            },
            'advertiser'
        )
        self.publish_prefix(
            {
                'category': 'stop',
                'video_id': f'waffresco_ad_loop_fr'
            },
            'advertiser'
        )
        self.publish_prefix(
            {
                'category': 'stop',
                'video_id': f'waffresco_ad_loop_en'
            },
            'advertiser'
        )

    @on_event(filter={'widget_id': 'advertiser_play_ads_glitch'})
    def button_advertiser_play_ads_glitch(self):
        self.publish_prefix({'category': 'play', 'video_id': 'ads_glitch'}, 'advertiser')

    @on_event(filter={'widget_id': 'advertiser_stop_ads_glitch'})
    def button_advertiser_stop_ads_glitch(self):
        self.publish_prefix({'category': 'stop', 'video_id': 'ads_glitch'}, 'advertiser')

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

    @on_event(filter={'widget_id': 'reset_synchronizer'})
    def button_reset_synchronizer(self):
        self.publish_prefix({'category': 'reset'}, 'synchronizer')

    @on_event(filter={'widget_id': 'synchronizer_overlay_video_glitch'})
    def button_synchronizer_overlay_video_glitch(self):
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

    @on_event(filter={'widget_id': 'maze_playing'})
    def button_maze_playing(self):
        self.publish_prefix({'category': 'set_status', 'status': 'playing'}, 'secure_floor')
        self.publish_prefix({'category': 'set_status', 'status': 'playing'}, 'laser_maze')
        self.publish_prefix({'category': 'playing'}, 'human_authenticator')

    @on_event(filter={'widget_id': 'maze_alarm'})
    def button_maze_alarm(self):
        self.publish_prefix({'category': 'set_status', 'status': 'alarm'}, 'secure_floor')
        self.publish_prefix({'category': 'set_status', 'status': 'stop_playing'}, 'laser_maze')
        self.publish_prefix({'category': 'set_status', 'status': 'disabled'}, 'human_authenticator')

    @on_event(filter={'widget_id': 'secure_floor_calibrate'})
    def button_secure_floor_calibrate(self):
        self.publish_prefix({'category': 'calibrate'}, 'secure_floor')

    @on_event(filter={'widget_id': 'maze_success'})
    def button_maze_success(self):
        self.publish_prefix({'category': 'success'}, 'secure_floor')
        self.publish_prefix({'category': 'set_status', 'status': 'success'}, 'laser_maze')
        self.publish_prefix({'category': 'set_status', 'status': 'success'}, 'human_authenticator')

    @on_event(filter={'widget_id': 'maze_reset'})
    def button_maze_reset(self):
        self.publish_prefix({'category': 'reset'}, 'laser_maze')
        self.publish_prefix({'category': 'reset'}, 'secure_floor')
        self.publish_prefix({'category': 'reset'}, 'human_authenticator')
        self.publish_prefix({'category': 'set_volume', 'track_id': 'alarm', 'volume': 0}, 'music_player')
        self.publish_prefix({'category': 'display_alarm_window', 'display': False}, 'root_server')
        self.publish_prefix({'category': 'display_alarm_window', 'display': False}, 'digital_lock')

    @on_event(filter={'widget_id': 'emergency_exit_unlock_to_outside'})
    def emergency_exit_unlock_to_outside(self):
        self.publish_prefix({'category': 'unlock', 'magnet_id': 'to_outside', 'relock': True}, 'emergency_exit')

    @on_event(filter={'widget_id': 'emergency_exit_lock_to_outside'})
    def button_emergency_exit_lock_to_outside(self):
        self.publish_prefix({'category': 'lock', 'magnet_id': 'to_outside'}, 'emergency_exit')

    @on_event(filter={'widget_id': 'emergency_exit_unlock_stock_to_machine'})
    def emergency_exit_unlock_stock_to_machine(self, with_sound: bool = False):
        if with_sound:
            self.publish_prefix({'category': 'play', 'sound_id': 'server_door_open'}, 'sound_player')
        self.publish_prefix({'category': 'unlock', 'magnet_id': 'stock_to_machine', 'relock': True}, 'emergency_exit')

    @on_event(filter={'widget_id': 'emergency_exit_lock_stock_to_machine'})
    def button_emergency_exit_lock_stock_to_machine(self):
        self.publish_prefix({'category': 'lock', 'magnet_id': 'stock_to_machine'}, 'emergency_exit')

    @on_event(filter={'widget_id': 'set_secure_floor_all_leds_color'})
    def button_set_secure_floor_all_leds_color(self, color: str):
        self.publish_prefix({'category': 'set_all_leds_color', 'color': color}, 'secure_floor')

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

    @on_event(filter={'widget_id': 'control_force_manual_mode'})
    def button_control_force_manual_mode(self):
        self.publish_prefix({'category': 'force_manual_mode'}, 'control_panel')

    @on_event(filter={'widget_id': 'synchronizer_restaurant_in_manual_mode'})
    def button_synchronizer_restaurant_in_manual_mode(self):
        self.publish_prefix({'category': 'restaurant_in_manual_mode'}, 'synchronizer')

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

    @on_event(filter={'widget_id': 'reset_inventory'})
    def button_reset_inventory(self):
        self.publish_prefix({'category': 'reset'}, 'inventory')
        self.set_session_data('sokoban_first_move_time_0', None)
        self.set_session_data('sokoban_first_move_time_1', None)
        self.set_session_data('sokoban_first_move_time_2', None)
        self.set_session_data('sokoban_success_time_0', None)
        self.set_session_data('sokoban_success_time_1', None)
        self.set_session_data('sokoban_success_time_2', None)

    @on_event(filter={'widget_id': 'inventory_black_screen'})
    def buttons_inventory_black_screen(self, display: bool):
        self.publish_prefix({'category': 'display_black_screen', 'display': display}, 'inventory')

    @on_event(filter={'widget_id': 'reset_orders'})
    def button_reset_orders(self):
        self.publish_prefix({'category': 'reset'}, 'orders')

    @on_event(filter={'widget_id': 'stop_orders_overlay_video'})
    def button_stop_orders_overlay_video(self):
        self.publish_prefix({'category': 'stop_overlay_video'}, 'orders')

    @on_event(filter={'widget_id': 'ventilation_panel', 'action': 'set_status'})
    def ventilation_panel_set_status(self, status: str):
        self.publish_prefix({'category': 'set_status', 'status': status}, 'ventilation_panel')

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
    def waffle_trapdoor_open(self):
        self.publish_prefix({'category': 'low'}, 'waffle_trapdoor')
        self.register_delayed_task(1, self.publish_prefix, {'category': 'high'}, 'waffle_trapdoor')

    @on_event(filter={'widget_id': 'backstage_trapdoor_open'})
    def buttons_backstage_trapdoor_open(self):
        self.publish_prefix({'category': 'low'}, 'backstage_trapdoor')
        self.register_delayed_task(1, self.publish_prefix, {'category': 'high'}, 'backstage_trapdoor')

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

    @on_event(filter={'widget_id': 'chopsticks', 'action': 'force_success'})
    def widget_chopsticks_success(self):
        self.publish_prefix({'category': 'force_success'}, 'chopsticks')

    @on_event(filter={'widget_id': 'chopsticks', 'action': 'reset'})
    def widget_chopsticks_reset(self):
        self.publish_prefix({'category': 'reset'}, 'chopsticks')

    @on_event(filter={'widget_id': 'chopsticks', 'action': 'emulate_chopstick_plug'})
    def widget_chopsticks_emulate_plug(self, letter_index: int):
        self.publish_prefix({'category': 'emulate_chopstick_plug', 'letter_index': letter_index}, 'chopsticks')

    @on_event(filter={'widget_id': 'chopsticks', 'action': 'emulate_chopstick_unplug'})
    def widget_chopsticks_emulate_unplug(self, letter_index: int):
        self.publish_prefix({'category': 'emulate_chopstick_unplug', 'letter_index': letter_index}, 'chopsticks')

    @on_event(filter={'widget_id': 'chopsticks', 'action': 'set_difficulty'})
    def widget_chopsticks_set_difficulty(self, difficulty: str):
        self.publish_prefix({'category': 'set_difficulty', 'difficulty': difficulty}, 'chopsticks')

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

    @on_event(filter={'widget_id': 'vents_locker'})
    def buttons_vents_locker(self, lock: bool):
        self.publish_prefix({'category': 'lock' if lock else 'unlock'}, 'vents_locker')

    @on_event(filter={'widget_id': 'alarm_relays'})
    def buttons_alarm_relays(self, activated: bool):
        self.publish_prefix({'category': 'alarm', 'activated': activated}, 'relays')

    @on_event(filter={'category': 'localize'})
    def localize(self, value: str):
        if value in ['fr', 'en']:
            if self.displaying_ads_loop:
                if not self.display_multiple_ads:
                    self.register_delayed_task(
                        1,
                        self.publish_prefix,
                        {
                            'category': 'stop',
                            'video_id': f'waffresco_ad_loop{self.get_locale_suffix()}'
                        },
                        'advertiser'
                    )

            self.set_session_data('locale', value)
            self.publish_prefix({'category': 'set_locale', 'locale': value}, 'broadcast')

            if self.displaying_ads_loop:
                self.play_ads()

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
        self.tic_tac_callback(self.session_timer)

    @on_event(filter={'widget_type': 'lasers', 'action': 'set_activated'})
    def toggle_permanent_laser_activation(self, activated: bool, laser_maze_channel: str, laser_index: int):
        self.publish_prefix(
            {'category': 'set_activated', 'activated': activated, 'index': laser_index}, laser_maze_channel)

    @on_event(filter={'widget_type': 'lasers', 'action': 'set_failures_to_auto_deactivate'})
    def set_failures_to_auto_deactivate(self, n: int):
        self.publish_prefix(
            {'category': 'set_failures_to_auto_deactivate', 'n': n}, 'laser_maze')

    @on_event(filter={'widget_type': 'lasers', 'action': 'set_check_sensors_delay'})
    def set_check_sensors_delay(self, n: int):
        self.publish_prefix(
            {'category': 'set_sensors_delay', 'value': n}, 'laser_maze')

    @on_event(filter={'widget_type': 'lasers', 'action': 'set_status'})
    def laser_set_status(self, status: str):
        self.publish_prefix({'category': 'set_status', 'status': status}, 'laser_maze')

    @on_event(filter={'widget_type': 'lasers', 'action': 'set_dynamic_lasers_difficulty'})
    def laser_set_dynamic_lasers_difficulty(self, difficulty: str):
        self.publish_prefix({'category': 'set_dynamic_lasers_difficulty', 'difficulty': difficulty}, 'laser_maze')

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
    def play_sound(self, sound_id: str, localized: bool = False):
        suffix = self.get_locale_suffix() if localized else ""
        self.publish_prefix(
            {
                'category': 'play',
                'sound_id': f"{sound_id}{suffix}",
            },
            'sound_player'
        )

    @on_event(filter={'widget_id': 'check_cylinders_availability'})
    def buttons_cylinders_check_availability(self, id: str):
        self.publish_prefix({'category': 'check_availability', 'id': id}, 'cylinders')

    @on_event(filter={'widget_type': 'camera', 'action': 'restart'})
    def buttons_camera_restart(self, camera_id: str):
        self.publish_prefix({'category': 'shell', 'command': 'sudo systemctl restart gstreamer.service'}, camera_id)

    @on_event(filter={'display_multiple_ads': 'display_multiple_ads'})
    def button_set_display_multiple_ads(self, value: bool):
        self.display_multiple_ads = value
        # TODO: add interaction with control on the interface

    @on_event(filter={'action': 'ack_motors_error'})
    def waffle_factory_ack_motors_error(self):
        self.publish_prefix({'category': 'ack_motors_error'}, 'waffle_factory')

    @on_event(filter={'action': 'ack_niryo_motors_error'})
    def waffle_factory_ack_niryo_motors_error(self):
        self.publish_prefix({'category': 'ack_motors_error'}, 'niryo')

    @on_event(filter={'action': 'run_homing_and_purge'})
    def waffle_factory_run_homing_and_purge(self):
        self.publish_prefix({'category': 'printer_homing', 'purge': True}, 'waffle_factory')

    @on_event(filter={'widget_id': 'set_cursor_visibility'})
    def set_cursor_visibility(self, show: bool = False):
        xserver_command = "X -s 0 -dpms" if show else "X -s 0 -dpms -nocursor"
        self.on_shell_command(
            f"""sudo sed -E -i -e "s/^(xserver-command=).*/\\1{xserver_command}/" -- /etc/lightdm/lightdm.conf &&"""
            """sudo systemctl restart lightdm""")


class ScenarioD1(Scenario):
    def first_order_niryo_light_on(self):
        self.register_delayed_task(
            1, self.publish_prefix,
            {'category': 'light_set_freq', 'led_id': 'niryo', 'value': 49.9}, 'waffle_factory')
        self.register_delayed_task(
            1.2, self.publish_prefix,
            {'category': 'light_set_freq', 'led_id': 'niryo', 'value': 1.1}, 'waffle_factory')
        self.register_delayed_task(
            1.5, self.publish_prefix,
            {'category': 'light_set_freq', 'led_id': 'niryo', 'value': 49.9}, 'waffle_factory')
        self.register_delayed_task(
            1.7, self.publish_prefix,
            {'category': 'light_set_freq', 'led_id': 'niryo', 'value': 1.1}, 'waffle_factory')
        self.register_delayed_task(
            2, self.publish_prefix,
            {'category': 'light_set_freq', 'led_id': 'niryo', 'value': 49.9}, 'waffle_factory')
        self.register_delayed_task(
            2.2, self.publish_prefix,
            {'category': 'light_set_freq', 'led_id': 'niryo', 'value': 1.1}, 'waffle_factory')
        self.register_delayed_task(
            2.5, self.publish_prefix,
            {'category': 'light_set_freq', 'led_id': 'niryo', 'value': 49.9}, 'waffle_factory')
        self.register_delayed_task(
            2.7, self.publish_prefix,
            {'category': 'light_set_freq', 'led_id': 'niryo', 'value': 1.1}, 'waffle_factory')
        self.register_delayed_task(
            3, self.publish_prefix,
            {'category': 'light_set_freq', 'led_id': 'niryo', 'value': 49.9}, 'waffle_factory')
        self.register_delayed_task(
            3.2, self.publish_prefix,
            {'category': 'light_set_freq', 'led_id': 'niryo', 'value': 1.1}, 'waffle_factory')
        self.register_delayed_task(
            3.5, self.publish_prefix,
            {'category': 'light_set_freq', 'led_id': 'niryo', 'value': 49.9}, 'waffle_factory')
        self.register_delayed_task(
            3.7, self.publish_prefix,
            {'category': 'light_set_freq', 'led_id': 'niryo', 'value': 1.1}, 'waffle_factory')
        self.register_delayed_task(
            4, self.publish_prefix,
            {'category': 'light_set_freq', 'led_id': 'niryo', 'value': 49.9}, 'waffle_factory')
        self.register_delayed_task(
            4.2, self.publish_prefix,
            {'category': 'light_set_freq', 'led_id': 'niryo', 'value': 1.1}, 'waffle_factory')
        self.register_delayed_task(
            4.5, self.publish_prefix,
            {'category': 'light_set_freq', 'led_id': 'niryo', 'value': 49.9}, 'waffle_factory')
        self.register_delayed_task(
            4.7, self.publish_prefix,
            {'category': 'light_set_freq', 'led_id': 'niryo', 'value': 1.1}, 'waffle_factory')
        self.register_delayed_task(
            5, self.publish_prefix,
            {'category': 'light_set_freq', 'led_id': 'niryo', 'value': 49.9}, 'waffle_factory')

    def resume_order_niryo_catch_attention(self):
        self.register_delayed_task(
            0.5, self.publish_prefix,
            {'category': 'light_set_freq', 'led_id': 'niryo', 'value': 49.9}, 'waffle_factory')
        self.register_delayed_task(
            0.7, self.publish_prefix,
            {'category': 'light_set_freq', 'led_id': 'niryo', 'value': 1.1}, 'waffle_factory')
        self.register_delayed_task(
            1, self.publish_prefix,
            {'category': 'light_set_freq', 'led_id': 'niryo', 'value': 49.9}, 'waffle_factory')
        self.register_delayed_task(
            1.2, self.publish_prefix,
            {'category': 'light_set_freq', 'led_id': 'niryo', 'value': 1.1}, 'waffle_factory')
        self.register_delayed_task(
            1.5, self.publish_prefix,
            {'category': 'light_set_freq', 'led_id': 'niryo', 'value': 49.9}, 'waffle_factory')
        self.register_delayed_task(
            1.7, self.publish_prefix,
            {'category': 'light_set_freq', 'led_id': 'niryo', 'value': 1.1}, 'waffle_factory')
        self.register_delayed_task(
            2, self.publish_prefix,
            {'category': 'light_set_freq', 'led_id': 'niryo', 'value': 49.9}, 'waffle_factory')
        self.register_delayed_task(
            2.2, self.publish_prefix,
            {'category': 'light_set_freq', 'led_id': 'niryo', 'value': 1.1}, 'waffle_factory')
        self.register_delayed_task(
            2.5, self.publish_prefix,
            {'category': 'light_set_freq', 'led_id': 'niryo', 'value': 49.9}, 'waffle_factory')
        self.register_delayed_task(
            2.8, self.publish_prefix,
            {'category': 'light_set_freq', 'led_id': 'niryo', 'value': 1.1}, 'waffle_factory')
        self.register_delayed_task(
            3, self.publish_prefix,
            {'category': 'light_set_freq', 'led_id': 'niryo', 'value': 49.9}, 'waffle_factory')
        self.register_delayed_task(
            3.2, self.publish_prefix,
            {'category': 'light_set_freq', 'led_id': 'niryo', 'value': 1.1}, 'waffle_factory')
        self.register_delayed_task(
            3.5, self.publish_prefix,
            {'category': 'light_set_freq', 'led_id': 'niryo', 'value': 49.9}, 'waffle_factory')


class ScenarioD2(Scenario):
    @on_event(filter={'widget_id': 'niryo_backstage_trapdoor_open'})
    def buttons_niryo_backstage_trapdoor_open(self):
        self.publish_prefix({'category': 'low'}, 'niryo_backstage_trapdoor')
        self.register_delayed_task(1, self.publish_prefix, {'category': 'high'}, 'niryo_backstage_trapdoor')
