import vlc

from twisted.internet import reactor

from justrelax.common.logging_utils import logger
from justrelax.node.service import JustSockNodeClientService


class HologramPlayer(JustSockNodeClientService):
    class COMMANDS:
        COMMAND_TYPE = "type"
        SELECT = "select"
        CHAPTER_ID = "chapter_id"

    def start(self):
        self.looping_task = None

        self.chapters = {}
        for chapter in self.node_params['chapters']:
            self.chapters[chapter['id']] = {
                'start': chapter['start'],
                'loop_a': chapter['loop_a'],
                'loop_b': chapter['loop_b'],
            }

        self.player = vlc.MediaPlayer(self.service_params['video_path'])
        self.player.set_fullscreen(True)

        if 'default_chapter' in self.service_params:
            self.lock_chapter(self.service_params['default_chapter'])

    def process_message(self, message):
        logger.debug("Processing message '{}'".format(message))
        if type(message) is not dict:
            logger.debug("Unknown message: skipping")
            return

        if self.COMMANDS.COMMAND_TYPE not in message:
            logger.debug("Message has no command type: skipping")
            return

        if message[self.COMMANDS.COMMAND_TYPE] == self.COMMANDS.SELECT:
            if self.COMMANDS.CHAPTER_ID not in message:
                logger.debug("Select command has no chapter id: skipping")
                return

            self.lock_chapter(message[self.COMMANDS.CHAPTER_ID])
        else:
            logger.debug("Unknown command type '{}': skipping".format(
                message[self.COMMANDS.COMMAND_TYPE]))

    def lock_chapter(self, chapter_id):
        logger.info("Locking on chapter id={}".format(chapter_id))

        chapter = self.chapters.get(chapter_id, None)
        if chapter is None:
            logger.error("Unknown chapter id={}: aborting".format(chapter_id))
            return

        if self.looping_task is not None:
            self.looping_task.cancel()

        self.player.set_time(int(self.chapters[chapter_id]['start'] * 1000))
        self.player.play()
        reactor.callLater(self.chapters[chapter_id]['loop_b'], self.loop_chapter, chapter_id)

    def loop_chapter(self, chapter_id):
        self.media_player.set_time(int(self.chapters[chapter_id]['loop_a'] * 1000))
        time_before_loop = self.chapters[chapter_id]['loop_b'] - self.chapters[chapter_id]['loop_a']
        reactor.callLater(time_before_loop, self.lock_loop, chapter_id)
