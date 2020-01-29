import uuid
import requests
import operator

from twisted.internet.task import LoopingCall

from justrelax.common.logging_utils import logger
from justrelax.orchestrator import RULES as R


class RulesProcessor:
    def __init__(self, factory, storage_url, room_id, channel):
        self.factory = factory
        self.storage_url = storage_url
        self.room_id = room_id
        self.channel = channel

        self.ticks = 0
        self.tick_loop = LoopingCall(self.tick)

        self.rule_definitions = []
        self.on_trigger_type_rules = {
            'incoming_event': [],
            'periodic_event': [],
            'session_start': [],
            'session_pause': [],
            'session_resume': [],
        }

        self.variable_definitions = []
        self.variables = {}

        self.last_created_object = {}

        self.condition_table = {
            'simple_condition': self.condition_simple_condition,
        }

        self.action_table = {
            'send_event_simple': self.action_send_event_simple,
            'send_event_complex': self.action_send_event_complex,
            'push_notification': self.action_push_notification,
            'set_variable': self.action_set_variable,
            'create_a_new_object': self.action_create_a_new_object,
            'save_object_in_object': self.action_save_object_in_object,
            'save_string_in_object': self.action_save_string_in_object,
            'save_integer_in_object': self.action_save_integer_in_object,
            'save_real_in_object': self.action_save_real_in_object,
            'save_boolean_in_object': self.action_save_boolean_in_object,
            'trigger_rule': self.action_trigger_rule,
            'do_nothing': self.action_do_nothing,
        }

        self.function_table = {
            'last_created_object': self.function_last_created_object,
            'object_get_object': self.function_object_get_object,
            'object_get_string': self.function_object_get_string,
            'object_get_integer': self.function_object_get_integer,
            'object_get_real': self.function_object_get_real,
            'object_get_boolean': self.function_object_get_boolean,
            'triggering_node_name': self.function_triggering_node_name,
            'triggering_event_simple': self.function_triggering_event_simple,
            'triggering_event_complex': self.function_triggering_event_complex,
            'integer_arithmetic': self.function_integer_arithmetic,
            'real_arithmetic': self.function_real_arithmetic,
            'integer_comparison': self.function_integer_comparison,
            'real_comparison': self.function_real_comparison,
            'string_comparison': self.function_string_comparison,
            'object_comparison': self.function_object_comparison,
            'boolean_comparison': self.function_boolean_comparison,
            'boolean_not': self.function_boolean_not,
            'boolean_or': self.function_boolean_or,
            'boolean_and': self.function_boolean_and,
        }

        self.integer_arithmetic_operator_table = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.floordiv,
        }

        self.real_arithmetic_operator_table = {
            '+': operator.add,
            '-': operator.sub,
            '*': operator.mul,
            '/': operator.truediv,
        }

        self.sortable_comparator_table = {
            '=': operator.eq,
            '!=': operator.ne,
            '>': operator.gt,
            '>=': operator.ge,
            '<': operator.lt,
            '<=': operator.le,
        }

        self.string_comparator_table = {
            'is equal to': operator.eq,
            'is not equal to': operator.ne,
            'contains': operator.contains,
        }

        self.object_comparator_table = {
            'is equal to': operator.is_,
            'is not equal to': operator.is_not,
        }

        self.boolean_comparator_table = {
            'is': operator.is_,
            'is not': operator.is_not,
        }

        # self.system_vars = {
        #     JR.SYSTEM_VARIABLE_IS_RUNNING: self.get_is_running,
        #     JR.SYSTEM_VARIABLE_TICKS: self.get_ticks
        # }
        # self.alarm_definitions = self.rules.get(JR.ALARMS, {})
        # self.alarms = {}

        self.records = []

        self.fetch_and_init_rules()

    def is_subscribed_to_channel(self, channel):
        return self.channel == channel

    def send_event(self, to, event):
        self.factory.send_to_node(to, self.channel, event)

    def tick(self):
        self.ticks += 1
        self.factory.send_beat(self.room_id, self.ticks)
        # self.process_alarms()

    def fetch_and_init_rules(self):
        scenario_rules = requests.get(
            '{}/get_scenario/'.format(self.storage_url),
            params={'room_id': self.room_id},
        ).json()

        self.rule_definitions = scenario_rules['rules']
        self.variable_definitions = scenario_rules['variables']

        for trigger_type in self.on_trigger_type_rules:
            self.on_trigger_type_rules[trigger_type] = []

        for rule in self.rule_definitions:
            for trigger in rule['triggers']:
                if trigger['template'] in self.on_trigger_type_rules:
                    self.on_trigger_type_rules[trigger['template']].append(rule)
                else:
                    self.on_trigger_type_rules[trigger['template']] = [rule]

        self.variables = {}
        for variable in self.variable_definitions:
            if variable['list']:
                self.variables[variable['name']] = []
            else:
                self.variables[variable['name']] = variable['init_value']

    def run_room(self):
        if not self.tick_loop.running:
            if self.ticks == 0:
                self.factory.send_notification('info', "Session started")
                self.process_rules_from_trigger_type('session_start', {})
            else:
                self.factory.send_notification('info', "Session resumed")
                self.process_rules_from_trigger_type('session_resume', {})
            self.tick_loop.start(1)

    def halt_room(self):
        if self.tick_loop.running:
            self.tick_loop.stop()
            self.factory.send_notification('info', "Session paused")
            self.process_rules_from_trigger_type('session_pause', {})

    def reset_room(self):
        if not self.tick_loop.running:
            self.factory.send_reset(self.room_id)
            self.factory.send_notification('info', "Session reset")
            self.ticks = 0
            self.records = []
            self.fetch_and_init_rules()

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

    def function_last_created_object(self, *args):
        return self.last_created_object

    def function_object_get_object(self, arguments, context):
        computed_object = self.compute(arguments['object'], context)
        computed_key = self.compute(arguments['key'], context)
        return dict(computed_object[computed_key])

    def function_object_get_string(self, arguments, context):
        computed_object = self.compute(arguments['object'], context)
        computed_key = self.compute(arguments['key'], context)
        return str(computed_object[computed_key])

    def function_object_get_integer(self, arguments, context):
        computed_object = self.compute(arguments['object'], context)
        computed_key = self.compute(arguments['key'], context)
        return int(computed_object[computed_key])

    def function_object_get_real(self, arguments, context):
        computed_object = self.compute(arguments['object'], context)
        computed_key = self.compute(arguments['key'], context)
        return float(computed_object[computed_key])

    def function_object_get_boolean(self, arguments, context):
        computed_object = self.compute(arguments['object'], context)
        computed_key = self.compute(arguments['key'], context)
        return bool(computed_object[computed_key])

    @staticmethod
    def function_triggering_node_name(arguments, context):
        return context.get(R.CONTEXT_TRIGGERING_EVENT_NODE_NAME, '')

    @staticmethod
    def function_triggering_event_simple(arguments, context):
        event = context.get(R.CONTEXT_TRIGGERING_EVENT, '')
        return str(event)

    @staticmethod
    def function_triggering_event_complex(arguments, context):
        event = context.get(R.CONTEXT_TRIGGERING_EVENT, '')
        return dict(event)

    def function_integer_arithmetic(self, arguments, context):
        computed_left = self.compute(arguments['left'], context)
        operator_name = arguments['operator']
        operator_ = self.integer_arithmetic_operator_table[operator_name]
        computed_right = self.compute(arguments['right'], context)
        return operator_(computed_left, computed_right)

    def function_real_arithmetic(self, arguments, context):
        computed_left = self.compute(arguments['left'], context)
        operator_name = arguments['operator']
        operator_ = self.real_arithmetic_operator_table[operator_name]
        computed_right = self.compute(arguments['right'], context)
        return operator_(computed_left, computed_right)

    def function_integer_comparison(self, arguments, context):
        computed_left = self.compute(arguments['left'], context)
        comparator_name = arguments['operator']
        comparator = self.sortable_comparator_table[comparator_name]
        computed_right = self.compute(arguments['right'], context)
        return comparator(computed_left, computed_right)

    def function_real_comparison(self, arguments, context):
        computed_left = self.compute(arguments['left'], context)
        comparator_name = arguments['operator']
        comparator = self.sortable_comparator_table[comparator_name]
        computed_right = self.compute(arguments['right'], context)
        return comparator(computed_left, computed_right)

    def function_string_comparison(self, arguments, context):
        computed_left = self.compute(arguments['left'], context)
        comparator_name = arguments['operator']
        comparator = self.string_comparator_table[comparator_name]
        computed_right = self.compute(arguments['right'], context)
        return comparator(computed_left, computed_right)

    def function_object_comparison(self, arguments, context):
        computed_left = self.compute(arguments['left'], context)
        comparator_name = arguments['operator']
        comparator = self.object_comparator_table[comparator_name]
        computed_right = self.compute(arguments['right'], context)
        return comparator(computed_left, computed_right)

    def function_boolean_comparison(self, arguments, context):
        computed_left = self.compute(arguments['left'], context)
        comparator_name = arguments['operator']
        comparator = self.boolean_comparator_table[comparator_name]
        computed_right = self.compute(arguments['right'], context)
        return comparator(computed_left, computed_right)

    def function_boolean_not(self, arguments, context):
        computed_right = self.compute(arguments['right'], context)
        return not computed_right

    def function_boolean_or(self, arguments, context):
        computed_left = self.compute(arguments['left'], context)
        computed_right = self.compute(arguments['right'], context)
        return computed_left or computed_right

    def function_boolean_and(self, arguments, context):
        computed_left = self.compute(arguments['left'], context)
        computed_right = self.compute(arguments['right'], context)
        return computed_left and computed_right

    def compute_condition(self, condition, context):
        condition_type = condition['template']
        condition_method = self.condition_table.get(condition_type, None)

        if condition_method is None:
            raise ValueError('Unknown condition type {}'.format(condition_type))

        return condition_method(condition['arguments'], context)

    def condition_simple_condition(self, arguments, context):
        return self.compute(arguments['condition'], context)

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

    def action_send_event_simple(self, arguments, context):
        computed_to = self.compute(arguments['node_name'], context)
        computed_event = str(self.compute(arguments['event'], context))
        self.send_event(computed_to, computed_event)

    def action_send_event_complex(self, arguments, context):
        computed_to = self.compute(arguments['node_name'], context)
        computed_event = dict(self.compute(arguments['event'], context))
        self.send_event(computed_to, computed_event)

    def action_push_notification(self, arguments, context):
        notification_type = arguments['type']
        computed_message = self.compute(arguments['message'], context)
        self.factory.send_notification(notification_type, computed_message)

    def action_record(self, arguments, context):
        computed_label = self.compute(arguments['label'], context)
        id_ = str(uuid.uuid4())
        ticks = self.ticks
        self.records.append({'id': id_, 'ticks': ticks, 'label': computed_label})
        self.factory.send_record(self.room_id, id_, ticks, computed_label)

    def action_create_a_new_object(self, *args):
        self.last_created_object = {}

    def action_save_object_in_object(self, arguments, context):
        computed_object = self.compute(arguments['object'], context)
        computed_key = self.compute(arguments['key'], context)
        computed_value = self.compute(arguments['value'], context)
        computed_object[computed_key] = dict(computed_value)

    def action_save_string_in_object(self, arguments, context):
        computed_object = self.compute(arguments['object'], context)
        computed_key = self.compute(arguments['key'], context)
        computed_value = self.compute(arguments['value'], context)
        computed_object[computed_key] = str(computed_value)

    def action_save_integer_in_object(self, arguments, context):
        computed_object = self.compute(arguments['object'], context)
        computed_key = self.compute(arguments['key'], context)
        computed_value = self.compute(arguments['value'], context)
        computed_object[computed_key] = int(computed_value)

    def action_save_real_in_object(self, arguments, context):
        computed_object = self.compute(arguments['object'], context)
        computed_key = self.compute(arguments['key'], context)
        computed_value = self.compute(arguments['value'], context)
        computed_object[computed_key] = float(computed_value)

    def action_save_boolean_in_object(self, arguments, context):
        computed_object = self.compute(arguments['object'], context)
        computed_key = self.compute(arguments['key'], context)
        computed_value = self.compute(arguments['value'], context)
        computed_object[computed_key] = int(computed_value)

    def action_do_nothing(self, *args):
        pass

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
