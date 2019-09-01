import uuid
import json
from datetime import datetime

from twisted.internet.task import LoopingCall

from justrelax.common.utils import ensure_iterable
from justrelax.common.constants import JUST_SOCK_PROTOCOL as P
from justrelax.orchestrator.services import Services
from justrelax.orchestrator.constants import RULES as JR
from justrelax.orchestrator.storage.models import MessageDirections
from justrelax.orchestrator.manager.session import SessionManager


class UndefinedAction(Exception):
    pass


class RulesProcessor:
    def __init__(self, room_id, channel, rules):
        self.room_id = room_id
        self.channel = channel
        self.rules = json.loads(rules) if rules else {}

        # session_id
        self.sid = None
        self.first_start = True

        self.ticks = 0
        self.tick_loop = LoopingCall(self.tick)

        self.variable_definitions = self.rules.get(JR.VARIABLES, {})
        self.vars = {}
        self.system_vars = {
            JR.SYSTEM_VARIABLE_IS_RUNNING: self.get_is_running,
            JR.SYSTEM_VARIABLE_TICKS: self.get_ticks
        }
        self.action_definitions = self.rules.get(JR.ACTIONS, {})
        self.condition_definitions = self.rules.get(JR.CONDITIONS, {})
        self.rule_definitions = self.rules.get(JR.RULES, {})
        self.alarm_definitions = self.rules.get(JR.ALARMS, {})
        self.alarms = {}

        self.records = []

        self.start_actions = self.rules.get(JR.START_ACTIONS, {})
        self.halt_actions = self.rules.get(JR.HALT_ACTIONS, {})
        self.reset_actions = self.rules.get(JR.RESET_ACTIONS, {})

        self.sm = SessionManager()

    def get_live_data(self):
        live_data = {
            "ticks": self.ticks,
            "records": self.records,
        }
        return live_data

    def get_is_running(self):
        return self.tick_loop.running

    def get_ticks(self):
        return self.ticks

    def process_alarms(self):
        context = {}
        to_pop = []
        for alarm in self.alarms:
            context[JR.CONTEXT_ALARM_NAME] = alarm

            self.alarms[alarm]["ticks"] -= 1

            if self.alarms[alarm]["ticks"] > 0:
                continue

            to_pop.append(alarm)

            conditions = self.alarm_definitions[alarm].get(JR.CONDITIONS, [True])
            if not self.compute_value(conditions):
                if self.sid is not None:
                    self.sm.process_alarm(
                        alarm_id=self.alarms[alarm]["id"],
                        executed_actions=False,
                    )
                    self.sm.commit()
                continue

            actions = self.alarm_definitions[alarm].get(JR.ACTIONS, [])
            self.process_actions(actions)

            if self.sid is not None:
                self.sm.process_alarm(
                    alarm_id=self.alarms[alarm]["id"],
                    executed_actions=True,
                )
                self.sm.commit()

        for key in to_pop:
            self.alarms.pop(key)

    def tick(self):
        self.ticks += 1
        Services.just_sock.factory.send_beat(self.room_id, self.ticks)
        self.process_alarms()

    def run_room(self, n_players):
        if not self.tick_loop.running:
            if self.first_start:
                created_session = self.sm.create_session(
                    room_id=self.room_id,
                    n_players=n_players,
                    start_date=datetime.utcnow(),
                )
                self.sm.commit()
                self.sid = created_session.id
                self.first_start = False

                self.process_actions(self.start_actions)

            self.tick_loop.start(1)

    def halt_room(self):
        if self.tick_loop.running:
            self.tick_loop.stop()

            self.process_actions(self.halt_actions)

    def reset_room(self):
        if not self.tick_loop.running:
            self.process_actions(self.reset_actions)

            self.reset_vars(self.variable_definitions)
            self.alarms = {}
            if self.sid is not None:
                self.sm.end_session(
                    sid=self.sid,
                    date=datetime.utcnow(),
                    ticks=self.ticks,
                )
                self.sid = None
            self.first_start = True
            self.ticks = 0
            self.records = []
            Services.just_sock.factory.send_reset(self.room_id)

    def reset_vars(self, variables):
        for name, var in variables.items():
            self.vars[name] = var[JR.VARIABLE_INIT_VALUE]

    def compute_value(self, expression, context=None):
        if context is None:
            context = {}

        if not isinstance(expression, dict):
            return expression

        if JR.OBJECT in expression:
            for key, value in expression[JR.OBJECT].items():
                expression[JR.OBJECT][key] = self.compute_value(value, context=context)
            return expression[JR.OBJECT]

        if JR.CONTEXT in expression:
            key = self.compute_value(expression[JR.CONTEXT], context=context)
            return context.get(key, None)

        if JR.VARIABLE in expression:
            var = self.compute_value(expression[JR.VARIABLE], context=context)
            return self.vars[var]

        if JR.SYSTEM_VARIABLE in expression:
            sys_var = self.compute_value(expression[JR.SYSTEM_VARIABLE], context=context)
            return self.system_vars[sys_var]()

        if JR.CONDITION in expression:
            return self.process_conditions(
                self.condition_definitions[expression[JR.CONDITION]],
                context=context
            )

        if JR.OPERATION_OPERATOR in expression:
            operator = expression[JR.OPERATION_OPERATOR]
            py_operator, n_operands = JR.OPERATORS[operator]

            left = self.compute_value(
                expression.get(JR.OPERATION_LEFT, None),
                context=context
            )
            right = self.compute_value(
                expression.get(JR.OPERATION_RIGHT, None),
                context=context
            )

            if n_operands == 1:
                return py_operator(right)
            else:
                return py_operator(left, right)

        return None

    def is_subscribed_to_channel(self, channel):
        return self.channel == channel

    def process_message(self, from_, message):
        context = {
            JR.CONTEXT_FROM: from_,
            JR.CONTEXT_MESSAGE: message,
        }

        if self.sid is not None:
            self.sm.create_message(
                sid=self.sid,
                direction=MessageDirections.from_node,
                node_name=from_,
                message=message,
                date=datetime.utcnow(),
                ticks=self.ticks,
            )
            self.sm.commit()

        for rule_name, rule_definition in self.rule_definitions.items():
            context[JR.CONTEXT_RULE_NAME] = rule_name
            conditions = rule_definition.get(JR.CONDITIONS, [True])

            if not self.process_conditions(conditions, context=context):
                continue

            if self.sid is not None:
                self.sm.create_rule(
                    sid=self.sid,
                    name=rule_name,
                    date=datetime.utcnow(),
                    ticks=self.ticks,
                )
                self.sm.commit()

            actions = rule_definition.get(JR.ACTIONS, [])
            self.process_actions(actions, context=context)

    def process_conditions(self, conditions, context=None):
        res = []
        for condition in ensure_iterable(conditions):
            res.append(self.compute_value(condition, context=context))
        return all(res)

    def process_action_from_name(self, action):
        context = {
            JR.CONTEXT_FROM: P.CLIENT_ADMIN
        }

        if action not in self.action_definitions:
            raise UndefinedAction("Action '{}' is not defined".format(action))

        self._process_action_action(action, context=context)

    def process_actions(self, actions, context=None):
        if context is None:
            context = {}

        for action in ensure_iterable(actions):
            if JR.ACTION in action:
                self.process_action_action(action, context=context)

            if JR.ACTION_SEND_TO in action:
                self.process_send_action(action, context=context)

            if JR.ACTION_SET in action:
                self.process_set_action(action, context=context)

            if JR.ACTION_START_ALARM in action:
                self.process_start_alarm_action(action, context=context)

            if JR.ACTION_CANCEL_ALARM in action:
                self.process_cancel_alarm_action(action, context=context)

            if JR.ACTION_RECORD in action:
                self.process_record_action(action, context=context)

    def process_action_action(self, action, context=None):
        for action_name in ensure_iterable(action[JR.ACTION]):
            computed_name = self.compute_value(action_name, context=context)
            self._process_action_action(computed_name, context=context)

    def _process_action_action(self, action, context=None):
        defined_action = self.action_definitions[action]

        if self.sid is not None:
            self.sm.create_action(
                sid=self.sid,
                name=action,
                date=datetime.utcnow(),
                ticks=self.ticks,
            )
            self.sm.commit()

        self.process_actions(defined_action, context=context)

    def process_send_action(self, action, context=None):
        for to in ensure_iterable(action[JR.ACTION_SEND_TO]):
            computed_to = self.compute_value(to, context=context)
            for message in ensure_iterable(action[JR.ACTION_SEND_TO_MESSAGE]):
                computed_message = self.compute_value(message, context=context)
                Services.just_sock.factory.send_to_node(
                    computed_to,
                    self.channel,
                    computed_message
                )
                if self.sid is not None:
                    self.sm.create_message(
                        sid=self.sid,
                        direction=MessageDirections.to_node,
                        node_name=computed_to,
                        message=computed_message,
                        date=datetime.utcnow(),
                        ticks=self.ticks,
                    )
                    self.sm.commit()

    def process_set_action(self, action, context=None):
        value = self.compute_value(action[JR.ACTION_SET_VALUE], context=context)
        for name in ensure_iterable(action[JR.ACTION_SET_NAME]):
            computed_name = self.compute_value(name, context=context)
            self.vars[computed_name] = value

    def process_start_alarm_action(self, action, context=None):
        ticks = self.compute_value(action[JR.ACTION_START_ALARM_TICKS], context=context)
        for name in ensure_iterable(action[JR.ACTION_START_ALARM]):
            computed_name = self.compute_value(name, context=context)

            alarm = self.alarm_definitions.get(computed_name, None)
            if alarm:
                if computed_name not in self.alarms:
                    if self.sid is not None:
                        created_alarm = self.sm.create_alarm(
                            sid=self.sid,
                            name=computed_name,
                            duration=ticks,
                            start_date=datetime.utcnow(),
                            start_ticks=self.ticks,
                        )
                        self.sm.commit()
                        alarm_id = created_alarm.id
                    else:
                        alarm_id = 0

                    self.alarms[computed_name] = {
                        "id": alarm_id,
                        "ticks": ticks,
                    }

    def process_cancel_alarm_action(self, action, context=None):
        for name in ensure_iterable(action[JR.ACTION_CANCEL_ALARM]):
            computed_name = self.compute_value(name, context=context)
            alarm = self.alarms.pop(computed_name, None)
            if alarm is not None:
                if self.sid is not None:
                    self.sm.cancel_alarm(
                        alarm_id=alarm["id"],
                        cancellation_date=datetime.utcnow(),
                        cancellation_ticks=self.ticks,
                    )
                    self.sm.commit()

    def process_record_action(self, action, context=None):
        computed_label = self.compute_value(action[JR.ACTION_RECORD], context=context)
        record = {
            P.RECORD_ID: str(uuid.uuid4()),
            P.RECORD_TICKS: self.ticks,
            P.RECORD_LABEL: computed_label,
        }
        self.records.append(record)
        Services.just_sock.factory.send_record(self.room_id, record)
        if self.sid is not None:
            self.sm.create_record(
                sid=self.sid,
                label=computed_label,
                date=datetime.utcnow(),
                ticks=self.ticks,
            )
            self.sm.commit()
