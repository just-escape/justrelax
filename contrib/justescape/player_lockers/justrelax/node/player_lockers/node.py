from justrelax.core.node import MagicNode, on_event
from justrelax.core.logging_utils import logger


class ArduinoProtocol:
    CATEGORY = "c"

    READ = "r"
    TAG = "t"
    OPEN_LOCKERS = "o"
    LOCKERS_BITMASK = "b"


class PlayerLockers(MagicNode):
    def __init__(self, *args, **kwargs):
        super(PlayerLockers, self).__init__(*args, **kwargs)

        self.lockers = self.config["lockers"]

    @on_event(filter={'category': 'unlock'})
    def event_unlock(self, locker_index: int):
        logger.info("Unlocking locker index={}".format(locker_index))
        bitmask = 2 ** locker_index
        self.event_unlock_from_bitmask(bitmask)

    @on_event(filter={'category': 'unlock_from_bitmask'})
    def event_unlock_from_bitmask(self, bitmask: int):
        logger.info("Unlocking from bitmask={}".format(bitmask))
        self.send_serial({
            ArduinoProtocol.CATEGORY: ArduinoProtocol.OPEN_LOCKERS,
            ArduinoProtocol.LOCKERS_BITMASK: bitmask,
        })

    @on_event(filter={ArduinoProtocol.CATEGORY: ArduinoProtocol.READ})
    def serial_event_read(self, t):
        tag = t

        bitmask = 0

        serialized_tag = "-".join([str(byte) for byte in tag]) if tag else None
        for locker_index, locker in enumerate(self.lockers):
            for tag in locker['tags']:
                if tag == serialized_tag:
                    bitmask += 2 ** locker_index
                    logger.info("Tag {} matches one of locker {} tags".format(tag, locker_index))
                    break

        if bitmask:
            self.event_unlock_from_bitmask(bitmask)
        else:
            logger.info("Tag {} doesn't match any locker tags: ignoring".format(serialized_tag))
