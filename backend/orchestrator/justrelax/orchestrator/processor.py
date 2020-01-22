import uuid

from twisted.internet.task import LoopingCall

from justrelax.common.logging_utils import logger
from justrelax.orchestrator import RULES as R


class RulesProcessor:
    def __init__(self, factory, room_id, channel, rules, variables):
        self.factory = factory
        self.room_id = room_id
        self.channel = channel

        self.ticks = 0
        self.tick_loop = LoopingCall(self.tick)

        self.rule_definitions = rules
        self.on_trigger_type_rules = {
            'incoming_event': [],
            'session_start': [],
            'session_pause': [],
            'session_resume': [],
        }
        self.init_rules()

        self.variable_definitions = variables
        self.variables = {}
        self.init_variables()

        self.condition_table = {
            'simple_condition': self.condition_simple_condition,
            'or': self.condition_or,
            'and': self.condition_and,
        }

        self.action_table = {
            'trigger_rule': self.action_trigger_rule,
            'set_variable': self.action_set_variable,
            'send_event': self.action_send_event,
            'push_info_notification': self.action_push_info_notification,
            'push_error_notification': self.action_push_error_notification,
        }

        self.function_table = {
            '+': self.function_addition,
            '-': self.function_substraction,
            '*': self.function_multiplication,
            '/': self.function_division,
        }

        # self.system_vars = {
        #     JR.SYSTEM_VARIABLE_IS_RUNNING: self.get_is_running,
        #     JR.SYSTEM_VARIABLE_TICKS: self.get_ticks
        # }
        # self.alarm_definitions = self.rules.get(JR.ALARMS, {})
        # self.alarms = {}

        self.records = []

    def is_subscribed_to_channel(self, channel):
        return self.channel == channel

    def send_event(self, to, event):
        self.factory.send_to_node(to, self.channel, event)

    def tick(self):
        self.ticks += 1
        self.factory.send_beat(self.room_id, self.ticks)
        # self.process_alarms()

    def init_rules(self):
        for rule in self.rule_definitions:
            for trigger in rule['triggers']:
                if trigger['template'] in self.on_trigger_type_rules:
                    self.on_trigger_type_rules[trigger['template']].append(rule)
                else:
                    self.on_trigger_type_rules[trigger['template']] = [rule]

    def init_variables(self):
        for variable in self.variables:
            if variable['list']:
                self.variables[variable['name']] = []
            else:
                self.variables[variable['name']] = variable['default_value']

    def run_room(self):
        if not self.tick_loop.running:
            self.tick_loop.start(1)
            if self.ticks == 0:
                self.factory.send_notification('info', "Session started")
                self.process_rules_from_trigger_type('session_start', {})
            else:
                self.factory.send_notification('info', "Session resumed")
                self.process_rules_from_trigger_type('session_resume', {})

    def halt_room(self):
        if self.tick_loop.running:
            self.tick_loop.stop()
            self.factory.send_notification('info', "Session paused")
            self.process_rules_from_trigger_type('session_halt', {})

    def reset_room(self):
        if not self.tick_loop.running:
            self.init_variables()
            self.ticks = 0
            self.records = []
            self.factory.send_reset(self.room_id)
            self.factory.send_notification('info', "Session reset")

    def on_event(self, from_, event):
        context = {
            R.CONTEXT_TRIGGERING_EVENT_NODE_NAME: from_,
            R.CONTEXT_TRIGGERING_EVENT: event,
        }

        self.process_rules_from_trigger_type('incoming_event', context)

    def process_rules_from_trigger_type(self, trigger_type, context):
        for rule in self.on_trigger_type_rules[trigger_type]:
            try:
                self.if_conditions_then_actions(
                    rule['conditions'], rule['actions'], context)
            except Exception:
                message = "Error while processing rule {}".format(rule['name'])
                self.factory.send_notification('error', message)
                logger.exception()

    def if_conditions_then_actions(self, conditions, actions, context):
        if all([self.compute_condition(c, context) for c in conditions]):
            for action in actions:
                self.process_action(action, context)

    def compute(self, value, context):
        if not isinstance(value, dict):
            return value

        if "object" in value:
            for key, value in value["object"].items():
                value["object"][key] = self.compute(value, context)
            return value["object"]

        if "variable" in value:
            variable_name = value["variable"]
            return self.variables[variable_name]

        if "function" in value:
            function = self.function_table.get(value["function"], None)
            if function is None:
                raise ValueError('Unknown function {}'.format(value["function"]))
            return function(value["arguments"], context)

        return None

    def function_addition(self, arguments, context):
        computed_left = self.compute(arguments['left'], context)
        computed_right = self.compute(arguments['right'], context)
        return computed_left + computed_right

    def function_substraction(self, arguments, context):
        computed_left = self.compute(arguments['left'], context)
        computed_right = self.compute(arguments['right'], context)
        return computed_left - computed_right

    def function_multiplication(self, arguments, context):
        computed_left = self.compute(arguments['left'], context)
        computed_right = self.compute(arguments['right'], context)
        return computed_left * computed_right

    def function_division(self, arguments, context):
        computed_left = self.compute(arguments['left'], context)
        computed_right = self.compute(arguments['right'], context)
        return computed_left / computed_right

    def compute_condition(self, condition, context):
        condition_type = condition['template']
        condition_method = self.condition_table.get(condition_type, None)

        if condition_method is None:
            raise ValueError('Unknown condition type {}'.format(condition_type))

        return condition_method(condition['arguments'], context)

    def condition_simple_condition(self, arguments, context):
        return self.compute(arguments['condition'], context)

    def condition_or(self, arguments, context):
        return self.compute(arguments['left'], context) or self.compute(arguments['right'], context)

    def condition_and(self, arguments, context):
        return self.compute(arguments['left'], context) and self.compute(arguments['right'], context)

    def process_action(self, action, context):
        action_type = action['template']
        action_method = self.action_table.get(action_type, None)

        if action_method is None:
            raise ValueError('Unknown action type {}'.format(action_type))

        return action_method(action['arguments'], context)

    def action_trigger_rule(self, arguments, context):
        computed_rule_name = self.compute(arguments['rule_name'], context)
        for rule in self.rule_definitions:
            if rule['name'] == computed_rule_name:
                conditions = rule['conditions']
                actions = rule['actions']
                self.if_conditions_then_actions(conditions, actions, context)
                break

    def action_set_variable(self, arguments, context):
        computed_variable_name = self.compute(arguments['variable_name'], context)
        computed_value = self.compute(arguments['value'], context)

        self.variables[computed_variable_name] = computed_value

    def action_send_event(self, arguments, context):
        computed_to = self.compute(arguments['node_name'], context)
        computed_event = self.compute(arguments['event'], context)
        self.send_event(computed_to, computed_event)

    def action_push_info_notification(self, arguments, context):
        computed_message = self.compute(arguments['message'], context)
        self.factory.send_notification('info', computed_message)

    def action_push_error_notification(self, arguments, context):
        computed_message = self.compute(arguments['message'], context)
        self.factory.send_notification('error', computed_message)

    def action_record(self, arguments, context):
        computed_label = self.compute(arguments['label'], context)
        id_ = str(uuid.uuid4())
        ticks = self.ticks
        self.records.append({'id': id_, 'ticks': ticks, 'label': computed_label})
        self.factory.send_record(self.room_id, id_, ticks, computed_label)

    # def process_alarms(self):
    #     context = {}
    #     to_pop = []
    #     for alarm in self.alarms:
    #         context[JR.CONTEXT_ALARM_NAME] = alarm
    #
    #         self.alarms[alarm]["ticks"] -= 1
    #
    #         if self.alarms[alarm]["ticks"] > 0:
    #             continue
    #
    #         to_pop.append(alarm)
    #
    #         conditions = self.alarm_definitions[alarm].get(JR.CONDITIONS, [True])
    #         self.compute_value(conditions)
    #
    #         actions = self.alarm_definitions[alarm].get(JR.ACTIONS, [])
    #         self.process_actions(actions)
    #
    #     for key in to_pop:
    #         self.alarms.pop(key)
    # def process_start_alarm_action(self, action, context=None):
    #     ticks = self.compute_value(action[JR.ACTION_START_ALARM_TICKS], context=context)
    #     for name in ensure_iterable(action[JR.ACTION_START_ALARM]):
    #         computed_name = self.compute_value(name, context=context)
    #
    #         alarm = self.alarm_definitions.get(computed_name, None)
    #         if alarm:
    #             if computed_name not in self.alarms:
    #                 alarm_id = 0
    #
    #                 self.alarms[computed_name] = {
    #                     "id": alarm_id,
    #                     "ticks": ticks,
    #                 }
    #
    # def process_cancel_alarm_action(self, action, context=None):
    #     for name in ensure_iterable(action[JR.ACTION_CANCEL_ALARM]):
    #         computed_name = self.compute_value(name, context=context)
    #         alarm = self.alarms.pop(computed_name, None)
