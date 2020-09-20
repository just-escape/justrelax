TRIGGER_TEMPLATES = [
    {
        'category': 'event',
        'name': 'incoming_event',
        'context': 'trigger',
        'links': [
            {
                'type': 'text',
                'locale': 'an_event_has_been_received',
            },
        ],
    },
    {
        'category': 'event',
        'name': 'incoming_event_from_node',
        'context': 'trigger',
        'links': [
            {
                'type': 'text',
                'locale': 'an_event_has_been_received_from_node',
            },
            {
                'type': 'argument',
                'key': 'node_name',
                'value_type': 'string',
                'default_value': '"node"',
            }
        ],
    },
    {
        'category': 'admin',
        'name': 'admin_button_press',
        'context': 'trigger',
        'links': [
            {
                'type': 'text',
                'locale': 'an_admin_button_has_been_pressed',
            },
        ],
    },
    {
        'category': 'admin',
        'name': 'admin_button_id_press',
        'context': 'trigger',
        'links': [
            {
                'type': 'text',
                'locale': 'the_admin_button',
            },
            {
                'type': 'argument',
                'key': 'button_id',
                'value_type': 'string',
                'default_value': '"id"',
            },
            {
                'type': 'text',
                'locale': 'has_been_pressed',
            }
        ],
    },
    {
        'category': 'time',
        'name': 'timed_trigger',
        'context': 'trigger',
        'links': [
            {
                'type': 'text',
                'locale': 'after',
            },
            {
                'type': 'argument',
                'key': 'session_time',
                'value_type': 'real',
                'default_value': '1.00',
            },
            {
                'type': 'text',
                'locale': 'seconds_of_session_time',
            },
        ],
    },
    {
        'category': 'time',
        'name': 'periodic_trigger',
        'context': 'trigger',
        'links': [
            {
                'type': 'text',
                'locale': 'every',
            },
            {
                'type': 'argument',
                'key': 'period',
                'value_type': 'real',
                'default_value': '1.00',
            },
            {
                'type': 'text',
                'locale': 'seconds_of_session_time',
            },
        ],
    },
    {
        'category': 'time',
        'name': 'timer_trigger',
        'context': 'trigger',
        'links': [
            {
                'type': 'argument',
                'key': 'timer',
                'value_type': 'timer',
                'default_value': 'null',
            },
            {
                'type': 'text',
                'locale': 'expires',
            },
        ],
    },
    {
        'category': 'session',
        'name': 'session_start',
        'context': 'trigger',
        'links': [
            {
                'type': 'text',
                'locale': 'the_session_is_started',
            },
        ],
    },
    {
        'category': 'session',
        'name': 'session_pause',
        'context': 'trigger',
        'links': [
            {
                'type': 'text',
                'locale': 'the_session_is_paused',
            },
        ],
    },
    {
        'category': 'session',
        'name': 'session_resume',
        'context': 'trigger',
        'links': [
            {
                'type': 'text',
                'locale': 'the_session_is_resumed',
            },
        ],
    },
    {
        'category': 'node',
        'name': 'node_connected',
        'context': 'trigger',
        'links': [
            {
                'type': 'text',
                'locale': 'a_node_has_connected',
            },
        ],
    },
    {
        'category': 'node',
        'name': 'specific_node_connected',
        'context': 'trigger',
        'links': [
            {
                'type': 'text',
                'locale': 'a_node_named_',
            },
            {
                'type': 'argument',
                'key': 'node_name',
                'value_type': 'string',
                'default_value': '\"node\"',
            },
            {
                'type': 'text',
                'locale': '_has_connected',
            },
        ],
    },
    {
        'category': 'node',
        'name': 'node_disconnected',
        'context': 'trigger',
        'links': [
            {
                'type': 'text',
                'locale': 'a_node_has_disconnected',
            },
        ],
    },
    {
        'category': 'node',
        'name': 'specific_node_disconnected',
        'context': 'trigger',
        'links': [
            {
                'type': 'text',
                'locale': 'a_node_named_',
            },
            {
                'type': 'argument',
                'key': 'node_name',
                'value_type': 'string',
                'default_value': '\"node\"',
            },
            {
                'type': 'text',
                'locale': '_has_disconnected',
            },
        ],
    },
]

