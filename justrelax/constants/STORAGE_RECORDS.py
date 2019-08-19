NEW_SESSION = "new_session"
END_OF_SESSION = "end_of_session"
PROCESS_RULE_ACTIONS = "process_rule_actions"
PROCESS_ACTION = "process_action"
START_ALARM = "start_alarm"
CANCEL_ALARM = "cancel_alarm"
PROCESS_ALARM = "process_alarm"
MESSAGE = "send_to"

DIRECTION_IN = "in"
DIRECTION_OUT = "out"

MAPPING = {
    NEW_SESSION: "record_new_session",
    END_OF_SESSION: "record_end_of_session",
    PROCESS_RULE_ACTIONS: "record_process_rule_actions",
    PROCESS_ACTION: "record_process_action",
    START_ALARM: "record_start_alarm",
    CANCEL_ALARM: "record_cancel_alarm",
    PROCESS_ALARM: "record_process_alarm",
    MESSAGE: "record_message",
}
