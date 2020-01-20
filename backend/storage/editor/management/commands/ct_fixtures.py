COMPONENT_TEMPLATES = [
    {
        'index': 1000,
        'name': 'incoming_event',
        'context': 'trigger',
        'links': [
            {
                'index': 1,
                'type': 'text',
                'text': 'An event has been received',
            },
        ],
    },
    {
        'index': 1001,
        'name': 'session_tick',
        'context': 'trigger',
        'links': [
            {
                'index': 1,
                'type': 'text',
                'text': 'Each session tick',
            },
        ],
    },
    {
        'index': 1002,
        'name': 'session_start',
        'context': 'trigger',
        'links': [
            {
                'index': 1,
                'type': 'text',
                'text': 'The session has started',
            },
        ],
    },
    {
        'index': 1003,
        'name': 'session_pause',
        'context': 'trigger',
        'links': [
            {
                'index': 1,
                'type': 'text',
                'text': 'The session has paused',
            },
        ],
    },
    {
        'index': 1004,
        'name': 'session_resume',
        'context': 'trigger',
        'links': [
            {
                'index': 1,
                'type': 'text',
                'text': 'The session has resumed',
            },
        ],
    },
    {
        'index': 2000,
        'name': 'simple_condition',
        'context': 'condition',
        'links': [
            {
                'index': 1,
                'type': 'text',
                'text': 'If ',
            },
            {
                'index': 2,
                'type': 'argument',
                'key': 'condition',
                'default_value': True,
            },
        ],
    },
    {
        'index': 2001,
        'name': 'or',
        'context': 'condition',
        'links': [
            {
                'index': 1,
                'type': 'argument',
                'key': 'left',
                'default_value': True,
            },
            {
                'index': 2,
                'type': 'text',
                'text': ' or ',
            },
            {
                'index': 3,
                'type': 'argument',
                'key': 'right',
                'default_value': True,
            },
        ],
    },
    {
        'index': 2002,
        'name': 'and',
        'context': 'condition',
        'links': [
            {
                'index': 1,
                'type': 'argument',
                'key': 'left',
                'default_value': True,
            },
            {
                'index': 2,
                'type': 'text',
                'text': ' and ',
            },
            {
                'index': 3,
                'type': 'argument',
                'key': 'right',
                'default_value': True,
            },
        ],
    },
    {
        'index': 3000,
        'name': 'send_event',
        'context': 'action',
        'links': [
            {
                'index': 1,
                'type': 'text',
                'text': 'Send event ',
            },
            {
                'index': 2,
                'type': 'argument',
                'key': 'event',
                'default_value': 'hello',
            },
            {
                'index': 3,
                'type': 'text',
                'text': ' to node named ',
            },
            {
                'index': 4,
                'type': 'argument',
                'key': 'node_name',
                'default_value': 'node',
            },
        ],
    },
    {
        'index': 3001,
        'name': 'set_variable',
        'context': 'action',
        'links': [
            {
                'index': 1,
                'type': 'text',
                'text': 'Set variable ',
            },
            {
                'index': 2,
                'type': 'argument',
                'key': 'variable_name',
                'default_value': 'variable',
            },
            {
                'index': 3,
                'type': 'text',
                'text': ' to value ',
            },
            {
                'index': 4,
                'type': 'argument',
                'key': 'value',
                'default_value': 'value',
            },
        ],
    },
    {
        'index': 3002,
        'name': 'trigger_rule',
        'context': 'action',
        'links': [
            {
                'index': 1,
                'type': 'text',
                'text': 'Trigger rule named ',
            },
            {
                'index': 2,
                'type': 'argument',
                'key': 'rule_name',
                'default_value': 'rule',
            },
        ],
    },
]