CONDITION_TEMPLATES = [
    {
        'category': '',
        'name': 'simple_condition',
        'context': 'condition',
        'links': [
            {
                'type': 'text',
                'locale': 'if',
            },
            {
                'type': 'argument',
                'key': 'condition',
                'value_type': 'boolean',
                'default_value': 'true',
            },
        ],
    },
]

ACTION_TEMPLATES = [
    {
        'category': 'event',
        'name': 'send_event_string',
        'context': 'action',
        'links': [
            {
                'type': 'text',
                'locale': 'send_event',
            },
            {
                'type': 'argument',
                'key': 'event',
                'value_type': 'string',
                'default_value': '"hello"',
            },
            {
                'type': 'text',
                'locale': 'to_node',
            },
            {
                'type': 'argument',
                'key': 'node_name',
                'value_type': 'string',
                'default_value': '"node"',
            },
        ],
    },
    {
        'category': 'event',
        'name': 'send_event_object',
        'context': 'action',
        'links': [
            {
                'type': 'text',
                'locale': 'send_event',
            },
            {
                'type': 'argument',
                'key': 'event',
                'value_type': 'object',
                'default_value': '{"template": "last_created_object", "arguments": {}}',
            },
            {
                'type': 'text',
                'locale': 'to_node',
            },
            {
                'type': 'argument',
                'key': 'node_name',
                'value_type': 'string',
                'default_value': '"node"',
            },
        ],
    },
    {
        'category': 'admin',
        'name': 'push_notification',
        'context': 'action',
        'links': [
            {
                'type': 'text',
                'locale': 'push_an',
            },
            {
                'type': 'argument',
                'key': 'type',
                'value_type': 'predefined',
                'predefined_choices': 'info,error',
                'default_value': '"info"',
            },
            {
                'type': 'text',
                'locale': 'notification_on_the_admin_interface_with_message',
            },
            {
                'type': 'argument',
                'key': 'message',
                'value_type': 'string',
                'default_value': '"message"',
            },
        ],
    },
    {
        'category': 'admin',
        'name': 'add_record_now',
        'context': 'action',
        'links': [
            {
                'type': 'text',
                'locale': 'add_a_record_now_with_label',
            },
            {
                'type': 'argument',
                'key': 'label',
                'value_type': 'string',
                'default_value': '"label"',
            },
        ],
    },
    {
        'category': 'admin',
        'name': 'add_record',
        'context': 'action',
        'links': [
            {
                'type': 'text',
                'locale': 'add_a_record_at',
            },
            {
                'type': 'argument',
                'key': 'session_time',
                'value_type': 'real',
                'default_value': '0',
            },
            {
                'type': 'text',
                'locale': 'seconds_with_label',
            },
            {
                'type': 'argument',
                'key': 'label',
                'value_type': 'string',
                'default_value': '"label"',
            },
        ],
    },
    {
        'category': 'object',
        'name': 'create_a_new_object',
        'context': 'action',
        'links': [
            {
                'type': 'text',
                'locale': 'create_a_new_object',
            },
        ],
    },
    {
        'category': 'object',
        'name': 'save_object_in_object',
        'context': 'action',
        'links': [
            {
                'type': 'text',
                'locale': 'save',
            },
            {
                'type': 'argument',
                'key': 'value',
                'value_type': 'object',
                'default_value': '{"template": "last_created_object", "arguments": {}}',
            },
            {
                'type': 'text',
                'locale': 'with_key',
            },
            {
                'type': 'argument',
                'key': 'key',
                'value_type': 'string',
                'default_value': '"key"',
            },
            {
                'type': 'text',
                'locale': 'in_object',
            },
            {
                'type': 'argument',
                'key': 'object',
                'value_type': 'object',
                'default_value': '{"template": "last_created_object", "arguments": {}}',
            }
        ],
    },
    {
        'category': 'object',
        'name': 'save_string_in_object',
        'context': 'action',
        'links': [
            {
                'type': 'text',
                'locale': 'save',
            },
            {
                'type': 'argument',
                'key': 'value',
                'value_type': 'string',
                'default_value': '"hello"',
            },
            {
                'type': 'text',
                'locale': 'with_key',
            },
            {
                'type': 'argument',
                'key': 'key',
                'value_type': 'string',
                'default_value': '"key"',
            },
            {
                'type': 'text',
                'locale': 'in_object',
            },
            {
                'type': 'argument',
                'key': 'object',
                'value_type': 'object',
                'default_value': '{"template": "last_created_object", "arguments": {}}',
            }
        ],
    },
    {
        'category': 'object',
        'name': 'save_integer_in_object',
        'context': 'action',
        'links': [
            {
                'type': 'text',
                'locale': 'save',
            },
            {
                'type': 'argument',
                'key': 'value',
                'value_type': 'integer',
                'default_value': '1',
            },
            {
                'type': 'text',
                'locale': 'with_key',
            },
            {
                'type': 'argument',
                'key': 'key',
                'value_type': 'string',
                'default_value': '"key"',
            },
            {
                'type': 'text',
                'locale': 'in_object',
            },
            {
                'type': 'argument',
                'key': 'object',
                'value_type': 'object',
                'default_value': '{"template": "last_created_object", "arguments": {}}',
            }
        ],
    },
    {
        'category': 'object',
        'name': 'save_real_in_object',
        'context': 'action',
        'links': [
            {
                'type': 'text',
                'locale': 'save',
            },
            {
                'type': 'argument',
                'key': 'value',
                'value_type': 'real',
                'default_value': '1.5',
            },
            {
                'type': 'text',
                'locale': 'with_key',
            },
            {
                'type': 'argument',
                'key': 'key',
                'value_type': 'string',
                'default_value': '"key"',
            },
            {
                'type': 'text',
                'locale': 'in_object',
            },
            {
                'type': 'argument',
                'key': 'object',
                'value_type': 'object',
                'default_value': '{"template": "last_created_object", "arguments": {}}',
            }
        ],
    },
    {
        'category': 'object',
        'name': 'save_boolean_in_object',
        'context': 'action',
        'links': [
            {
                'type': 'text',
                'locale': 'save',
            },
            {
                'type': 'argument',
                'key': 'value',
                'value_type': 'boolean',
                'default_value': 'true',
            },
            {
                'type': 'text',
                'locale': 'with_key',
            },
            {
                'type': 'argument',
                'key': 'key',
                'value_type': 'string',
                'default_value': '"key"',
            },
            {
                'type': 'text',
                'locale': 'in_object',
            },
            {
                'type': 'argument',
                'key': 'object',
                'value_type': 'object',
                'default_value': '{"template": "last_created_object", "arguments": {}}',
            }
        ],
    },
    {
        'category': 'timer',
        'name': 'start_timer',
        'context': 'action',
        'links': [
            {
                'type': 'text',
                'locale': 'start_timer',
            },
            {
                'type': 'argument',
                'key': 'timer',
                'value_type': 'timer',
                'default_value': '{"template": "expiring_timer", "arguments": {}}',
            },
            {
                'type': 'text',
                'locale': 'as_a',
            },
            {
                'type': 'argument',
                'key': 'type',
                'value_type': 'predefined',
                'predefined_choices': 'one_shot,periodic',
                'default_value': '"one_shot"',
            },
            {
                'type': 'text',
                'locale': 'timer_that_will_expire_in',
            },
            {
                'type': 'argument',
                'key': 'time',
                'value_type': 'real',
                'default_value': '30.00',
            },
            {
                'type': 'text',
                'locale': 'seconds',
            },
        ],
    },
    {
        'category': 'timer',
        'name': 'pause_timer',
        'context': 'action',
        'links': [
            {
                'type': 'text',
                'locale': 'pause',
            },
            {
                'type': 'argument',
                'key': 'timer',
                'value_type': 'timer',
                'default_value': '{"template": "last_started_timer", "arguments": {}}',
            },
        ],
    },
    {
        'category': 'timer',
        'name': 'resume_timer',
        'context': 'action',
        'links': [
            {
                'type': 'text',
                'locale': 'resume',
            },
            {
                'type': 'argument',
                'key': 'timer',
                'value_type': 'timer',
                'default_value': '{"template": "last_started_timer", "arguments": {}}',
            },
        ],
    },
    {
        'category': 'game_session',
        'name': 'run_game_session',
        'context': 'action',
        'links': [
            {
                'type': 'text',
                'locale': 'run_game_session',
            },
        ],
    },
    {
        'category': 'game_session',
        'name': 'halt_game_session',
        'context': 'action',
        'links': [
            {
                'type': 'text',
                'locale': 'halt_game_session',
            },
        ],
    },
    {
        'category': 'game_session',
        'name': 'reset_game_session',
        'context': 'action',
        'links': [
            {
                'type': 'text',
                'locale': 'reset_game_session',
            },
        ],
    },
    {
        'category': '',
        'name': 'if_then_else_multiple_functions',
        'context': 'action',
        'links': [
            {
                'type': 'text',
                'locale': 'if_then_do_else_do',
            },
        ],
        'context_paragraphs': [
            {
                'type': 'condition',
                'key': 'if_conditions',
            },
            {
                'type': 'action',
                'key': 'then_actions',
            },
            {
                'type': 'action',
                'key': 'else_actions',
            },
        ],
    },
    {
        'category': '',
        'name': 'wait',
        'context': 'action',
        'links': [
            {
                'type': 'text',
                'locale': 'wait',
            },
            {
                'type': 'argument',
                'key': 'time',
                'value_type': 'real',
                'default_value': '1.5',
            },
            {
                'type': 'text',
                'locale': 'seconds',
            },
        ],
    },
    {
        'category': '',
        'name': 'set_variable',
        'context': 'action',
        'links': [
            {
                'type': 'text',
                'locale': 'set_value_of_variable',
            },
            {
                'type': 'argument',
                'key': 'variable',
                'value_type': 'variable',
                'default_value': 'null',
            },
            {
                'type': 'text',
                'locale': 'to',
            },
            {
                'type': 'argument',
                'key': 'value',
                'value_type': 'disabled',
                'default_value': 'null',
            },
        ],
    },
    {
        'category': '',
        'name': 'trigger_rule',
        'context': 'action',
        'links': [
            {
                'type': 'text',
                'locale': 'trigger_rule',
            },
            {
                'type': 'argument',
                'key': 'rule',
                'value_type': 'predefined',
                'default_value': '{\"rule\": null}',
                'predefined_choices': '<rules>',
            },
        ],
    },
    {
        'category': '',
        'name': 'do_nothing',
        'context': 'action',
        'links': [
            {
                'type': 'text',
                'locale': 'do_nothing',
            },
        ],
    },
]

