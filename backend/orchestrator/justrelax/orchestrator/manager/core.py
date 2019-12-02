from justrelax.orchestrator.storage.session import get_session


class Manager:
    def __init__(self):
        self.session = get_session()

    def commit(self):
        self.session.commit()
