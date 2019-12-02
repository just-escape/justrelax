from justrelax.orchestrator.manager.core import Manager
from justrelax.orchestrator.storage.models import Session
from justrelax.orchestrator.storage.models import Rule, Action, Alarm, Message, Record


class SessionManager(Manager):
    def create_session(self, room_id, n_players, start_date):
        s = Session(
            room_id=room_id,
            n_players=n_players,
            start_date=start_date,
        )
        self.session.add(s)
        return s

    def end_session(self, sid, date, ticks):
        updates = {
            "end_date": date,
            "end_ticks": ticks,
        }
        return self.session.query(Session).filter_by(id=sid).update(updates)

    def create_rule(self, sid, name, date, ticks):
        r = Rule(
            session_id=sid,
            name=name,
            execution_date=date,
            execution_ticks=ticks,
        )
        self.session.add(r)
        return r

    def create_action(self, sid, name, date, ticks):
        a = Action(
            session_id=sid,
            name=name,
            execution_date=date,
            execution_ticks=ticks,
        )
        self.session.add(a)
        return a

    def create_alarm(self, sid, name, duration, start_date, start_ticks):
        a = Alarm(
            session_id=sid,
            name=name,
            duration_ticks=duration,
            start_date=start_date,
            start_ticks=start_ticks,
        )
        self.session.add(a)
        return a

    def cancel_alarm(self, alarm_id, cancellation_date, cancellation_ticks):
        updates = {
            "cancellation_date": cancellation_date,
            "cancellation_ticks": cancellation_ticks,
        }
        return self.session.query(Alarm).filter_by(id=alarm_id).update(updates)

    def process_alarm(self, alarm_id, executed_actions):
        updates = {
            "executed_actions": executed_actions,
        }
        return self.session.query(Alarm).filter_by(id=alarm_id).update(updates)

    def create_message(self, sid, direction, node_name, message, date, ticks):
        m = Message(
            session_id=sid,
            direction=direction,
            node_name=node_name,
            message=message,
            date=date,
            ticks=ticks,
        )
        self.session.add(m)
        return m

    def create_record(self, sid, label, date, ticks):
        r = Record(
            session_id=sid,
            label=label,
            date=date,
            ticks=ticks,
        )
        self.session.add(r)
        return r