OBJECT_TEMPLATES = [
    {
        'category': 'object',
        'name': 'last_created_object',
        'context': 'object',
        'links': [
            {
                'type': 'text',
                'locale': 'last_created_object',
            },
        ],
    },
    {
        'category': 'object',
        'name': 'object_get_object',
        'context': 'object',
        'links': [
            {
                'type': 'text',
                'locale': 'get_object_associated_with_key',
            },
            {
                'type': 'argument',
                'key': 'key',
                'value_type': 'string',
                'default_value': '"key"',
            },
            {
                'type': 'text',
                'locale': 'in_object',
            },
            {
                'type': 'argument',
                'key': 'object',
                'value_type': 'object',
                'default_value': '{"template": "last_created_object", "arguments": {}}',
            },
        ],
    },
    {
        'category': 'trigger',
        'name': 'triggering_event_object',
        'context': 'object',
        'links': [
            {
                'type': 'text',
                'locale': 'triggering_event_object',
            },
        ],
    },
]

STRING_TEMPLATES = [
    {
        'category': '',
        'name': 'substring',
        'context': 'string',
        'links': [
            {
                'type': 'text',
                'locale': 'all_characters_of_string_',
            },
            {
                'type': 'argument',
                'key': 'string',
                'value_type': 'string',
                'default_value': '\"hello\"',
            },
            {
                'type': 'text',
                'locale': '_between_positions_',
            },
            {
                'type': 'argument',
                'key': 'first_char',
                'value_type': 'integer',
                'default_value': '0',
            },
            {
                'type': 'text',
                'locale': '_and_',
            },
            {
                'type': 'argument',
                'key': 'last_char',
                'value_type': 'integer',
                'default_value': '3',
            },
            {
                'type': 'text',
                'locale': '_included',
            },
        ],
    },
    {
        'category': 'object',
        'name': 'object_get_string',
        'context': 'string',
        'links': [
            {
                'type': 'text',
                'locale': 'get_string_associated_with_key',
            },
            {
                'type': 'argument',
                'key': 'key',
                'value_type': 'string',
                'default_value': '"key"',
            },
            {
                'type': 'text',
                'locale': 'in_object',
            },
            {
                'type': 'argument',
                'key': 'object',
                'value_type': 'object',
                'default_value': '{"template": "last_created_object", "arguments": {}}',
            },
        ],
    },
    {
        'category': 'trigger',
        'name': 'triggering_node_name',
        'context': 'string',
        'links': [
            {
                'type': 'text',
                'locale': 'triggering_node',
            },
        ],
    },
    {
        'category': 'trigger',
        'name': 'triggering_event_string',
        'context': 'string',
        'links': [
            {
                'type': 'text',
                'locale': 'triggering_event_string',
            },
        ],
    },
    {
        'category': 'trigger',
        'name': 'triggering_admin_button_id',
        'context': 'string',
        'links': [
            {
                'type': 'text',
                'locale': 'triggering_admin_button_id',
            },
        ],
    },
    {
        'category': 'conversion',
        'name': 'real_to_string',
        'context': 'string',
        'links': [
            {
                'type': 'text',
                'locale': 'string('
            },
            {
                'type': 'argument',
                'key': 'real',
                'value_type': 'real',
                'default_value': '1.5',
            },
            {
                'type': 'text',
                'locale': ')'
            },
        ],
    },
    {
        'category': 'conversion',
        'name': 'boolean_to_string',
        'context': 'string',
        'links': [
            {
                'type': 'text',
                'locale': 'string('
            },
            {
                'type': 'argument',
                'key': 'boolean',
                'value_type': 'boolean',
                'default_value': 'true',
            },
            {
                'type': 'text',
                'locale': ')'
            },
        ],
    },
    {
        'category': 'conversion',
        'name': 'object_to_string',
        'context': 'string',
        'links': [
            {
                'type': 'text',
                'locale': 'string('
            },
            {
                'type': 'argument',
                'key': 'object',
                'value_type': 'object',
                'default_value': '{"template": "last_created_object", "arguments": {}}',
            },
            {
                'type': 'text',
                'locale': ')'
            },
        ],
    },
    {
        'category': 'conversion',
        'name': 'integer_to_string',
        'context': 'string',
        'links': [
            {
                'type': 'text',
                'locale': 'string('
            },
            {
                'type': 'argument',
                'key': 'integer',
                'value_type': 'integer',
                'default_value': '1',
            },
            {
                'type': 'text',
                'locale': ')'
            },
        ],
    },
]

