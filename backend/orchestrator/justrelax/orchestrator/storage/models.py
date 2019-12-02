import json
import enum

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, Enum
from sqlalchemy import ForeignKey
from sqlalchemy.orm import validates, relationship
from sqlalchemy.ext.declarative import declarative_base
from marshmallow_sqlalchemy import ModelSchema

from justrelax.common.validation import validate_channel

Base = declarative_base()


class Room(Base):
    __tablename__ = 'room'

    id = Column(Integer, primary_key=True)
    scenario = Column(String(64), nullable=False)
    cardinal = Column(String(64))
    channel = Column(String(64), nullable=False)
    rules = Column(Text())
    cameras = relationship('Camera')

    @validates('scenario')
    def validate_scenario(self, _, value):
        if not isinstance(value, str):
            raise ValueError("scenario ({}) must be a string".format(value))

        if len(value) > 64:
            raise ValueError("scenario ({}) is limited to 64 characters".format(value))

        return value

    @validates('cardinal')
    def validate_cardinal(self, _, value):
        if value is None:
            return value

        if not isinstance(value, str):
            raise ValueError("cardinal ({}) must be a string".format(value))

        if len(value) > 64:
            raise ValueError("cardinal ({}) is limited to 64 characters".format(value))

        return value

    @validates('channel')
    def validate_channel(self, _, value):
        if not isinstance(value, str):
            raise ValueError("channel ({}) must be a string".format(value))

        # TODO: check if the value is for bytes
        if len(value) > 64:
            raise ValueError("channel ({}) is limited to 64 characters".format(value))

        if not validate_channel(value):
            raise ValueError("channel ({}) must be an alphanumeric string".format(value))

        return value

    @validates('rules')
    def validate_rules(self, _, value):
        #TODO: think of an ergonomic way to deal with this
        return value

    def as_dict(self):
        schema = RoomSchema()
        room = schema.dump(self)
        room['rules'] = json.loads(room['rules'])
        return room


class Camera(Base):
    __tablename__ = 'camera'

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    url = Column(String(1024), nullable=False)
    room_id = Column(Integer, ForeignKey('room.id'), nullable=False)

    @validates('name')
    def validate_name(self, _, value):
        if not isinstance(value, str):
            raise ValueError("name ({}) must be a string".format(value))

        if len(value) > 64:
            raise ValueError("name ({}) is limited to 64 characters".format(value))

        return value

    @validates('url')
    def validate_url(self, _, value):
        if not isinstance(value, str):
            raise ValueError("url ({}) must be a string".format(value))

        if len(value) > 1024:
            raise ValueError("url ({}) is limited to 64 characters".format(value))

        return value

    @validates('room_id')
    def validate_room_id(self, _, value):
        if not isinstance(value, int):
            raise ValueError("room_id ({}) must be an int".format(value))

        return value

    def as_dict(self):
        schema = CameraSchema()
        return schema.dump(self)


class Session(Base):
    __tablename__ = 'session'

    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey('room.id'), nullable=False)
    n_players = Column(Integer, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime)
    end_ticks = Column(Integer)


class Rule(Base):
    __tablename__ = 'rule'

    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('session.id'), nullable=False)
    name = Column(String(128), nullable=False)
    execution_date = Column(DateTime, nullable=False)
    execution_ticks = Column(Integer, nullable=False)


class Action(Base):
    __tablename__ = 'action'

    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('session.id'), nullable=False)
    name = Column(String(128), nullable=False)
    execution_date = Column(DateTime, nullable=False)
    execution_ticks = Column(Integer, nullable=False)


class Alarm(Base):
    __tablename__ = 'alarm'

    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('session.id'), nullable=False)
    name = Column(String(128), nullable=False)
    duration_ticks = Column(Integer, nullable=False)
    start_date = Column(DateTime, nullable=False)
    start_ticks = Column(Integer, nullable=False)
    cancellation_date = Column(DateTime)
    cancellation_ticks = Column(Integer)
    executed_actions = Column(Boolean)


class MessageDirections(enum.Enum):
    to_node = 'to_node'
    from_node = 'from_node'


class Message(Base):
    __tablename__ = 'message'

    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('session.id'), nullable=False)
    direction = Column(Enum(MessageDirections), nullable=False)
    node_name = Column(String(128), nullable=False)
    message = Column(String(128), nullable=False)
    date = Column(DateTime, nullable=False)
    ticks = Column(Integer, nullable=False)


class Record(Base):
    __tablename__ = 'record'

    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('session.id'), nullable=False)
    label = Column(String(128), nullable=False)
    date = Column(DateTime, nullable=False)
    ticks = Column(Integer, nullable=False)


class RoomSchema(ModelSchema):
    class Meta:
        model = Room
        exclude = ["cameras"]


class CameraSchema(ModelSchema):
    class Meta:
        model = Camera


class SessionSchema(ModelSchema):
    class Meta:
        model = Session


class RuleSchema(ModelSchema):
    class Meta:
        model = Rule


class ActionSchema(ModelSchema):
    class Meta:
        model = Action


class AlarmSchema(ModelSchema):
    class Meta:
        model = Alarm


class MessageSchema(ModelSchema):
    class Meta:
        model = Message


class RecordSchema(ModelSchema):
    class Meta:
        model = Record
