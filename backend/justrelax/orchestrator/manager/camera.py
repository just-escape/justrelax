from justrelax.orchestrator.manager.core import Manager
from justrelax.orchestrator.storage.models import Camera


class CameraManager(Manager):
    def get_all_from_room_id(self, room_id):
        return self.session.query(Camera).filter(Camera.room_id == room_id)
