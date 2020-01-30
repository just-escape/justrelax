COMPONENT_TEMPLATES = [
    {
        'name': 'incoming_event',
        'context': 'trigger',
        'links': [
            {
                'type': 'text',
                'text': 'An event has been received',
            },
        ],
    },
    {
        'name': 'periodic_event',
        'context': 'trigger',
        'links': [
            {
                'type': 'text',
                'text': 'Every ',
            },
            {
                'type': 'argument',
                'key': 'period',
                'value_type': 'real',
                'default_value': '1.00',
            },
            {
                'type': 'text',
                'text': ' second(s) of session time',
            },
        ],
    },
    {
        'name': 'session_start',
        'context': 'trigger',
        'links': [
            {
                'type': 'text',
                'text': 'The session has started',
            },
        ],
    },
    {
        'name': 'session_pause',
        'context': 'trigger',
        'links': [
            {
                'type': 'text',
                'text': 'The session has paused',
            },
        ],
    },
    {
        'name': 'session_resume',
        'context': 'trigger',
        'links': [
            {
                'type': 'text',
                'text': 'The session has resumed',
            },
        ],
    },
    {
        'name': 'simple_condition',
        'context': 'condition',
        'links': [
            {
                'type': 'text',
                'text': 'If ',
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
        'name': 'send_event_simple',
        'context': 'action',
        'links': [
            {
                'type': 'text',
                'text': 'Send event ',
            },
            {
                'type': 'argument',
                'key': 'event',
                'value_type': 'string',
                'default_value': '"hello"',
            },
            {
                'type': 'text',
                'text': ' to node named ',
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
        'name': 'send_event_complex',
        'context': 'action',
        'links': [
            {
                'type': 'text',
                'text': 'Send event ',
            },
            {
                'type': 'argument',
                'key': 'event',
                'value_type': 'object',
                'default_value': '{"function": "last_created_object"}',
            },
            {
                'type': 'text',
                'text': ' to node named ',
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
        'name': 'push_notification',
        'context': 'action',
        'links': [
            {
                'type': 'text',
                'text': 'Push an ',
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
                'text': ' notification with message ',
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
        'name': 'set_variable',
        'context': 'action',
        'links': [
            {
                'type': 'text',
                'text': 'Set value of variable ',
            },
            {
                'type': 'argument',
                'key': 'variable_name',
                'value_type': 'variable',
                'default_value': 'null',
            },
            {
                'type': 'text',
                'text': ' to ',
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
        'name': 'create_a_new_object',
        'context': 'action',
        'links': [
            {
                'type': 'text',
                'text': 'Create a new object',
            },
        ],
    },
    {
        'name': 'save_object_in_object',
        'context': 'action',
        'links': [
            {
                'type': 'text',
                'text': 'Save ',
            },
            {
                'type': 'argument',
                'key': 'value',
                'value_type': 'object',
                'default_value': '{"function": "last_created_object"}',
            },
            {
                'type': 'text',
                'text': ' with key ',
            },
            {
                'type': 'argument',
                'key': 'key',
                'value_type': 'string',
                'default_value': '"key"',
            },
            {
                'type': 'text',
                'text': ' in object ',
            },
            {
                'type': 'argument',
                'key': 'object',
                'value_type': 'object',
                'default_value': '{"function": "last_created_object"}',
            }
        ],
    },
    {
        'name': 'save_string_in_object',
        'context': 'action',
        'links': [
            {
                'type': 'text',
                'text': 'Save ',
            },
            {
                'type': 'argument',
                'key': 'value',
                'value_type': 'string',
                'default_value': '"hello"',
            },
            {
                'type': 'text',
                'text': ' with key ',
            },
            {
                'type': 'argument',
                'key': 'key',
                'value_type': 'string',
                'default_value': '"key"',
            },
            {
                'type': 'text',
                'text': ' in object ',
            },
            {
                'type': 'argument',
                'key': 'object',
                'value_type': 'object',
                'default_value': '{"function": "last_created_object"}',
            }
        ],
    },
    {
        'name': 'save_integer_in_object',
        'context': 'action',
        'links': [
            {
                'type': 'text',
                'text': 'Save ',
            },
            {
                'type': 'argument',
                'key': 'value',
                'value_type': 'integer',
                'default_value': '1',
            },
            {
                'type': 'text',
                'text': ' with key ',
            },
            {
                'type': 'argument',
                'key': 'key',
                'value_type': 'string',
                'default_value': '"key"',
            },
            {
                'type': 'text',
                'text': ' in object ',
            },
            {
                'type': 'argument',
                'key': 'object',
                'value_type': 'object',
                'default_value': '{"function": "last_created_object"}',
            }
        ],
    },
    {
        'name': 'save_real_in_object',
        'context': 'action',
        'links': [
            {
                'type': 'text',
                'text': 'Save ',
            },
            {
                'type': 'argument',
                'key': 'value',
                'value_type': 'real',
                'default_value': '1.5',
            },
            {
                'type': 'text',
                'text': ' with key ',
            },
            {
                'type': 'argument',
                'key': 'key',
                'value_type': 'string',
                'default_value': '"key"',
            },
            {
                'type': 'text',
                'text': ' in object ',
            },
            {
                'type': 'argument',
                'key': 'object',
                'value_type': 'object',
                'default_value': '{"function": "last_created_object"}',
            }
        ],
    },
    {
        'name': 'save_boolean_in_object',
        'context': 'action',
        'links': [
            {
                'type': 'text',
                'text': 'Save ',
            },
            {
                'type': 'argument',
                'key': 'value',
                'value_type': 'boolean',
                'default_value': 'true',
            },
            {
                'type': 'text',
                'text': ' with key ',
            },
            {
                'type': 'argument',
                'key': 'key',
                'value_type': 'string',
                'default_value': '"key"',
            },
            {
                'type': 'text',
                'text': ' in object ',
            },
            {
                'type': 'argument',
                'key': 'object',
                'value_type': 'object',
                'default_value': '{"function": "last_created_object"}',
            }
        ],
    },
    {
        'name': 'trigger_rule',
        'context': 'action',
        'links': [
            {
                'type': 'text',
                'text': 'Trigger rule named ',
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
        'name': 'do_nothing',
        'context': 'action',
        'links': [
            {
                'type': 'text',
                'text': 'Do nothing',
            },
        ],
    },
]
