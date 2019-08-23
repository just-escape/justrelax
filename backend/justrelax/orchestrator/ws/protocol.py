import json

from autobahn.twisted.websocket import WebSocketServerProtocol

from justrelax.common.logging import logger
from justrelax.common.constants import JUST_SOCK_PROTOCOL as P
from justrelax.common.validation import validate_node_name, validate_channel


class JustSockServerProtocol(WebSocketServerProtocol):
    def __init__(self):
        super(JustSockServerProtocol, self).__init__()
        self.name = None
        self.channel = None
        self.client_type = None

    def onConnect(self, request):
        logger.info("Node connecting: {}".format(request.peer))

    def onOpen(self):
        logger.info("Node connected: {}".format(self.peer))

    def connectionLost(self, reason):
        if self.client_type == P.CLIENT_ADMIN:
            identifier = self.name
            self.factory.unregister_admin(self)
        elif self.client_type == P.CLIENT_NODE:
            identifier = "{}@{}".format(self.name, self.channel)
            self.factory.unregister_node(self)
        else:
            identifier = self.peer

        logger.info("Lost connection with {}".format(identifier))

    def onMessage(self, payload, isBinary):
        if isBinary:
            logger.warning("Binary message received ({} bytes): ignoring".format(len(payload)))
            return

        try:
            unicode_event = payload.decode('utf8')
        except UnicodeDecodeError:
            logger.exception("Cannot load {}: ignoring".format(payload))
            return

        try:
            event_dict = json.loads(unicode_event)
        except json.JSONDecodeError:
            logger.exception("Cannot load {}: ignoring".format(unicode_event))
            return

        ok, warning = self.validate_event(event_dict)
        if not ok:
            logger.info("Received {}".format(event_dict))
            logger.warning(warning)
            logger.info("Ignoring")
        else:
            logger.debug("Received {}".format(event_dict))

            self.log_event(event_dict, to_server=True)

            if self.client_type == P.CLIENT_NODE:
                # event_dict[P.EVENT_TYPE] is P.EVENT_TYPE_MESSAGE thanks to
                # validate_event
                message = event_dict[P.EVENT_CONTENT]

                self.factory.process_message(self.name, self.channel, message)
            elif self.client_type == P.CLIENT_ADMIN:
                logger.warning("$admin messages not handled: ignoring")

            else:
                self.process_i_am_event(event_dict)

    def validate_event(self, event):
        try:
            event_type = event[P.EVENT_TYPE]
        except KeyError:
            return False, "Event has no type"

        try:
            content = event[P.EVENT_CONTENT]
        except KeyError:
            return False, "Event has no content"

        if not self.client_type:
            if event_type != P.EVENT_TYPE_I_AM:
                return False, "Client type is not yet declared"

            if type(content) != dict:
                return False, "Expecting a dict content"

            if P.I_AM_CLIENT_TYPE not in content:
                return False, "Missing client type argument"

            if content[P.I_AM_CLIENT_TYPE] not in P.CLIENT_TYPES:
                return False, "Unknown client type"

            if content[P.I_AM_CLIENT_TYPE] == P.CLIENT_NODE:
                if P.I_AM_NAME not in content:
                    return False, "Missing name argument"

                if not validate_node_name(content[P.I_AM_NAME]):
                    return False, "Name must be alphanumeric"

                if P.I_AM_CHANNEL not in content:
                    return False, "Missing channel argument"

                if not validate_channel(content[P.I_AM_CHANNEL]):
                    return False, "Channel must be alphanumeric"
        else:
            if event_type != P.EVENT_TYPE_MESSAGE:
                return False, "Expecting a message event"

        return True, None

    def log_event(self, event, to_server=True):
        if not self.client_type:
            identifier = self.peer
        else:
            if self.client_type == P.CLIENT_ADMIN:
                at = "<room id={}>".format(event[P.EVENT_ROOM_ID])
            else:
                at = self.channel

            identifier = "{}@{}".format(self.name, at)

        if to_server:
            from_ = identifier
            to = "$server"
        else:
            from_ = "$server"
            to = identifier

        type_ = event[P.EVENT_TYPE]

        content = event.get(P.EVENT_CONTENT, "")

        logger.info("[{} > {}] {} {}".format(from_, to, type_, content))

    def process_i_am_event(self, event):
        # P.CLIENT_NODE or P.CLIENT_ADMIN, thanks to validate_event
        self.client_type = event[P.EVENT_CONTENT][P.I_AM_CLIENT_TYPE]

        if event[P.EVENT_CONTENT][P.I_AM_CLIENT_TYPE] == P.CLIENT_NODE:
            self.name = event[P.EVENT_CONTENT][P.I_AM_NAME]
            self.channel = event[P.EVENT_CONTENT][P.I_AM_CHANNEL]
            self.factory.register_node(self)
        else:
            self.name = P.CLIENT_ADMIN
            self.factory.register_admin(self)

    def send_message(self, message):
        event = {
            P.EVENT_TYPE: P.EVENT_TYPE_MESSAGE,
            P.EVENT_CONTENT: message,
        }
        self.send_json(event)

    def send_beat(self, room_id, ticks):
        event = {
            P.EVENT_ROOM_ID: room_id,
            P.EVENT_TYPE: P.EVENT_TYPE_TIC_TAC,
            P.EVENT_CONTENT: ticks
        }
        self.send_json(event)

    def send_record(self, room_id, record):
        event = {
            P.EVENT_ROOM_ID: room_id,
            P.EVENT_TYPE: P.EVENT_TYPE_RECORD,
            P.EVENT_CONTENT: record,
        }
        self.send_json(event)

    def send_reset(self, room_id):
        event = {
            P.EVENT_ROOM_ID: room_id,
            P.EVENT_TYPE: P.EVENT_TYPE_RESET,
        }
        self.send_json(event)

    def send_json(self, dict_):
        unicode_json = json.dumps(dict_, ensure_ascii=False)
        bytes_ = unicode_json.encode("utf8")

        logger.debug("Sending {}".format(dict_))
        self.log_event(dict_, to_server=False)
        self.sendMessage(bytes_)
