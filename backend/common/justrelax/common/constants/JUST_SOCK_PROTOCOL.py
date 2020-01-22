ROOM_ID = 'room_id'
MESSAGE_TYPE = 'message_type'
EVENT = 'event'

MESSAGE_TYPE_I_AM = 'IAM'
MESSAGE_TYPE_EVENT = 'EVENT'
MESSAGE_TYPE_TIC_TAC = 'TIC'
MESSAGE_TYPE_NOTIFICATION = 'NOTIFICATION'
MESSAGE_TYPE_RECORD = 'REC'
MESSAGE_TYPE_RESET = 'RESET'

MESSAGE_TYPE_RUN = 'RUN'
MESSAGE_TYPE_HALT = 'HALT'
MESSAGE_TYPE_SEND_EVENT_TO = 'SEND_EVENT_TO'
MESSAGE_TYPE_SEND_EVENT_AS = 'SEND_EVENT_AS'

HANDLED_ADMIN_MESSAGE_TYPES = {
    MESSAGE_TYPE_RUN,
    MESSAGE_TYPE_HALT,
    MESSAGE_TYPE_RESET,
    MESSAGE_TYPE_SEND_EVENT_TO,
    MESSAGE_TYPE_SEND_EVENT_AS,
}

I_AM_CLIENT_TYPE = 'client_type'
I_AM_NAME = 'name'
I_AM_CHANNEL = 'channel'

TIC_TAC_TICKS = 'ticks'

NOTIFICATION_TYPE = 'notification_type'
NOTIFICATION_MESSAGE = 'notification_message'

RECORD_ID = 'id'
RECORD_TICKS = 'ticks'
RECORD_LABEL = 'label'

SEND_EVENT_NODE = 'node'

CLIENT_NODE = 'node'
CLIENT_ADMIN = 'admin'
CLIENT_TYPES = {CLIENT_NODE, CLIENT_ADMIN}

SERVER = '$server'
