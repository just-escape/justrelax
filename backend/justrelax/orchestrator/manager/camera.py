from justrelax.orchestrator.manager.core import Manager
from justrelax.orchestrator.storage.models import Camera


class CameraManager(Manager):
    def get_all(self):
        return self.session.query(Camera).all()
