FUNCTIONS = [
    {
        'category': '',
        'name': 'last_created_object',
        'return_type': 'object',
        'links': [
            {
                'type': 'text',
                'locale': 'last_created_object',
            },
        ],
    },
    {
        'category': '',
        'name': 'object_get_object',
        'return_type': 'object',
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
                'default_value': '{"function": "last_created_object", "arguments": {}}',
            },
        ],
    },
    {
        'category': '',
        'name': 'object_get_string',
        'return_type': 'string',
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
                'default_value': '{"function": "last_created_object", "arguments": {}}',
            },
        ],
    },
    {
        'category': '',
        'name': 'object_get_integer',
        'return_type': 'integer',
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
                'default_value': '{"function": "last_created_object", "arguments": {}}',
            },
        ],
    },
    {
        'category': '',
        'name': 'object_get_real',
        'return_type': 'real',
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
                'default_value': '{"function": "last_created_object", "arguments": {}}',
            },
        ],
    },
    {
        'category': '',
        'name': 'object_get_boolean',
        'return_type': 'boolean',
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
                'default_value': '{"function": "last_created_object", "arguments": {}}',
            },
        ],
    },
    {
        'category': '',
        'name': 'triggering_node_name',
        'return_type': 'string',
        'links': [
            {
                'type': 'text',
                'locale': 'triggering_node',
            },
        ],
    },
    {
        'category': '',
        'name': 'triggering_event_string',
        'return_type': 'string',
        'links': [
            {
                'type': 'text',
                'locale': 'triggering_event_string',
            },
        ],
    },
    {
        'category': '',
        'name': 'triggering_event_object',
        'return_type': 'object',
        'links': [
            {
                'type': 'text',
                'locale': 'triggering_event_object',
            },
        ],
    },
    {
        'category': '',
        'name': 'triggering_admin_button_id',
        'return_type': 'string',
        'links': [
            {
                'type': 'text',
                'locale': 'triggering_admin_button_id',
            },
        ],
    },
    {
        'category': '',
        'name': 'integer_arithmetic',
        'return_type': 'integer',
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
        'category': '',
        'name': 'real_arithmetic',
        'return_type': 'real',
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
        'category': '',
        'name': 'integer_comparison',
        'return_type': 'boolean',
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
        'return_type': 'boolean',
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
        'return_type': 'boolean',
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
                'predefined_choices': '=,!=,contains',
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
        'return_type': 'boolean',
        'links': [
            {
                'type': 'argument',
                'key': 'left',
                'value_type': 'object',
                'default_value': '{"function": "last_created_object", "arguments": {}}',
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
                'default_value': '{"function": "last_created_object", "arguments": {}}',
            },
        ],
    },
    {
        'category': '',
        'name': 'boolean_comparison',
        'return_type': 'boolean',
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
    {
        'category': '',
        'name': 'timer_remaining_time',
        'return_type': 'real',
        'links': [
            {
                'type': 'text',
                'locale': 'remaining_time_of'
            },
            {
                'type': 'argument',
                'key': 'timer',
                'value_type': 'timer',
                'default_value': '{"function": "last_started_timer", "arguments": {}}',
            }
        ],
    },
    {
        'category': '',
        'name': 'integer_to_string',
        'return_type': 'string',
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
    {
        'category': '',
        'name': 'real_to_string',
        'return_type': 'string',
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
        'category': '',
        'name': 'boolean_to_string',
        'return_type': 'string',
        'links': [
            {
                'type': 'text',
                'locale': 'string('
            },
            {
                'type': 'argument',
                'key': 'boolean',
                'value_type': 'boolean',
                'default_value': 'True',
            },
            {
                'type': 'text',
                'locale': ')'
            },
        ],
    },
    {
        'category': '',
        'name': 'object_to_string',
        'return_type': 'string',
        'links': [
            {
                'type': 'text',
                'locale': 'string('
            },
            {
                'type': 'argument',
                'key': 'object',
                'value_type': 'object',
                'default_value': '{"function": "last_created_object", "arguments": {}}',
            },
            {
                'type': 'text',
                'locale': ')'
            },
        ],
    },
    {
        'category': '',
        'name': 'real_to_integer',
        'return_type': 'integer',
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
                'key': 'integer',
                'value_type': 'integer',
                'default_value': '1.5',
            },
            {
                'type': 'text',
                'locale': ')'
            },
        ],
    },
    {
        'category': '',
        'name': 'integer_to_real',
        'return_type': 'real',
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
        'category': '',
        'name': 'boolean_not',
        'return_type': 'boolean',
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
        'return_type': 'boolean',
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
        'return_type': 'boolean',
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
        'name': 'expiring_timer',
        'return_type': 'timer',
        'links': [
            {
                'type': 'text',
                'locale': 'expiring_timer',
            },
        ],
    },
    {
        'category': '',
        'name': 'last_started_timer',
        'return_type': 'timer',
        'links': [
            {
                'type': 'text',
                'locale': 'last_started_timer',
            },
        ],
    },
]
