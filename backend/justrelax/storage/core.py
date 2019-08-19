class Storage:
    def __init__(self, *args, **kwargs):
        pass

    def record_new_session(self, sid, date, channel, scenario_name, room_name, n_players, **kwargs):
        pass

    def record_end_of_session(self, sid, date, ticks, **kwargs):
        pass

    def record_process_rule_actions(self, sid, date, ticks, rule_name, **kwargs):
        pass

    def record_process_action(self, sid, date, ticks, action_name):
        pass

    def record_start_alarm(self, sid, date, ticks, alarm_name, duration_ticks, **kwargs):
        pass

    def record_cancel_alarm(self, sid, date, ticks, alarm_name, **kwargs):
        pass

    def record_process_alarm(self, sid, alarm_name, executed_actions, **kwargs):
        pass

    def record_message(self, sid, date, ticks, direction, node_name, message, **kwargs):
        pass

    def commit(self):
        pass
