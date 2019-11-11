from justrelax.orchestrator.manager.core import Manager
from justrelax.orchestrator.storage.models import Room


class RoomManager(Manager):
    def get_all(self):
        return self.session.query(Room).all()

    def get(self, id_):
        return self.session.query(Room).filter(Room.id == id_)

    def create(self, scenario, cardinal, channel, rules):
        r = Room(
            scenario=scenario,
            cardinal=cardinal,
            channel=channel,
            rules=rules,
        )
        self.session.add(r)
        return r

    def update(self, id_, updates):
        pass

    def update_rules(self, id_, rules):
        self.session.query(Room).filter_by(id=id_).update({Room.rules: rules})

    def delete(self, id_):
        pass
