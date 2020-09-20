import uuid
import math
import requests
import operator
import time

from twisted.internet import reactor
from twisted.internet.defer import Deferred, inlineCallbacks

from justrelax.common.logging_utils import logger
from justrelax.orchestrator import RULES as R

STATE_NOT_STARTED = 'not_started'
STATE_TICKING = 'ticking'
STATE_PAUSED = 'paused'


class Timer:
    def __init__(self, processor, time, repeat=False, callback=None, *args, **kwargs):
        self.processor = processor
        self.time = time
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
        if self.processor.state == STATE_TICKING:
            self.compute_and_schedule()

    def compute_and_schedule(self):
        now = time.monotonic()
        try:
            computed_time = self.processor.compute(self.time, {})
        except Exception:
            message = "Error while computing {}".format(self.time)
            self.processor.factory.send_notification('error', message)
            logger.exception()
        else:
            self.last_computed_delay = computed_time
            self.last_schedule_timestamp = now
            self.task = reactor.callLater(computed_time, self.perform_task)

    def pause(self):
        if self.task and self.task.active() and self.processor.state == STATE_TICKING:
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

    def resume(self):
        if self.task and not self.task.active() and not self.manual_pause and self.processor.state == STATE_TICKING:
            now = time.monotonic()
            self.last_schedule_timestamp = now
            self.task = reactor.callLater(
                self.last_computed_delay, self.perform_task)

    def cancel(self):
        if self.task and self.task.active():
            self.task.cancel()

    def perform_task(self):
        if self.repeat:
            self.compute_and_schedule()
        else:
            self.processor.dereference_timer(self)
        self.callback(*self.callback_args, **self.callback_kwargs)


class SessionTimer:
    def __init__(self, processor):
        self.processor = processor

        self.tic_tac_period = 1  # seconds

        self.state = STATE_NOT_STARTED
        self.session_time = 0.

        self.task = None
        self.last_computed_delay = 0.
        self.last_schedule_timestamp = 0.

    def start(self):
        if self.state == STATE_NOT_STARTED:
            self.last_schedule_timestamp = time.monotonic()
            self.schedule_next_tic_tac()
            self.state = STATE_TICKING

    def schedule_next_tic_tac(self):
        now = time.monotonic()
        delta_since_last_schedule = now - self.last_schedule_timestamp
        self.last_schedule_timestamp = now

        self.session_time += delta_since_last_schedule
        delay_before_next_call = self.tic_tac_period - self.session_time % self.tic_tac_period
        self.task = reactor.callLater(delay_before_next_call, self.tic_tac)

    def pause(self):
        if self.state == STATE_TICKING:
            delta_since_last_schedule = time.monotonic() - self.last_schedule_timestamp
            self.last_computed_delay = self.tic_tac_period - delta_since_last_schedule
            self.session_time += delta_since_last_schedule
            self.task.cancel()
            self.state = STATE_PAUSED

    def resume(self):
        if self.state == STATE_PAUSED:
            now = time.monotonic()
            self.last_schedule_timestamp = now
            self.task = reactor.callLater(self.last_computed_delay, self.tic_tac)
            self.state = STATE_TICKING

    def cancel(self):
        if self.state == STATE_PAUSED:
            self.session_time = 0.
            self.state = STATE_NOT_STARTED

    def tic_tac(self):
        self.schedule_next_tic_tac()
        self.processor.tic_tac()


