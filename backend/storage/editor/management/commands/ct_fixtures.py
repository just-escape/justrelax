COMPONENT_TEMPLATES = [
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
                'default_value': '{"function": "last_created_object", "arguments": {}}',
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
                'default_value': '{"function": "last_created_object", "arguments": {}}',
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
                'default_value': '{"function": "last_created_object", "arguments": {}}',
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
                'default_value': '{"function": "last_created_object", "arguments": {}}',
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
                'default_value': '{"function": "last_created_object", "arguments": {}}',
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
                'default_value': '{"function": "last_created_object", "arguments": {}}',
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
                'default_value': '{"function": "last_created_object", "arguments": {}}',
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
                'default_value': '{"function": "expiring_timer", "arguments": {}}',
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
                'default_value': '{"function": "last_started_timer", "arguments": {}}',
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
                'default_value': '{"function": "last_started_timer", "arguments": {}}',
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
                'locale': 'trigger_rule_named',
            },
            {
                'type': 'argument',
                'key': 'rule_name',
                'value_type': 'predefined',
                'default_value': 'null',
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
