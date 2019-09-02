import json

from twisted.web.static import File

from justrelax.orchestrator import conf
from justrelax.orchestrator.http.core import app
from justrelax.orchestrator.manager.media import MediaManager


@app.route("/media/", methods=['GET'], branch=True)
def get_media(request):
    request.setHeader('Access-Control-Allow-Origin', '*')

    return File(conf.MEDIA_DIRECTORY)


@app.route("/medias", methods=['GET'])
def get_all_medias(request):
    request.setHeader('Content-Type', 'application/json')
    request.setHeader('Access-Control-Allow-Origin', '*')

    response = {}

    try:
        mm = MediaManager()
        files = mm.get_all()
    except Exception as e:
        response["success"] = False
        response["error"] = str(e)
    else:
        response["success"] = True
        response["content"] = files

    return json.dumps(response)
