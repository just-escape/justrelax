import sqlite3

from justrelax.storage.core import Storage


class SQLite3Storage(Storage):
    DATE_MASK = '%Y-%m-%d %H:%M:%S.%U'

    def __init__(self, db_file):
        super(SQLite3Storage, self).__init__()

        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def record_new_session(self, sid, date, channel, scenario_name, room_name, n_players, **kwargs):
        query = """
            INSERT INTO session
                (id, channel, scenario, room, n_players, start_date)
            VALUES
                (?, ?, ?, ?, ?, ?)
        """
        params = (sid, channel, scenario_name, room_name, n_players, date.strftime(self.DATE_MASK),)

        self.cursor.execute(query, params)

    def record_end_of_session(self, sid, date, ticks, **kwargs):
        query = """
            UPDATE
                session
            SET
                end_date = ?,
                end_ticks = ?
            WHERE
                id = ?
        """
        params = (date.strftime(self.DATE_MASK), ticks, sid,)

        self.cursor.execute(query, params)

    def record_process_rule_actions(self, sid, date, ticks, rule_name, **kwargs):
        query = """
            INSERT INTO rule
                (session_id, name, execution_date, execution_ticks)
            VALUES
                (?, ?, ?, ?)
        """
        params = (sid, rule_name, date.strftime(self.DATE_MASK), ticks,)

        self.cursor.execute(query, params)

    def record_process_action(self, sid, date, ticks, action_name):
        query = """
            INSERT INTO action
                (session_id, name, execution_date, execution_ticks)
            VALUES
                (?, ?, ?, ?)
        """
        params = (sid, action_name, date.strftime(self.DATE_MASK), ticks,)

        self.cursor.execute(query, params)

    def record_start_alarm(self, sid, date, ticks, alarm_name, duration_ticks, **kwargs):
        query = """
            INSERT INTO alarm
                (session_id, name, duration_ticks, start_date, start_ticks, executed_actions)
            VALUES
                (?, ?, ?, ?, ?, -1)
        """
        params = (sid, alarm_name, duration_ticks, date.strftime(self.DATE_MASK), ticks,)

        self.cursor.execute(query, params)

    def record_cancel_alarm(self, sid, date, ticks, alarm_name, **kwargs):
        query = """
            UPDATE
                alarm
            SET
                cancellation_date = ?,
                cancellation_ticks = ?
            WHERE
                id = (SELECT MAX(id) FROM alarm WHERE session_id = ? AND name = ?)
        """
        params = (date.strftime(self.DATE_MASK), ticks, sid, alarm_name,)

        self.cursor.execute(query, params)

    def record_process_alarm(self, sid, alarm_name, executed_actions, **kwargs):
        query = """
            UPDATE
                alarm
            SET
                executed_actions = ?
            WHERE
                id = (SELECT MAX(id) FROM alarm WHERE session_id = ? AND name = ?)
        """
        params = (1 if executed_actions else 0, sid, alarm_name,)

        self.cursor.execute(query, params)

    def record_message(self, sid, date, ticks, direction, node_name, message, **kwargs):
        query = """
            INSERT INTO message
                (session_id, direction, node_name, message, reception_date, reception_ticks)
            VALUES
                (?, ?, ?, ?, ?, ?)
        """
        params = (sid, direction, node_name, message, date.strftime(self.DATE_MASK), ticks,)

        self.cursor.execute(query, params)

    def commit(self):
        self.connection.commit()