class RulesProcessor:
    def __init__(self, factory, storage_url, room_id, channel):
        self.factory = factory
        self.storage_url = storage_url
        self.room_id = room_id
        self.channel = channel

        self.session_timer = SessionTimer(self)

        self.rule_definitions = []
        self.on_trigger_type_rules = {
            'incoming_event': [],
            'incoming_event_from_node': [],
            'node_connection': [],
            'specific_node_connection': [],
            'node_disconnection': [],
            'specific_node_disconnection': [],
            'admin_button_press': [],
            'admin_button_id_press': [],
            'session_start': [],
            'session_pause': [],
            'session_resume': [],
        }

        self.timers = set()

        self.variables = {}

        self.last_created_object = {}
        # The variable name or None is no timer was ever started
        self.last_started_timer = None

        self.condition_table = {
            'simple_condition': self.condition_simple_condition,
        }

        self.action_table = {
            'send_event_string': self.action_send_event_string,
            'send_event_object': self.action_send_event_object,
            'push_notification': self.action_push_notification,
            'add_record_now': self.action_add_record_now,
            'add_record': self.action_add_record,
            'set_variable': self.action_set_variable,
            'create_a_new_object': self.action_create_a_new_object,
            'save_object_in_object': self.action_save_object_in_object,
            'save_string_in_object': self.action_save_string_in_object,
            'save_integer_in_object': self.action_save_integer_in_object,
            'save_real_in_object': self.action_save_real_in_object,
            'save_boolean_in_object': self.action_save_boolean_in_object,
            'trigger_rule': self.action_trigger_rule,
            'start_timer': self.action_start_timer,
            'pause_timer': self.action_pause_timer,
            'resume_timer': self.action_resume_timer,
            'run_game_session': self.action_run_game_session,
            'halt_game_session': self.action_halt_game_session,
            'reset_game_session': self.action_reset_game_session,
            'if_then_else_multiple_functions': self.action_if_then_else_multiple_functions,
            'wait': self.action_wait,
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
            'triggering_event_string': self.function_triggering_event_string,
            'triggering_event_object': self.function_triggering_event_object,
            'triggering_admin_button_id': self.function_triggering_admin_button_id,
            'substring': self.function_substring,
            'integer_arithmetic': self.function_integer_arithmetic,
            'real_arithmetic': self.function_real_arithmetic,
            'integer_comparison': self.function_integer_comparison,
            'real_comparison': self.function_real_comparison,
            'string_comparison': self.function_string_comparison,
            'object_comparison': self.function_object_comparison,
            'boolean_comparison': self.function_boolean_comparison,
            'timer_remaining_time': self.function_timer_remaining_time,
            'session_time': self.function_session_time,
            'integer_to_string': self.function_integer_to_string,
            'real_to_string': self.function_real_to_string,
            'boolean_to_string': self.function_boolean_to_string,
            'object_to_string': self.function_object_to_string,
            'real_to_integer': self.function_real_to_integer,
            'integer_to_real': self.function_integer_to_real,
            'boolean_not': self.function_boolean_not,
            'boolean_or': self.function_boolean_or,
            'boolean_and': self.function_boolean_and,
            'expiring_timer': self.function_expiring_timer,
            'last_started_timer': self.function_last_started_timer,
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

        self.object_comparator_table = {
            'is': operator.is_,
            'is_not': operator.is_not,
        }

        self.boolean_comparator_table = {
            'is': operator.is_,
            'is_not': operator.is_not,
        }

        self.records = []

        self.fetch_and_init_rules()

    @property
    def state(self):
        return self.session_timer.state

    def is_subscribed_to_channel(self, channel):
        return self.channel == channel

    def send_event(self, to, event):
        self.factory.send_to_node(to, self.channel, event)

    def fetch_and_init_rules(self):
        scenario_rules = requests.get(
            '{}/get_scenario/'.format(self.storage_url),
            params={'room_id': self.room_id},
        ).json()

        self.rule_definitions = scenario_rules['rules']

        for trigger_type in self.on_trigger_type_rules:
            self.on_trigger_type_rules[trigger_type] = []
        self.timers = set()

        self.variables = {}
        variable_definitions = scenario_rules['variables']
        for variable in variable_definitions:
            if variable['type'] == 'timer':
                context = {R.CONTEXT_EXPIRING_TIMER: variable['name']}
                init_value = Timer(
                    self,
                    0, False,
                    self.process_rules, [], context,
                )
            else:
                init_value = variable['init_value']
            self.variables[variable['name']] = init_value

        for rule in self.rule_definitions:
            for trigger in rule['content']['triggers']:
                if trigger['template'] in self.on_trigger_type_rules:
                    self.on_trigger_type_rules[trigger['template']].append(
                        {
                            "trigger": trigger,
                            "rule": rule,
                        }
                    )
                elif trigger['template'] == 'timed_trigger':
                    self.timers.add(
                        Timer(
                            self,
                            trigger['arguments']['session_time'], False,
                            self.process_rule, rule, {},
                        )
                    )
                elif trigger['template'] == 'periodic_trigger':
                    self.timers.add(
                        Timer(
                            self,
                            trigger['arguments']['period'], True,
                            self.process_rule, rule, {},
                        )
                    )
                elif trigger['template'] == 'timer_trigger':
                    variable_timer_name = trigger['arguments']['timer']['variable']
                    self.variables[variable_timer_name].callback_args[0].append(
                        {
                            "trigger": {},
                            "rule": rule,
                        }
                    )
                else:
                    logger.warning("Unknown trigger type {}: skipping".format(trigger['template']))

    def run_room(self):
        if self.session_timer.state == STATE_NOT_STARTED:
            self.process_rules(self.on_trigger_type_rules['session_start'], {})
            self.session_timer.start()
            self.schedule_timers()
            self.factory.send_notification('info', "Session started")
        elif self.session_timer.state == STATE_PAUSED:
            self.process_rules(self.on_trigger_type_rules['session_resume'], {})
            self.session_timer.resume()
            self.resume_timers()
            self.factory.send_notification('info', "Session resumed")

    def halt_room(self):
        if self.session_timer.state == STATE_TICKING:
            self.process_rules(self.on_trigger_type_rules['session_pause'], {})
            self.pause_timers()
            self.session_timer.pause()
            self.factory.send_notification('info', "Session paused")

    def reset_room(self):
        if self.session_timer.state == STATE_PAUSED:
            self.factory.send_reset(self.room_id)
            self.cancel_timers()
            self.session_timer.cancel()
            self.records = []
            self.fetch_and_init_rules()
            self.factory.send_notification('info', "Session reset")

    def on_node_connection(self, node_name):
        context = {
            R.CONTEXT_TRIGGERING_NODE_NAME: node_name,
        }

        self.process_rules(self.on_trigger_type_rules['node_connection'], context)

        for rule in self.on_trigger_type_rules['specific_node_connection']:
            computed_triggering_node_name = self.compute(
                rule['trigger']['arguments']['node_name'], context)
            if computed_triggering_node_name == node_name:
                self.process_rule(rule['rule'], context)

    def on_node_disconnection(self, node_name):
        context = {
            R.CONTEXT_TRIGGERING_NODE_NAME: node_name,
        }

        self.process_rules(self.on_trigger_type_rules['node_disconnection'], context)

        for rule in self.on_trigger_type_rules['specific_node_disconnection']:
            computed_triggering_node_name = self.compute(
                rule['trigger']['arguments']['node_name'], context)
            if computed_triggering_node_name == node_name:
                self.process_rule(rule['rule'], context)

    def on_event(self, from_, event):
        context = {
            R.CONTEXT_TRIGGERING_NODE_NAME: from_,
            R.CONTEXT_TRIGGERING_EVENT: event,
        }

        self.process_rules(self.on_trigger_type_rules['incoming_event'], context)

        for rule in self.on_trigger_type_rules['incoming_event_from_node']:
            computed_triggering_node_name = self.compute(
                rule['trigger']['arguments']['node_name'], context)
            if computed_triggering_node_name == from_:
                self.process_rule(rule['rule'], context)

    def on_admin_button_pressed(self, button_id):
        context = {
            R.CONTEXT_TRIGGERING_ADMIN_BUTTON_ID: button_id,
        }

        self.process_rules(self.on_trigger_type_rules['admin_button_press'], context)

        for rule in self.on_trigger_type_rules['admin_button_id_press']:
            computed_triggering_button_id = self.compute(
                rule['trigger']['arguments']['button_id'], context)
            if computed_triggering_button_id == button_id:
                self.process_rule(rule['rule'], context)

    def process_rules(self, rules, context):
        for rule in rules:
            self.process_rule(rule['rule'], context)

    def process_rule(self, rule, context):
        try:
            self.if_conditions_then_actions(
                rule['content']['conditions'], rule['content']['actions'], context)
        except Exception:
            message = "Error while processing rule {}".format(rule['name'])
            self.factory.send_notification('error', message)
            logger.exception()

    @inlineCallbacks
    def if_conditions_then_actions(self, conditions, actions, context):
        if all([self.compute_condition(c, context) for c in conditions]):
            for action in actions:
                yield self.process_action(action, context)

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

        if "template" in value:
            function = self.function_table.get(value["template"], None)
            if function is None:
                raise ValueError('Unknown function {}'.format(value["template"]))
            return function(value["arguments"], context)

        if "rule" in value:
            for rule in self.rule_definitions:
                if rule['id'] == value["rule"]:
                    return rule
            else:
                raise ValueError('Rule id={} not found'.format(value["rule"]))

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
        return context.get(R.CONTEXT_TRIGGERING_NODE_NAME, '')

    @staticmethod
    def function_triggering_event_string(arguments, context):
        event = context.get(R.CONTEXT_TRIGGERING_EVENT, '')
        return str(event)

    @staticmethod
    def function_triggering_event_object(arguments, context):
        event = context.get(R.CONTEXT_TRIGGERING_EVENT, '')
        return dict(event)

    @staticmethod
    def function_triggering_admin_button_id(arguments, context):
        admin_button_id = context.get(R.CONTEXT_TRIGGERING_ADMIN_BUTTON_ID, '')
        return admin_button_id

    def function_substring(self, arguments, context):
        computed_string = self.compute(arguments['string'], context)
        computed_first_char = self.compute(arguments['first_char'], context)
        computed_last_char = self.compute(arguments['last_char'], context)

        # +1 on last char because it is more intuitive by default
        # "abc"[0:0] returns ""
        # "abc"[0:0+1] returns "a"
        substring = computed_string[computed_first_char:computed_last_char+1]

        return substring

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
        computed_right = self.compute(arguments['right'], context)

        if comparator_name == '=':
            return computed_left == computed_right
        elif comparator_name == '!=':
            return computed_left != computed_right
        elif comparator_name == 'contains':
            return computed_right in computed_left
        elif comparator_name == 'startswith':
            return computed_left.startswith(computed_right)
        elif comparator_name == 'endswith':
            return computed_left.endswith(computed_right)
        else:
            return False

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

    def function_timer_remaining_time(self, arguments, context):
        timer = self.compute(arguments['timer'], context)
        return timer.get_remaining_time() if timer else 0.

    def function_session_time(self, arguments, context):
        return int(self.session_timer.session_time)

    def function_integer_to_string(self, arguments, context):
        integer = self.compute(arguments['integer'], context)
        return str(integer)

    def function_real_to_string(self, arguments, context):
        real = self.compute(arguments['real'], context)
        return str(real)

    def function_boolean_to_string(self, arguments, context):
        boolean = self.compute(arguments['boolean'], context)
        return str(boolean)

    def function_object_to_string(self, arguments, context):
        object_ = self.compute(arguments['object'], context)
        return str(object_)

    def function_real_to_integer(self, arguments, context):
        real = self.compute(arguments['real'], context)
        operation = arguments['operation']
        if operation == 'ceil':
            return math.ceil(real)
        elif operation == 'floor':
            return math.floor(real)
        else:
            return round(real)

    def function_integer_to_real(self, arguments, context):
        integer = self.compute(arguments['integer'], context)
        return float(integer)

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

    @staticmethod
    def function_expiring_timer(arguments, context):
        return context.get(R.CONTEXT_EXPIRING_TIMER, None)

    def function_last_started_timer(self, *args):
        return self.last_started_timer

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

        arguments = action['arguments']
        paragraphs = action.get('paragraphs', {})

        return action_method(arguments, paragraphs, context)

    def action_run_game_session(self, arguments, paragraphs, context):
        self.run_room()

    def action_halt_game_session(self, arguments, paragraphs, context):
        self.halt_room()

    def action_reset_game_session(self, arguments, paragraphs, context):
        self.reset_room()

    def action_trigger_rule(self, arguments, paragraphs, context):
        computed_rule = self.compute(arguments['rule'], context)

        conditions = computed_rule['content']['conditions']
        actions = computed_rule['content']['actions']
        self.if_conditions_then_actions(conditions, actions, context)

    def action_set_variable(self, arguments, paragraphs, context):
        variable_name = arguments['variable']['variable']
        if type(self.variables[variable_name]) is Timer:
            logger.warning("set_variable action is not supported for timer variables")
            return
        computed_value = self.compute(arguments['value'], context)

        self.variables[variable_name] = computed_value

    def action_send_event_string(self, arguments, paragraphs, context):
        computed_to = self.compute(arguments['node_name'], context)
        computed_event = str(self.compute(arguments['event'], context))
        self.send_event(computed_to, computed_event)

    def action_send_event_object(self, arguments, paragraphs, context):
        computed_to = self.compute(arguments['node_name'], context)
        computed_event = dict(self.compute(arguments['event'], context))
        self.send_event(computed_to, computed_event)

    def action_push_notification(self, arguments, paragraphs, context):
        notification_type = arguments['type']
        computed_message = self.compute(arguments['message'], context)
        self.factory.send_notification(notification_type, computed_message)

    def action_add_record_now(self, arguments, paragraphs, context):
        computed_label = self.compute(arguments['label'], context)
        session_time = self.session_timer.session_time
        self.record(session_time, computed_label)

    def action_add_record(self, arguments, paragraphs, context):
        computed_label = self.compute(arguments['label'], context)
        computed_session_time = self.compute(arguments['session_time'], context)
        self.record(computed_session_time, computed_label)

    def record(self, session_time, label):
        id_ = str(uuid.uuid4())
        self.records.append({'id': id_, 'session_time': session_time, 'label': label})
        self.factory.send_record(self.room_id, id_, session_time, label)

    def action_create_a_new_object(self, *args):
        self.last_created_object = {}

    def action_save_object_in_object(self, arguments, paragraphs, context):
        computed_object = self.compute(arguments['object'], context)
        computed_key = self.compute(arguments['key'], context)
        computed_value = self.compute(arguments['value'], context)
        computed_object[computed_key] = dict(computed_value)

    def action_save_string_in_object(self, arguments, paragraphs, context):
        computed_object = self.compute(arguments['object'], context)
        computed_key = self.compute(arguments['key'], context)
        computed_value = self.compute(arguments['value'], context)
        computed_object[computed_key] = str(computed_value)

    def action_save_integer_in_object(self, arguments, paragraphs, context):
        computed_object = self.compute(arguments['object'], context)
        computed_key = self.compute(arguments['key'], context)
        computed_value = self.compute(arguments['value'], context)
        computed_object[computed_key] = int(computed_value)

    def action_save_real_in_object(self, arguments, paragraphs, context):
        computed_object = self.compute(arguments['object'], context)
        computed_key = self.compute(arguments['key'], context)
        computed_value = self.compute(arguments['value'], context)
        computed_object[computed_key] = float(computed_value)

    def action_save_boolean_in_object(self, arguments, paragraphs, context):
        computed_object = self.compute(arguments['object'], context)
        computed_key = self.compute(arguments['key'], context)
        computed_value = self.compute(arguments['value'], context)
        computed_object[computed_key] = bool(computed_value)

    def action_start_timer(self, arguments, paragraphs, context):
        timer = self.compute(arguments['timer'], context)
        if timer:
            repeat = True if arguments['type'] == 'periodic' else False
            time_ = arguments['time']

            if timer in self.timers:
                timer.cancel()

            timer.repeat = repeat
            timer.time = time_
            timer.manual_pause = False
            self.timers.add(timer)
            self.last_started_timer = timer

            timer.start()

    def action_pause_timer(self, arguments, paragraphs, context):
        timer = self.compute(arguments['timer'], context)
        if timer:
            timer.manual_pause = True
            timer.pause()

    def action_resume_timer(self, arguments, paragraphs, context):
        timer = self.compute(arguments['timer'], context)
        if timer:
            timer.manual_pause = False
            timer.resume()

    @inlineCallbacks
    def action_if_then_else_multiple_functions(self, arguments, paragraphs, context):
        conditions = paragraphs['if_conditions']
        if all([self.compute_condition(c, context) for c in conditions]):
            actions = paragraphs['then_actions']
        else:
            actions = paragraphs['else_actions']

        for action in actions:
            yield self.process_action(action, context)

    def action_wait(self, arguments, paragraphs, context):
        time_ = self.compute(arguments['time'], context)

        d = Deferred()
        timer = Timer(self, time_, False, d.callback, None)
        self.timers.add(timer)
        timer.start()

        return d

    def action_do_nothing(self, *args):
        pass

    def tic_tac(self):
        self.factory.send_tic_tac(self.room_id, self.session_timer.session_time)

    def schedule_timers(self):
        for timer in self.timers:
            timer.start()

    def resume_timers(self):
        for timer in self.timers:
            timer.resume()

    def pause_timers(self):
        for timer in self.timers:
            timer.pause()

    def cancel_timers(self):
        for timer in self.timers:
            timer.cancel()

    def dereference_timer(self, timer):
        self.timers.remove(timer)
