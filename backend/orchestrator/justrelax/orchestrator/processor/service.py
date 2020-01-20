from twisted.application.service import Service

from justrelax.orchestrator.processor.engine import RulesProcessor


class JustProcessService(Service):
    def __init__(self, rooms):
        self.processors = {}
        for room in rooms:
            self.new_processor(room.id, room.channel, room.rules)

        super(JustProcessService, self).__init__()

    def new_processor(self, room_id, channel, rules):
        processor = RulesProcessor(
            room_id=room_id,
            channel=channel,
            rules=rules,
        )
        self.processors[room_id] = processor

    def get_processor(self, room_id):
        processor = self.processors.get(room_id, None)
        if processor is None:
            raise ValueError("Room not found (room_id={})".format(room_id))
        return processor

    def process_message(self, name, channel, message):
        for _, processor in self.processors.items():
            if processor.is_subscribed_to_channel(channel):
                processor.process_message(name, message)
