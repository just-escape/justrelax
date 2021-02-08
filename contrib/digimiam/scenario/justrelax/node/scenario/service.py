import time

from twisted.internet import reactor

from justrelax.common.logging_utils import logger
from justrelax.node.service import PublishSubscribeClientService, on_event


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


class Scenario(PublishSubscribeClientService):
    def __init__(self, *args, **kwargs):
        super(Scenario, self).__init__(*args, **kwargs)

        self.dx = self.node_params['publication_channel_prefix']

        self.timers = {
            'update_street_time': Timer(1, True, self.update_street_time),
            'ventilation_instruction': Timer(30, False, self.give_ventilation_instruction),
        }

        self.seconds = 0

    def update_street_time(self):
        self.seconds += 1
        self.publish({'category': 'set_session_time', 'seconds': self.seconds}, f'{self.dx}street_display')

    def give_ventilation_instruction(self):
        self.publish({'category': 'documentation_unplug_instruction', 'highlight': True}, f'{self.dx}orders')

    @on_event(filter={'from': 'orchestrator', 'category': 'start'})
    def start(self):
        self.timers['update_street_time'].start()

    @on_event(filter={'from': 'orchestrator', 'category': 'pause'})
    def pause(self):
        for timer_name, timer in self.timers.items():
            timer.session_pause()

    @on_event(filter={'from': 'orchestrator', 'category': 'resume'})
    def resume(self):
        for timer_name, timer in self.timers.items():
            timer.session_resume()

    @on_event(filter={'from': 'orchestrator', 'category': 'reset'})
    def reset(self):
        self.seconds = 0

    @on_event(filter={'from': 'street_display', 'category': 'play'})
    def street_display_event_play(self):
        def play_ms_pepper_here_you_are():
            self.publish({'category': 'play', 'video_id': 'ms_pepper_here_you_are'}, f'{self.dx}advertiser')
            reactor.callLater(35, after_ms_pepper_here_you_are)

        def after_ms_pepper_here_you_are():
            self.publish({'category': 'play', 'video_id': 'ads_glitch'}, f'{self.dx}advertiser')
            self.publish({'category': 'set_volume', 'track_id': 'track1', 'volume': 70}, f'{self.dx}music_player')
            self.publish(
                {'category': 'set_volume', 'track_id': 'track1', 'volume': 50, 'duration': 10, 'delay': 5},
                f'{self.dx}music_player'
            )
            self.publish(
                {'category': 'set_volume', 'track_id': 'track1', 'volume': 30, 'duration': 60, 'delay': 90},
                f'{self.dx}music_player'
            )
            self.publish({'category': 'play', 'track_id': 'track1'}, f'{self.dx}music_player')
            reactor.callLater(5, open_the_door)

        def open_the_door():
            self.publish({'category': 'unlock'}, f'{self.dx}front_door_magnet')
            self.publish({'category': 'play'}, f'{self.dx}orchestrator')

        play_ms_pepper_here_you_are()

    @on_event(filter={'from': 'street_display', 'category': 'unlock_front_door'})
    def street_display_event_unlock_front_door(self):
        self.publish({'category': 'unlock'}, f'{self.dx}front_door_magnet')

    @on_event(filter={'from': 'chopsticks', 'category': 'success'})
    def chopsticks_event_success(self):
        self.publish({'category': 'set_status', 'status': 'playing'}, f'{self.dx}control_panel')

    @on_event(filter={'from': 'control_panel', 'category': 'manual_mode'})
    def control_panel_event_manual_mode(self):
        self.publish({'category': 'stop', 'track_id': 'track1'}, f'{self.dx}music_player')
        self.publish({'category': 'set_volume', 'track_id': 'track2', 'volume': 0}, f'{self.dx}music_player')
        self.publish(
            {'category': 'set_volume', 'track_id': 'track2', 'volume': 40, 'duration': 15}, f'{self.dx}music_player')
        self.publish({'category': 'play', 'track_id': 'track2', 'delay': 2}, f'{self.dx}music_player')
        self.publish({'category': 'play_overlay_video', 'video_id': 'glitching_less'}, f'{self.dx}orders')
        self.publish({'category': 'stop_overlay_video'}, f'{self.dx}synchronizer')
        self.publish({'category': 'play', 'video_id': 'ads_loop'}, f'{self.dx}advertiser')
        self.publish({'category': 'stop', 'video_id': 'ads_glitch'}, f'{self.dx}advertiser')
        self.publish({'category': 'restaurant_in_manual_mode'}, f'{self.dx}synchronizer')
        reactor.callLater(0.2, self.publish, {'to': 'refectory_lights', 'category': 'off', 'color': 'all'})

    @on_event(filter={'from': 'synchronizer', 'category': 'set_menu_entry'})
    def synchronizer_event_set_menu_entry(self, dish: str, index: int):
        self.publish({'category': 'set_slide', 'chapter_id': dish, 'slide_index': index}, f'{self.dx}holographic_menu')

    @on_event(filter={'from': 'synchronizer', 'category': 'light_service_success'})
    def synchronizer_event_light_service_success(self):
        self.publish({'category': 'set_light_service_status', 'repaired': True}, f'{self.dx}control_panel')

    @on_event(filter={'from': 'synchronizer', 'category': 'menu_service_success'})
    def synchronizer_event_menu_service_success(self):
        self.publish({'category': 'set_menu_service_status', 'repaired': False}, f'{self.dx}control_panel')

        def light_animation_step_1():
            self.publish({'category': 'on', 'color': 'all'}, f'{self.dx}refectory_lights')
            reactor.callLater(0.1, light_animation_step_2)

        def light_animation_step_2():
            self.publish({'category': 'off', 'color': 'all'}, f'{self.dx}refectory_lights')
            reactor.callLater(0.1, light_animation_step_3)

        def light_animation_step_3():
            self.publish({'category': 'on', 'color': 'all'}, f'{self.dx}refectory_lights')

        reactor.callLater(1.5, light_animation_step_1)

    @on_event(filter={'from': 'synchronizer', 'category': 'services_synchronization_success'})
    def synchronizer_event_services_synchronization_success(self):
        def post_delay():
            self.publish({'category': 'stop_overlay_video'}, f'{self.dx}orders')

        reactor.callLater(4, post_delay)

    @on_event(filter={'from': 'holographic_menu', 'category': 'play_slide'})
    def holographic_menu_event_play_slide(self, slide: int):
        self.publish({'category': 'set_menu_cursor_position', 'position': slide}, f'{self.dx}synchronizer')

    @on_event(filter={'from': 'load_cells', 'category': 'load_cell'})
    def load_cells_event_load_cell(self, color: str, activated: bool):
        self.publish({'color': color, 'activated': activated}, f'{self.dx}synchronizer')

    @on_event(filter={'from': 'synchronizer', 'category': 'on'})
    def synchronizer_event_on(self, color: str):
        self.publish({'category': 'on', 'color': color}, f'{self.dx}refectory_lights')

    @on_event(filter={'from': 'synchronizer', 'category': 'off'})
    def synchronizer_event_off(self, color: str):
        self.publish({'category': 'off', 'color': color}, f'{self.dx}refectory_lights')

    @on_event(filter={'from': 'ventilation_panel', 'category': 'game_start'})
    def ventilation_panel_event_game_start(self):
        self.timers['ventilation_instruction'].cancel()
        self.publish({'category': 'documentation_unplug_instruction', 'highlight': False}, f'{self.dx}orders')

    @on_event(filter={'from': 'ventilation_panel', 'category': 'start_new_round'})
    def ventilation_panel_event_start_new_round(self, round: int):
        self.publish({'category': 'set_ventilation_panel_round', 'round': round}, f'{self.dx}orders')

    @on_event(filter={'from': 'ventilation_panel', 'category': 'set_status'})
    def ventilation_panel_event_set_status(self, status: str):
        if status == 'playing':
            self.publish({'category': 'set_documentation_visibility', 'show': True}, f'{self.dx}orders')
            self.timers['ventilation_instruction'].start()
        else:
            self.publish({'category': 'set_documentation_visibility', 'show': False}, f'{self.dx}orders')

    @on_event(filter={'from': 'sokoban_controls', 'category': 'control'})
    def sokoban_controls_event(self, name: str, pressed: bool):
        self.publish({'category': 'control', 'name': name, 'pressed': pressed}, f'{self.dx}inventory')

    @on_event(filter={'from': 'secure_floor', 'category': 'clear'})
    def secure_floor_event_clear(self):
        self.publish({'category': 'playing'}, f'{self.dx}laser_maze')
        self.publish({'category': 'set_status', 'status': 'playing'}, f'{self.dx}human_authenticator')

    @on_event(filter={'from': 'laser_maze', 'category': 'alarm'})
    def laser_maze_event_alarm(self):
        self.publish({'category': 'stop_playing'}, f'{self.dx}laser_maze')
        self.publish({'category': 'set_status', 'status': 'alarm'}, f'{self.dx}secure_floor')
        self.publish({'category': 'set_status', 'status': 'disabled'}, f'{self.dx}human_authenticator')

    @on_event(filter={'from': 'human_authenticator', 'category': 'success'})
    def human_authenticator_event_success(self):
        self.publish({'category': 'set_success', 'value': True}, f'{self.dx}laser_maze')
        self.publish({'category': 'success'}, f'{self.dx}secure_floor')

    @on_event(filter={'from': 'root_server', 'category': 'success'})
    def root_server_event_success(self):
        def post_delay():
            self.publish({'category': 'final_animation'}, f'{self.dx}root_server')

        reactor.callLater(0.5, post_delay)

    @on_event(filter={'from': 'root_server', 'category': 'ms_pepper_mad_end'})
    def root_server_event_ms_pepper_mad_end(self):
        def post_delay():
            self.publish({'category': 'display_danger_window'}, f'{self.dx}synchronizer')
            self.publish({'category': 'display_danger_window'}, f'{self.dx}orders')
            self.publish({'category': 'display_danger_window'}, f'{self.dx}inventory')
            self.publish({'category': 'display_danger_window'}, f'{self.dx}root_server')

        reactor.callLater(2, post_delay)