INTEGER_TEMPLATES = [
    {
        'category': 'object',
        'name': 'object_get_integer',
        'context': 'integer',
        'links': [
            {
                'type': 'text',
                'locale': 'get_integer_associated_with_key',
            },
            {
                'type': 'argument',
                'key': 'key',
                'value_type': 'string',
                'default_value': '"key"',
            },
            {
                'type': 'text',
                'locale': 'in_object',
            },
            {
                'type': 'argument',
                'key': 'object',
                'value_type': 'object',
                'default_value': '{"template": "last_created_object", "arguments": {}}',
            },
        ],
    },
    {
        'category': 'math',
        'name': 'integer_arithmetic',
        'context': 'integer',
        'links': [
            {
                'type': 'argument',
                'key': 'left',
                'value_type': 'integer',
                'default_value': '1',
            },
            {
                'type': 'text',
                'locale': 'space',
            },
            {
                'type': 'argument',
                'key': 'operator',
                'value_type': 'predefined',
                'predefined_choices': '+,-,*,/',
                'default_value': '"+"',
            },
            {
                'type': 'text',
                'locale': 'space',
            },
            {
                'type': 'argument',
                'key': 'right',
                'value_type': 'integer',
                'default_value': '1',
            },
        ],
    },
    {
        'category': 'conversion',
        'name': 'real_to_integer',
        'context': 'integer',
        'links': [
            {
                'type': 'argument',
                'key': 'operation',
                'value_type': 'predefined',
                'predefined_choices': 'round,ceil,floor',
                'default_value': '"round"',
            },
            {
                'type': 'text',
                'locale': '('
            },
            {
                'type': 'argument',
                'key': 'real',
                'value_type': 'real',
                'default_value': '1.5',
            },
            {
                'type': 'text',
                'locale': ')'
            },
        ],
    },
]

