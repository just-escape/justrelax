import json

from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker

from justrelax.orchestrator.storage.models import Base, Room, Camera


if __name__ == '__main__':
    engine = create_engine(
        'postgresql://justrelax:justrelaxlalalalala@localhost:5432/justrelax')
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

    session_maker = sessionmaker(bind=engine)
    s = session_maker()

    with open('digimiam_rules.json', 'r') as fh:
        rules = json.dumps(json.load(fh))

    r = Room(
        scenario='Le digimiam',
        cardinal='room 1',
        channel='digimiam1',
        rules=rules,
    )
    s.add(r)
    s.commit()
    for i in range(1, 7):
        c = Camera(
            room_id=r.id,
            name='Cam {}'.format(i),
            url='http://192.168.0.3:80',
        )
        s.add(c)

    r = Room(
        scenario='Le digimiam',
        cardinal='room 2',
        channel='digimiam2',
        rules=rules,
    )
    s.add(r)
    s.commit()
    for i in range(1, 7):
        c = Camera(
            room_id=r.id,
            name='Cam {}'.format(i),
            url='http://192.168.0.3:80',
        )
        s.add(c)

    s.commit()
