from flask import Flask
from flask import json
from flask import jsonify
from flask import request
from flask import redirect
from flask import url_for
from flask import abort
from flask.json import JSONEncoder
from flask_sockets import Sockets
from datetime import datetime
from datetime import timedelta
from imageinspector import DockerHubImageInspector
import os
import time
from pprint import pprint
from requests.exceptions import HTTPError

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        try:
            if isinstance(obj, datetime):
                return obj.isoformat()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)

app = Flask(__name__)
app.json_encoder = CustomJSONEncoder
sockets = Sockets(app)


@app.route("/")
def hello():
    return jsonify(message="Hello World!")

@sockets.route("/ws")
def websocket(ws):
    while not ws.closed:
        message = ws.receive()
        print(message)
        ws.send(message)
    #for n in range(3):
    #    ws.send({"time": time.time()})
    #    time.sleep(1)


@app.route("/<namespace>/<image>")
def canonical_image_details(namespace, image):
    start = time.time()
    if ":" in image:
        (image, tag) = image.split(":")
    else:
        tag = "latest"
    result = {}
    error = None
    try:
        dhii = DockerHubImageInspector(namespace + "/" + image, tag)
        result = {
            "schema_version": dhii.manifest["schemaVersion"],
            "name": dhii.manifest["name"],
            "tag": dhii.manifest["tag"],
            "architecture": dhii.manifest["architecture"],
            "history_length": len(dhii.manifest["history"]),
            "num_layers": len(dhii.layers),
            "config": json.loads(dhii.manifest["history"][0]["v1Compatibility"])["container_config"],
            "layers": [],
            "image_size": 0
        }
        for l in dhii.layers:
            bytes = dhii.get_layer_size(l)
            result["image_size"] += bytes
            result["layers"].append({"digest": l, "size": bytes})
    except HTTPError, e:
        if "404" in str(e):
            abort(404)
        else:
            error = str(e)
    except e:
        error = str(e)
    duration = time.time() - start
    return jsonify(metadata=result, duration=duration, error=error)




if __name__ == '__main__':
    from gevent import pywsgi
    from geventwebsocket.handler import WebSocketHandler
    server = pywsgi.WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    server.serve_forever()
