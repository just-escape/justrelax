FUNCTIONS = [
    {
        'category': '',
        'name': 'last_created_object',
        'return_type': 'object',
        'links': [
            {
                'type': 'text',
                'text': 'Last created object',
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
                'text': 'Load value with key ',
            },
            {
                'type': 'argument',
                'key': 'key',
                'value_type': 'string',
                'default_value': '"key"',
            },
            {
                'type': 'text',
                'text': ' from ',
            },
            {
                'type': 'argument',
                'key': 'object',
                'value_type': 'object',
                'default_value': '{"function": "last_created_object"}',
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
                'text': 'Load value with key ',
            },
            {
                'type': 'argument',
                'key': 'key',
                'value_type': 'string',
                'default_value': '"key"',
            },
            {
                'type': 'text',
                'text': ' from ',
            },
            {
                'type': 'argument',
                'key': 'object',
                'value_type': 'object',
                'default_value': '{"function": "last_created_object"}',
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
                'text': 'Load value with key ',
            },
            {
                'type': 'argument',
                'key': 'key',
                'value_type': 'string',
                'default_value': '"key"',
            },
            {
                'type': 'text',
                'text': ' from ',
            },
            {
                'type': 'argument',
                'key': 'object',
                'value_type': 'object',
                'default_value': '{"function": "last_created_object"}',
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
                'text': 'Load value with key ',
            },
            {
                'type': 'argument',
                'key': 'key',
                'value_type': 'string',
                'default_value': '"key"',
            },
            {
                'type': 'text',
                'text': ' from ',
            },
            {
                'type': 'argument',
                'key': 'object',
                'value_type': 'object',
                'default_value': '{"function": "last_created_object"}',
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
                'text': 'Load value with key ',
            },
            {
                'type': 'argument',
                'key': 'key',
                'value_type': 'string',
                'default_value': '"key"',
            },
            {
                'type': 'text',
                'text': ' from ',
            },
            {
                'type': 'argument',
                'key': 'object',
                'value_type': 'object',
                'default_value': '{"function": "last_created_object"}',
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
                'text': 'Triggering node',
            },
        ],
    },
    {
        'category': '',
        'name': 'triggering_event_simple',
        'return_type': 'string',
        'links': [
            {
                'type': 'text',
                'text': 'Triggering event',
            },
        ],
    },
    {
        'category': '',
        'name': 'triggering_event_complex',
        'return_type': 'object',
        'links': [
            {
                'type': 'text',
                'text': 'Triggering event',
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
                'text': ' ',
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
                'text': ' ',
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
                'text': ' ',
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
                'text': ' ',
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
                'text': ' ',
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
                'text': ' ',
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
                'text': ' ',
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
                'text': ' ',
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
                'text': ' ',
            },
            {
                'type': 'argument',
                'key': 'operator',
                'value_type': 'predefined',
                'predefined_choices': 'is equal to,is not equal to,contains',
                'default_value': '"is equal to"',
            },
            {
                'type': 'text',
                'text': ' ',
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
                'default_value': '{"function": "last_created_object"}',
            },
            {
                'type': 'text',
                'text': ' ',
            },
            {
                'type': 'argument',
                'key': 'operator',
                'value_type': 'predefined',
                'predefined_choices': 'is equal to,is not equal to',
                'default_value': '"is equal to"',
            },
            {
                'type': 'text',
                'text': ' ',
            },
            {
                'type': 'argument',
                'key': 'right',
                'value_type': 'object',
                'default_value': '{"function": "last_created_object"}',
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
                'text': ' ',
            },
            {
                'type': 'argument',
                'key': 'operator',
                'value_type': 'predefined',
                'predefined_choices': 'is,is not',
                'default_value': '"is"',
            },
            {
                'type': 'text',
                'text': ' ',
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
        'name': 'timer_get_remaining_time',
        'return_type': 'real',
        'links': [
            {
                'type': 'text',
                'text': 'Remaining time of '
            },
            {
                'type': 'argument',
                'key': 'timer',
                'value_type': 'timer',
                'default_value': '{"function": "last_started_timer"}',
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
                'text': 'String('
            },
            {
                'type': 'argument',
                'key': 'integer',
                'value_type': 'integer',
                'default_value': '1',
            },
            {
                'type': 'text',
                'text': ')'
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
                'text': 'String('
            },
            {
                'type': 'argument',
                'key': 'real',
                'value_type': 'real',
                'default_value': '1.5',
            },
            {
                'type': 'text',
                'text': ')'
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
                'text': 'String('
            },
            {
                'type': 'argument',
                'key': 'boolean',
                'value_type': 'boolean',
                'default_value': 'True',
            },
            {
                'type': 'text',
                'text': ')'
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
                'text': 'String('
            },
            {
                'type': 'argument',
                'key': 'object',
                'value_type': 'object',
                'default_value': '{"function": "last_created_object"}',
            },
            {
                'type': 'text',
                'text': ')'
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
                'predefined_choices': 'Round,Ceil,Floor',
                'default_value': '"Round"',
            },
            {
                'type': 'text',
                'text': '('
            },
            {
                'type': 'argument',
                'key': 'integer',
                'value_type': 'integer',
                'default_value': '1.5',
            },
            {
                'type': 'text',
                'text': ')'
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
                'text': 'Real('
            },
            {
                'type': 'argument',
                'key': 'integer',
                'value_type': 'integer',
                'default_value': '1',
            },
            {
                'type': 'text',
                'text': ')'
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
                'text': 'not ',
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
                'text': ' or ',
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
                'text': ' and ',
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
                'text': 'Expiring timer',
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
                'text': 'Last started timer',
            },
        ],
    },
]
