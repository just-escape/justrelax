import uuid
import json
import string
from random import choice
from datetime import datetime

from twisted.internet.task import LoopingCall


from justrelax.common.utils import ensure_iterable
from justrelax.constants import JSON_RULES_BUILTINS as JR
from justrelax.constants import STORAGE_RECORDS as SR
from justrelax.constants import JUST_SOCK_PROTOCOL as P


class UndefinedAction(Exception):
    pass


class RulesProcessor:
    def __init__(self, service, scenario, room, channel, rules, storage, cams):
        super(RulesProcessor, self).__init__()

        self.service = service
        self.scenario = scenario
        self.room = room
        self.channel = channel

        self.rules = self.load_rules(rules)

        # unique id of the game session
        self.session_id = self.get_new_session_id()
        self.recording_session = False
        self.first_start = True
        self.halt_date = 0

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

        self.storage = storage
        self.cams = cams

    def get_config(self):
        config = {
            "scenario": self.scenario,
            "room": self.room,
            "channel": self.channel,
            "rules": self.rules,
            "ticks": self.ticks,
            "records": self.records,
            "cams": self.cams,
        }
        return config

    @staticmethod
    def load_rules(json_rules_path):
        with open(json_rules_path, "r") as f:
            rules = json.load(f)
        return rules

    @staticmethod
    def get_new_session_id():
        chars = string.ascii_letters + string.digits
        return "".join([choice(chars) for _ in range(6)])

    def get_is_running(self):
        return self.tick_loop.running

    def get_ticks(self):
        return self.ticks

    def process_alarms(self):
        context = {}
        to_pop = []
        for alarm in self.alarms:
            context[JR.CONTEXT_ALARM_NAME] = alarm

            self.alarms[alarm] -= 1

            if self.alarms[alarm] > 0:
                continue

            to_pop.append(alarm)

            conditions = self.alarm_definitions[alarm].get(JR.CONDITIONS, [True])
            if not self.compute_value(conditions):
                self.record(SR.PROCESS_ALARM, alarm_name=alarm, executed_actions=False)
                self.storage.commit()
                continue

            actions = self.alarm_definitions[alarm].get(JR.ACTIONS, [])
            self.process_actions(actions)

            self.record(SR.PROCESS_ALARM, alarm_name=alarm, executed_actions=True)
            self.storage.commit()

        for key in to_pop:
            self.alarms.pop(key)

    def tick(self):
        self.ticks += 1
        self.service.send_beat(self.channel, self.ticks)
        self.process_alarms()

    def run_room(self):
        if not self.tick_loop.running:
            if self.first_start:
                self.record(
                    SR.NEW_SESSION,
                    channel=self.channel,
                    scenario_name=self.scenario,
                    room_name=self.room,
                    n_players="X",
                )
                self.first_start = False

                self.process_actions(self.start_actions)

            self.tick_loop.start(1)
            self.recording_session = True

    def halt_room(self):
        if self.tick_loop.running:
            self.tick_loop.stop()
            self.halt_date = datetime.utcnow()

            self.process_actions(self.halt_actions)

    def reset_room(self):
        if not self.tick_loop.running:
            self.process_actions(self.reset_actions)

            self.reset_vars(self.variable_definitions)
            self.alarms = {}
            self.record(SR.END_OF_SESSION)
            self.session_id = self.get_new_session_id()
            self.first_start = True
            self.recording_session = False
            self.ticks = 0
            self.records = []
            self.service.send_reset(self.channel)

    def reset_vars(self, variables):
        for name, var in variables.items():
            self.vars[name] = var[JR.VARIABLE_INIT_VALUE]

    def compute_value(self, expression, context=None):
        if context is None:
            context = {}

        if not isinstance(expression, dict):
            return expression

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

        self.record(
            SR.MESSAGE,
            direction=SR.DIRECTION_IN,
            node_name=from_,
            message=message
        )
        self.storage.commit()

        for rule_name, rule_definition in self.rule_definitions.items():
            context[JR.CONTEXT_RULE_NAME] = rule_name
            conditions = rule_definition.get(JR.CONDITIONS, [True])

            if not self.process_conditions(conditions, context=context):
                continue

            self.record(SR.PROCESS_RULE_ACTIONS, rule_name=rule_name)

            actions = rule_definition.get(JR.ACTIONS, [])
            self.process_actions(actions, context=context)

            self.storage.commit()

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
        self.record(SR.PROCESS_ACTION, action_name=action)
        self.process_actions(defined_action, context=context)
        self.storage.commit()

    def process_send_action(self, action, context=None):
        for to in ensure_iterable(action[JR.ACTION_SEND_TO]):
            computed_to = self.compute_value(to, context=context)
            for message in ensure_iterable(action[JR.ACTION_SEND_TO_MESSAGE]):
                computed_message = self.compute_value(message, context=context)
                self.service.send_to_node(computed_to, self.channel, computed_message)
                self.record(
                    SR.MESSAGE,
                    direction=SR.DIRECTION_OUT,
                    node_name=computed_to,
                    message=computed_message
                )
                self.storage.commit()

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
                    self.alarms[computed_name] = ticks
                    self.record(SR.START_ALARM, alarm_name=computed_name, duration_ticks=ticks)
                    self.storage.commit()

    def process_cancel_alarm_action(self, action, context=None):
        for name in ensure_iterable(action[JR.ACTION_CANCEL_ALARM]):
            computed_name = self.compute_value(name, context=context)
            remaining_ticks = self.alarms.pop(computed_name, None)
            if remaining_ticks is not None:
                self.record(SR.CANCEL_ALARM, alarm_name=computed_name)
                self.storage.commit()

    def process_record_action(self, action, context=None):
        computed_label = self.compute_value(action[JR.ACTION_RECORD], context=context)
        record = {
            P.RECORD_ID: str(uuid.uuid4()),
            P.RECORD_TICKS: self.ticks,
            P.RECORD_LABEL: computed_label,
        }
        self.records.append(record)
        self.service.send_record(self.channel, record)
        # TODO: storage

    def record(self, record_type, **kwargs):
        if self.recording_session:
            date = self.halt_date if record_type == SR.END_OF_SESSION else datetime.utcnow()
            getattr(self.storage, SR.MAPPING[record_type])(
                sid=self.session_id,
                date=date,
                ticks=self.ticks,
                **kwargs,
            )
