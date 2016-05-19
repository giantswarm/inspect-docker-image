from flask import Flask
from flask import json
from flask import jsonify
from flask import request
from flask import redirect
from flask import url_for
from flask import abort
from flask.ext.cors import CORS
from flask.json import JSONEncoder
from datetime import datetime
from datetime import timedelta
from imageinspector import DockerHubImageInspector
from imageinspector import DockerImageInspector
import os
import time
from pprint import pprint
from requests.exceptions import HTTPError, ConnectTimeout

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
CORS(app, resources={r"/*": {"origins": "*"}})
app.json_encoder = CustomJSONEncoder
app.config.update(dict(
    PREFERRED_URL_SCHEME = os.getenv("PREFERRED_URL_SCHEME", "https"),
    DEFAULT_REGISTRY = "index.docker.io",
    DEFAULT_NAMESPACE = "library"
))

@app.route("/")
def hello():
    return jsonify(message="Hello World!",
                   source="https://github.com/giantswarm/inspect-docker-image")

@app.route("/<registry>/<namespace>/<image>")
def canonical_image_details(registry, namespace, image):
    start = time.time()
    if ":" in image:
        (image, tag) = image.split(":")
    else:
        tag = "latest"
    result = {}
    error = None
    try:
        if registry == app.config["DEFAULT_REGISTRY"]:
            dii = DockerHubImageInspector(namespace + "/" + image, tag)
        else:
            dii = DockerImageInspector(registry, namespace + "/" + image, tag)

        result = {
            "schema_version": dii.manifest["schemaVersion"],
            "name": dii.manifest["name"],
            "tag": dii.manifest["tag"],
            "architecture": dii.manifest["architecture"],
            "history_length": len(dii.manifest["history"]),
            "num_layers": len(dii.layers),
            "config": json.loads(dii.manifest["history"][0]["v1Compatibility"])["container_config"],
            "layers": [],
            "image_size": 0
        }
        for l in dii.layers:
            bytesize = dii.get_layer_size(l)
            if bytesize is not None:
                result["image_size"] += bytesize
            result["layers"].append({"digest": l, "size": bytesize})
    except HTTPError, e:
        if "404" in str(e):
            abort(404)
        else:
            error = str(e)
    except ConnectTimeout, e:
        error = str(e)
    except Exception, e:
        error = str(e)
    duration = time.time() - start
    return jsonify(metadata=result, duration=duration, error=error)


@app.route("/<image>")
def namespace_image_redirect(image):
    if image == "favicon.ico":
        abort(404)
    url = url_for("canonical_image_details",
        registry=app.config["DEFAULT_REGISTRY"],
        namespace=app.config["DEFAULT_NAMESPACE"],
        image=image,
        _external=True,
        _scheme=app.config["PREFERRED_URL_SCHEME"])
    return redirect(url)


@app.route("/<namespace>/<image>")
def image_redirect(namespace, image):
    url = url_for("canonical_image_details",
        registry=app.config["DEFAULT_REGISTRY"],
        namespace=namespace,
        image=image,
        _external=True,
        _scheme=app.config["PREFERRED_URL_SCHEME"])
    return redirect(url)

if __name__ == '__main__':
    debug = os.getenv("DEBUGGING")
    if debug is None:
        app.run(host="0.0.0.0", port=5000, debug=False)
    else:
        app.run(host="0.0.0.0", port=5000, debug=True)
