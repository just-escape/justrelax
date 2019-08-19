import json

from klein import Klein

from justrelax.orchestrator.processor.engine import UndefinedAction


class App:
    app = Klein()
    service = None
    processor_configs = None

    @staticmethod
    def get_resource():
        return App.app.resource()

    @staticmethod
    def get_processor_configs():
        return App.service.get_processor_configs()

    @staticmethod
    @app.route("/get_rooms")
    def get_rooms(request):
        request.setHeader('Content-Type', 'application/json')
        request.setHeader('Access-Control-Allow-Origin', '*')

        response = {}

        try:
            config = App.get_processor_configs()
        except Exception as e:
            response["success"] = False
            response["error"] = str(e)
        else:
            response["success"] = True
            response["content"] = config

        return json.dumps(response)

    @staticmethod
    @app.route("/run_room")
    def run_room(request):
        request.setHeader('Content-Type', 'application/json')
        request.setHeader('Access-Control-Allow-Origin', '*')

        response = {}

        channel = request.args.get(b'channel', [None])[0].decode('utf8')

        try:
            App.service.run_room(channel)
        except Exception as e:
            response["success"] = False
            response["error"] = str(e)
        else:
            response["success"] = True

        return json.dumps(response)

    @staticmethod
    @app.route("/halt_room")
    def halt_room(request):
        request.setHeader('Content-Type', 'application/json')
        request.setHeader('Access-Control-Allow-Origin', '*')

        response = {}

        channel = request.args.get(b'channel', [None])[0].decode('utf8')

        try:
            App.service.halt_room(channel)
        except Exception as e:
            response["success"] = False
            response["error"] = str(e)
        else:
            response["success"] = True

        return json.dumps(response)

    @staticmethod
    @app.route("/reset_room")
    def reset_room(request):
        request.setHeader('Content-Type', 'application/json')
        request.setHeader('Access-Control-Allow-Origin', '*')

        response = {}

        channel = request.args.get(b'channel', [None])[0].decode('utf8')

        try:
            App.service.reset_room(channel)
        except Exception as e:
            response["success"] = False
            response["error"] = str(e)
        else:
            response["success"] = True

        return json.dumps(response)

    @staticmethod
    @app.route("/process_action")
    def process_action(request):
        request.setHeader('Content-Type', 'application/json')
        request.setHeader('Access-Control-Allow-Origin', '*')

        response = {}

        channel = request.args.get(b'channel', [None])[0].decode('utf8')
        action = request.args.get(b'name', [None])[0].decode('utf8')

        from justrelax.common.logging import logger
        logger.info("{} {}".format(channel, action))

        try:
            App.service.process_action(channel, action)
        except UndefinedAction as e:
            response["success"] = False
            response["error"] = str(e)
        except Exception as e:
            response["success"] = False
            response["error"] = str(e)
        else:
            response["success"] = True

        return json.dumps(response)