REAL_TEMPLATES = [
    {
        'category': 'object',
        'name': 'object_get_real',
        'context': 'real',
        'links': [
            {
                'type': 'text',
                'locale': 'get_real_associated_with_key',
            },
            {
                'type': 'argument',
                'key': 'key',
                'value_type': 'string',
                'default_value': '"key"',
            },
            {
                'type': 'text',
                'locale': 'in_object',
            },
            {
                'type': 'argument',
                'key': 'object',
                'value_type': 'object',
                'default_value': '{"template": "last_created_object", "arguments": {}}',
            },
        ],
    },
    {
        'category': 'math',
        'name': 'real_arithmetic',
        'context': 'real',
        'links': [
            {
                'type': 'argument',
                'key': 'left',
                'value_type': 'real',
                'default_value': '1',
            },
            {
                'type': 'text',
                'locale': 'space',
            },
            {
                'type': 'argument',
                'key': 'operator',
                'value_type': 'predefined',
                'predefined_choices': '+,-,*,/',
                'default_value': '"+"',
            },
            {
                'type': 'text',
                'locale': 'space',
            },
            {
                'type': 'argument',
                'key': 'right',
                'value_type': 'real',
                'default_value': '1',
            },
        ],
    },
    {
        'category': 'conversion',
        'name': 'integer_to_real',
        'context': 'real',
        'links': [
            {
                'type': 'text',
                'locale': 'real('
            },
            {
                'type': 'argument',
                'key': 'integer',
                'value_type': 'integer',
                'default_value': '1',
            },
            {
                'type': 'text',
                'locale': ')'
            },
        ],
    },
    {
        'category': 'timer',
        'name': 'timer_remaining_time',
        'context': 'real',
        'links': [
            {
                'type': 'text',
                'locale': 'remaining_time_of'
            },
            {
                'type': 'argument',
                'key': 'timer',
                'value_type': 'timer',
                'default_value': '{"template": "last_started_timer", "arguments": {}}',
            }
        ],
    },
    {
        'category': 'game_session',
        'name': 'session_time',
        'context': 'integer',
        'links': [
            {
                'type': 'text',
                'locale': 'session_time',
            },
        ],
    },
]

