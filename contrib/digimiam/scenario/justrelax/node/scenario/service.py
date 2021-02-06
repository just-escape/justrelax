import time

from twisted.internet import reactor

from justrelax.common.logging_utils import logger
from justrelax.node.service import JustSockClientService, orchestrator_event


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

    def perform_task(self):
        if self.repeat:
            self.start()

        self.callback(*self.callback_args, **self.callback_kwargs)


class Scenario(JustSockClientService):
    def __init__(self, *args, **kwargs):
        super(Scenario, self).__init__(*args, **kwargs)

        self.timers = {
            'update_street_time': Timer(1, True, self.update_street_time),
            'ventilation_instruction': Timer(30, False, self.give_ventilation_instruction),
        }

        self.seconds = 0

    def update_street_time(self):
        self.seconds += 1
        self.send_event({'to': 'street_display', 'category': 'set_session_time', 'seconds': self.seconds})

    def give_ventilation_instruction(self):
        self.send_event({'to': 'orders', 'category': 'documentation_unplug_instruction', 'highlight': True})

    @orchestrator_event(filter={'from': 'orchestrator', 'category': 'start'})
    def start(self):
        self.timers['update_street_time'].start()

    @orchestrator_event(filter={'from': 'orchestrator', 'category': 'pause'})
    def pause(self):
        for timer_name, timer in self.timers.items():
            timer.session_pause()

    @orchestrator_event(filter={'from': 'orchestrator', 'category': 'resume'})
    def resume(self):
        for timer_name, timer in self.timers.items():
            timer.session_resume()

    @orchestrator_event(filter={'from': 'orchestrator', 'category': 'reset'})
    def reset(self):
        self.seconds = 0

    @orchestrator_event(filter={'from': 'street_display', 'category': 'play'})
    def street_display_event_play(self):
        def play_ms_pepper_here_you_are():
            self.send_event({'to': 'advertiser', 'category': 'play', 'video_id': 'ms_pepper_here_you_are'})
            reactor.callLater(35, after_ms_pepper_here_you_are)

        def after_ms_pepper_here_you_are():
            self.send_event({'to': 'advertiser', 'category': 'play', 'video_id': 'ads_glitch'})
            self.send_event({'to': 'music_player', 'category': 'set_volume', 'track_id': 'track1', 'volume': 70})
            self.send_event(
                {
                    'to': 'music_player', 'category': 'set_volume', 'track_id': 'track1', 'volume': 50, 'duration': 10,
                    'delay': 5
                }
            )
            self.send_event(
                {
                    'to': 'music_player', 'category': 'set_volume', 'track_id': 'track1', 'volume': 30, 'duration': 60,
                    'delay': 90
                }
            )
            self.send_event({'to': 'music_player', 'category': 'play', 'track_id': 'track1'})
            reactor.callLater(5, open_the_door)

        def open_the_door():
            self.send_event({'to': 'front_door_magnet', 'category': 'unlock'})
            self.send_event({'to': 'orchestrator', 'category': 'play'})

        play_ms_pepper_here_you_are()

    @orchestrator_event(filter={'from': 'street_display', 'category': 'unlock_front_door'})
    def street_display_event_unlock_front_door(self):
        self.send_event({'to': 'front_door_magnet', 'category': 'unlock'})

    @orchestrator_event(filter={'from': 'chopsticks', 'category': 'success'})
    def chopsticks_event_success(self):
        self.send_event({'to': 'control_panel', 'category': 'set_status', 'status': 'playing'})

    @orchestrator_event(filter={'from': 'control_panel', 'category': 'manual_mode'})
    def control_panel_event_manual_mode(self):
        self.send_event({'to': 'music_player', 'category': 'stop', 'track_id': 'track1'})
        self.send_event({'to': 'music_player', 'category': 'set_volume', 'track_id': 'track2', 'volume': 0})
        self.send_event(
            {'to': 'music_player', 'category': 'set_volume', 'track_id': 'track2', 'volume': 40, 'duration': 15})
        self.send_event({'to': 'music_player', 'category': 'play', 'track_id': 'track2', 'delay': 2})
        self.send_event({'to': 'orders', 'category': 'play_overlay_video', 'video_id': 'glitching_less'})
        self.send_event({'to': 'synchronizer', 'category': 'stop_overlay_video'})
        self.send_event({'to': 'advertiser', 'category': 'play', 'video_id': 'ads_loop'})
        self.send_event({'to': 'advertiser', 'category': 'stop', 'video_id': 'ads_glitch'})
        self.send_event({'to': 'synchronizer', 'category': 'restaurant_in_manual_mode'})
        reactor.callLater(0.2, self.send_event, {'to': 'refectory_lights', 'category': 'off', 'color': 'all'})

    @orchestrator_event(filter={'from': 'synchronizer', 'category': 'set_menu_entry'})
    def synchronizer_event_set_menu_entry(self, dish: str, index: int):
        self.send_event({'to': 'holographic_menu', 'category': 'set_slide', 'chapter_id': dish, 'slide_index': index})

    @orchestrator_event(filter={'from': 'synchronizer', 'category': 'light_service_success'})
    def synchronizer_event_light_service_success(self):
        self.send_event({'to': 'control_panel', 'category': 'set_light_service_status', 'repaired': True})

    @orchestrator_event(filter={'from': 'synchronizer', 'category': 'menu_service_success'})
    def synchronizer_event_menu_service_success(self):
        self.send_event({'to': 'control_panel', 'category': 'set_menu_service_status', 'repaired': False})

        def light_animation_step_1():
            self.send_event({'to': 'refectory_lights', 'category': 'on', 'color': 'all'})
            reactor.callLater(0.1, light_animation_step_2)

        def light_animation_step_2():
            self.send_event({'to': 'refectory_lights', 'category': 'off', 'color': 'all'})
            reactor.callLater(0.1, light_animation_step_3)

        def light_animation_step_3():
            self.send_event({'to': 'refectory_lights', 'category': 'on', 'color': 'all'})

        reactor.callLater(1.5, light_animation_step_1)

    @orchestrator_event(filter={'from': 'synchronizer', 'category': 'services_synchronization_success'})
    def synchronizer_event_services_synchronization_success(self):
        def post_delay():
            self.send_event({'to': 'orders', 'category': 'stop_overlay_video'})

        reactor.callLater(4, post_delay)

    @orchestrator_event(filter={'from': 'holographic_menu', 'category': 'play_slide'})
    def holographic_menu_event_play_slide(self, slide: int):
        self.send_event({'to': 'synchronizer', 'category': 'set_menu_cursor_position', 'position': slide})

    @orchestrator_event(filter={'from': 'load_cells', 'category': 'load_cell'})
    def load_cells_event_load_cell(self, color: str, activated: bool):
        self.send_event({'to': 'synchronizer', 'color': color, 'activated': activated})

    @orchestrator_event(filter={'from': 'synchronizer', 'category': 'on'})
    def synchronizer_event_on(self, color: str):
        self.send_event({'to': 'refectory_lights', 'category': 'on', 'color': color})

    @orchestrator_event(filter={'from': 'synchronizer', 'category': 'off'})
    def synchronizer_event_off(self, color: str):
        self.send_event({'to': 'refectory_lights', 'category': 'off', 'color': color})

    @orchestrator_event(filter={'from': 'ventilation_panel', 'category': 'game_start'})
    def ventilation_panel_event_game_start(self):
        self.timers['ventilation_instruction'].cancel()
        self.send_event({'to': 'orders', 'category': 'documentation_unplug_instruction', 'highlight': False})

    @orchestrator_event(filter={'from': 'ventilation_panel', 'category': 'start_new_round'})
    def ventilation_panel_event_start_new_round(self, round: int):
        self.send_event({'to': 'orders', 'category': 'set_ventilation_panel_round', 'round': round})

    @orchestrator_event(filter={'from': 'ventilation_panel', 'category': 'set_status'})
    def ventilation_panel_event_set_status(self, status: str):
        if status == 'playing':
            self.send_event({'to': 'orders', 'category': 'set_documentation_visibility', 'show': True})
            self.timers['ventilation_instruction'].start()
        else:
            self.send_event({'to': 'orders', 'category': 'set_documentation_visibility', 'show': False})

    @orchestrator_event(filter={'from': 'sokoban_controls', 'category': 'control'})
    def sokoban_controls_event(self, name: str, pressed: bool):
        self.send_event({'to': 'inventory', 'category': 'control', 'name': name, 'pressed': pressed})

    @orchestrator_event(filter={'from': 'secure_floor', 'category': 'clear'})
    def secure_floor_event_clear(self):
        self.send_event({'to': 'laser_maze', 'category': 'playing'})
        self.send_event({'to': 'human_authenticator', 'category': 'set_status', 'status': 'playing'})

    @orchestrator_event(filter={'from': 'laser_maze', 'category': 'alarm'})
    def laser_maze_event_alarm(self):
        self.send_event({'to': 'laser_maze', 'category': 'stop_playing'})
        self.send_event({'to': 'secure_floor', 'category': 'set_status', 'status': 'alarm'})
        self.send_event({'to': 'human_authenticator', 'category': 'set_status', 'status': 'disabled'})

    @orchestrator_event(filter={'from': 'human_authenticator', 'category': 'success'})
    def human_authenticator_event_success(self):
        self.send_event({'to': 'laser_maze', 'category': 'set_success', 'value': True})
        self.send_event({'to': 'secure_floor', 'category': 'success'})

    @orchestrator_event(filter={'from': 'root_server', 'category': 'success'})
    def root_server_event_success(self):
        def post_delay():
            self.send_event({'to': 'root_server', 'category': 'final_animation'})

        reactor.callLater(0.5, post_delay)

    @orchestrator_event(filter={'from': 'root_server', 'category': 'ms_pepper_mad_end'})
    def root_server_event_ms_pepper_mad_end(self):
        def post_delay():
            self.send_event({'to': 'synchronizer', 'category': 'display_danger_window'})
            self.send_event({'to': 'orders', 'category': 'display_danger_window'})
            self.send_event({'to': 'inventory', 'category': 'display_danger_window'})
            self.send_event({'to': 'root_server', 'category': 'display_danger_window'})

        reactor.callLater(2, post_delay)
