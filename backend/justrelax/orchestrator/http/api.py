import json

from klein import Klein

from justrelax.orchestrator.services import Services
from justrelax.orchestrator.manager.room import RoomManager
from justrelax.orchestrator.manager.camera import CameraManager
from justrelax.orchestrator.processor.engine import UndefinedAction


def get_arg(request, name):
    encoded_name = name.encode('utf8')
    arg = request.args.get(encoded_name, None)
    if arg is None:
        return arg
    return arg[0].decode('utf8')


class App:
    app = Klein()
    resource = app.resource()

    @staticmethod
    @app.route("/rooms", methods=['GET'])
    def get_rooms(request):
        request.setHeader('Content-Type', 'application/json')
        request.setHeader('Access-Control-Allow-Origin', '*')

        response = {}

        try:
            rm = RoomManager()
            rooms = rm.get_all()
            room_dicts = [r.as_dict() for r in rooms]
        except Exception as e:
            response["success"] = False
            response["error"] = str(e)
        else:
            response["success"] = True
            response["content"] = room_dicts

        return json.dumps(response)

    @staticmethod
    @app.route("/rooms/<int:id_>", methods=['GET'])
    def get_room(request, id_):
        request.setHeader('Content-Type', 'application/json')
        request.setHeader('Access-Control-Allow-Origin', '*')

        response = {}

        try:
            rm = RoomManager()
            room = rm.get(id_)
        except Exception as e:
            response["success"] = False
            response["error"] = str(e)
        else:
            response["success"] = True
            response["content"] = room.as_dict()

        return json.dumps(response)

    @staticmethod
    @app.route("/rooms", methods=['POST'])
    def create_room(request):
        request.setHeader('Content-Type', 'application/json')
        request.setHeader('Access-Control-Allow-Origin', '*')

        response = {}

        scenario = get_arg(request, 'scenario')
        cardinal = get_arg(request, 'cardinal')
        channel = get_arg(request, 'channel')
        rules = get_arg(request, 'rules')

        try:
            rm = RoomManager()
            room = rm.create(scenario, cardinal, channel, rules)
            rm.commit()
        except Exception as e:
            response["success"] = False
            response["error"] = str(e)
        else:
            response["success"] = True
            response["content"] = room.as_dict()

        return json.dumps(response)

    @staticmethod
    @app.route("/rooms/<int:id_>", methods=['PUT', 'PATCH'])
    def update_room(request, id_):
        request.setHeader('Content-Type', 'application/json')
        request.setHeader('Access-Control-Allow-Origin', '*')

        response = {}

        fields = [
            'scenario',
            'cardinal',
            'channel',
            'rules',
        ]

        updates = {}
        for field in fields:
            value = get_arg(request, field)
            if value:
                updates[field] = value

        try:
            rm = RoomManager()
            room = rm.update(id_, updates)
            rm.commit()
        except Exception as e:
            response["success"] = False
            response["error"] = str(e)
        else:
            response["success"] = True
            response["content"] = room.as_dict()

        return json.dumps(response)

    @staticmethod
    @app.route("/rooms/<int:id_>", methods=['DELETE'])
    def delete_room(request, id_):
        request.setHeader('Content-Type', 'application/json')
        request.setHeader('Access-Control-Allow-Origin', '*')

        response = {}

        try:
            rm = RoomManager()
            rm.delete(id_)
            rm.commit()
        except Exception as e:
            response["success"] = False
            response["error"] = str(e)
        else:
            response["success"] = True

        return json.dumps(response)

    @staticmethod
    @app.route("/rooms/<int:id_>/get_live_data", methods=['GET'])
    def get_room_live_data(request, id_):
        request.setHeader('Content-Type', 'application/json')
        request.setHeader('Access-Control-Allow-Origin', '*')

        response = {}

        try:
            processor = Services.just_process.get_processor(id_)
            live_data = processor.get_live_data()
        except Exception as e:
            response["success"] = False
            response["error"] = str(e)
        else:
            response["success"] = True
            response["content"] = live_data

        return json.dumps(response)

    @staticmethod
    @app.route("/rooms/<int:id_>/run", methods=['POST'])
    def run_room(request, id_):
        request.setHeader('Content-Type', 'application/json')
        request.setHeader('Access-Control-Allow-Origin', '*')

        response = {}

        n_players = get_arg(request, 'n_players')

        try:
            n_players = int(n_players)
        except ValueError:
            response["success"] = False
            response["error"] = "n_players ({}) must be an int".format(
                n_players)
        else:
            try:
                processor = Services.just_process.get_processor(id_)
                processor.run_room(n_players=n_players)
            except Exception as e:
                response["success"] = False
                response["error"] = str(e)
            else:
                response["success"] = True

        return json.dumps(response)

    @staticmethod
    @app.route("/rooms/<int:id_>/set_n_players", methods=['POST'])
    def set_n_players(request, id_):
        request.setHeader('Content-Type', 'application/json')
        request.setHeader('Access-Control-Allow-Origin', '*')

        response = {}

        n_players = get_arg(request, 'n_players')

        try:
            n_players = int(n_players)
        except ValueError:
            response["success"] = False
            response["error"] = "n_players ({}) must be an int".format(
                n_players)
        else:
            try:
                processor = Services.just_process.get_processor(id_)
                processor.set_n_players(n_players=n_players)
            except Exception as e:
                response["success"] = False
                response["error"] = str(e)
            else:
                response["success"] = True

        return json.dumps(response)

    @staticmethod
    @app.route("/rooms/<int:id_>/halt", methods=["POST"])
    def halt_room(request, id_):
        request.setHeader('Content-Type', 'application/json')
        request.setHeader('Access-Control-Allow-Origin', '*')

        response = {}

        try:
            processor = Services.just_process.get_processor(id_)
            processor.halt_room()
        except Exception as e:
            response["success"] = False
            response["error"] = str(e)
        else:
            response["success"] = True

        return json.dumps(response)

    @staticmethod
    @app.route("/rooms/<int:id_>/reset", methods=["POST"])
    def reset_room(request, id_):
        request.setHeader('Content-Type', 'application/json')
        request.setHeader('Access-Control-Allow-Origin', '*')

        response = {}

        try:
            processor = Services.just_process.get_processor(id_)
            processor.reset_room()
        except Exception as e:
            response["success"] = False
            response["error"] = str(e)
        else:
            response["success"] = True

        return json.dumps(response)

    @staticmethod
    @app.route("/rooms/<int:id_>/action", methods=["POST"])
    def process_action(request, id_):
        request.setHeader('Content-Type', 'application/json')
        request.setHeader('Access-Control-Allow-Origin', '*')

        response = {}

        name = get_arg(request, 'name')

        try:
            processor = Services.just_process.get_processor(id_)
            processor.process_action_from_name(name)
        except UndefinedAction as e:
            response["success"] = False
            response["error"] = str(e)
        except Exception as e:
            response["success"] = False
            response["error"] = str(e)
        else:
            response["success"] = True

        return json.dumps(response)

    @staticmethod
    @app.route("/cameras", methods=["GET"])
    def get_cameras(request):
        request.setHeader('Content-Type', 'application/json')
        request.setHeader('Access-Control-Allow-Origin', '*')

        response = {}

        try:
            cm = CameraManager()
            cameras = cm.get_all()
            camera_dicts = [c.as_dict() for c in cameras]
        except Exception as e:
            response["success"] = False
            response["error"] = str(e)
        else:
            response["success"] = True
            response["content"] = camera_dicts

        return json.dumps(response)