BOOLEAN_TEMPLATES = [
    {
        'category': 'object',
        'name': 'object_get_boolean',
        'context': 'boolean',
        'links': [
            {
                'type': 'text',
                'locale': 'get_boolean_associated_with_key',
            },
            {
                'type': 'argument',
                'key': 'key',
                'value_type': 'string',
                'default_value': '"key"',
            },
            {
                'type': 'text',
                'locale': 'in_object',
            },
            {
                'type': 'argument',
                'key': 'object',
                'value_type': 'object',
                'default_value': '{"template": "last_created_object", "arguments": {}}',
            },
        ],
    },
    {
        'category': '',
        'name': 'boolean_not',
        'context': 'boolean',
        'links': [
            {
                'type': 'text',
                'locale': 'not',
            },
            {
                'type': 'argument',
                'key': 'right',
                'value_type': 'boolean',
                'default_value': 'true',
            },
        ],
    },
    {
        'category': '',
        'name': 'boolean_or',
        'context': 'boolean',
        'links': [
            {
                'type': 'argument',
                'key': 'left',
                'value_type': 'boolean',
                'default_value': 'true',
            },
            {
                'type': 'text',
                'locale': 'or',
            },
            {
                'type': 'argument',
                'key': 'right',
                'value_type': 'boolean',
                'default_value': 'true',
            },
        ],
    },
    {
        'category': '',
        'name': 'boolean_and',
        'context': 'boolean',
        'links': [
            {
                'type': 'argument',
                'key': 'left',
                'value_type': 'boolean',
                'default_value': 'true',
            },
            {
                'type': 'text',
                'locale': 'and',
            },
            {
                'type': 'argument',
                'key': 'right',
                'value_type': 'boolean',
                'default_value': 'true',
            },
        ],
    },
    {
        'category': '',
        'name': 'integer_comparison',
        'context': 'boolean',
        'links': [
            {
                'type': 'argument',
                'key': 'left',
                'value_type': 'integer',
                'default_value': '1',
            },
            {
                'type': 'text',
                'locale': 'space',
            },
            {
                'type': 'argument',
                'key': 'operator',
                'value_type': 'predefined',
                'predefined_choices': '=,!=,>,>=,<,<=',
                'default_value': '"="',
            },
            {
                'type': 'text',
                'locale': 'space',
            },
            {
                'type': 'argument',
                'key': 'right',
                'value_type': 'integer',
                'default_value': '1',
            },
        ],
    },
    {
        'category': '',
        'name': 'real_comparison',
        'context': 'boolean',
        'links': [
            {
                'type': 'argument',
                'key': 'left',
                'value_type': 'real',
                'default_value': '1',
            },
            {
                'type': 'text',
                'locale': 'space',
            },
            {
                'type': 'argument',
                'key': 'operator',
                'value_type': 'predefined',
                'predefined_choices': '=,!=,>,>=,<,<=',
                'default_value': '"="',
            },
            {
                'type': 'text',
                'locale': 'space',
            },
            {
                'type': 'argument',
                'key': 'right',
                'value_type': 'real',
                'default_value': '1',
            },
        ],
    },
    {
        'category': '',
        'name': 'string_comparison',
        'context': 'boolean',
        'links': [
            {
                'type': 'argument',
                'key': 'left',
                'value_type': 'string',
                'default_value': '"hello"',
            },
            {
                'type': 'text',
                'locale': 'space',
            },
            {
                'type': 'argument',
                'key': 'operator',
                'value_type': 'predefined',
                'predefined_choices': '=,!=,contains,startswith,endswith',
                'default_value': '"="',
            },
            {
                'type': 'text',
                'locale': 'space',
            },
            {
                'type': 'argument',
                'key': 'right',
                'value_type': 'string',
                'default_value': '"hello"',
            },
        ],
    },
    {
        'category': '',
        'name': 'object_comparison',
        'context': 'boolean',
        'links': [
            {
                'type': 'argument',
                'key': 'left',
                'value_type': 'object',
                'default_value': '{"template": "last_created_object", "arguments": {}}',
            },
            {
                'type': 'text',
                'locale': 'space',
            },
            {
                'type': 'argument',
                'key': 'operator',
                'value_type': 'predefined',
                'predefined_choices': 'is,is_not',
                'default_value': '"is"',
            },
            {
                'type': 'text',
                'locale': 'space',
            },
            {
                'type': 'argument',
                'key': 'right',
                'value_type': 'object',
                'default_value': '{"template": "last_created_object", "arguments": {}}',
            },
        ],
    },
    {
        'category': '',
        'name': 'boolean_comparison',
        'context': 'boolean',
        'links': [
            {
                'type': 'argument',
                'key': 'left',
                'value_type': 'boolean',
                'default_value': 'true',
            },
            {
                'type': 'text',
                'locale': 'space',
            },
            {
                'type': 'argument',
                'key': 'operator',
                'value_type': 'predefined',
                'predefined_choices': 'is,is_not',
                'default_value': '"is"',
            },
            {
                'type': 'text',
                'locale': 'space',
            },
            {
                'type': 'argument',
                'key': 'right',
                'value_type': 'boolean',
                'default_value': 'true',
            },
        ],
    },
]

TIMER_TEMPLATES = [
    {
        'category': 'timer',
        'name': 'expiring_timer',
        'context': 'timer',
        'links': [
            {
                'type': 'text',
                'locale': 'expiring_timer',
            },
        ],
    },
    {
        'category': 'timer',
        'name': 'last_started_timer',
        'context': 'timer',
        'links': [
            {
                'type': 'text',
                'locale': 'last_started_timer',
            },
        ],
    },
]

TEMPLATES = (
    TRIGGER_TEMPLATES +
    CONDITION_TEMPLATES +
    ACTION_TEMPLATES +
    OBJECT_TEMPLATES +
    STRING_TEMPLATES +
    INTEGER_TEMPLATES +
    REAL_TEMPLATES +
    BOOLEAN_TEMPLATES +
    TIMER_TEMPLATES
)
