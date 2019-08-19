import operator
from collections import namedtuple


START_ACTIONS = "start_actions"
HALT_ACTIONS = "halt_actions"
RESET_ACTIONS = "reset_actions"

ALARMS = "alarms"

ACTIONS = "actions"
ACTION_SEND_TO = "send_to"
ACTION_SEND_TO_MESSAGE = "message"
ACTION_SET = "set"
ACTION_SET_NAME = "name"
ACTION_SET_VALUE = "value"
ACTION_START_ALARM = "start_alarm"
ACTION_START_ALARM_TICKS = "ticks"
ACTION_CANCEL_ALARM = "cancel_alarm"
ACTION_RECORD = "record"

CONDITIONS = "conditions"

RULES = "rules"

VARIABLES = "variables"
VARIABLE_INIT_VALUE = "init_value"

OPERATION_LEFT = "left"
OPERATION_OPERATOR = "operator"
OPERATION_RIGHT = "right"

VARIABLE = "variable"

SYSTEM_VARIABLE = "system_variable"
SYSTEM_VARIABLE_IS_RUNNING = "is_running"
SYSTEM_VARIABLE_TICKS = "ticks"

CONDITION = "condition"

ACTION = "action"

CONTEXT = "context"
CONTEXT_FROM = "from"
CONTEXT_MESSAGE = "message"
CONTEXT_RULE_NAME = "rule_name"
CONTEXT_ALARM_NAME = "alarm_name"

OperatorMapping = namedtuple("OperatorMapping", ["py_operator", "n_operands"])
OPERATORS = {
    "+": OperatorMapping(operator.add, 2),
    "-": OperatorMapping(operator.sub, 2),
    "*": OperatorMapping(operator.mul, 2),
    "/": OperatorMapping(operator.truediv, 2),
    "%": OperatorMapping(operator.mod, 2),
    "not": OperatorMapping(operator.not_, 1),
    "and": OperatorMapping(operator.and_, 2),
    "or": OperatorMapping(operator.or_, 2),
    ">": OperatorMapping(operator.gt, 2),
    ">=": OperatorMapping(operator.ge, 2),
    "=": OperatorMapping(operator.eq, 2),
    "!=": OperatorMapping(operator.ne, 2),
    "<=": OperatorMapping(operator.le, 2),
    "<": OperatorMapping(operator.lt, 2),
}
