import requests
import json
import humanize
import sys
from requests.exceptions import HTTPError, ConnectTimeout
import dateutil.parser

class DockerImageInspector(object):

    def __init__(self, registry_hostname, repository_name, tag="latest"):
        self.base_url = "https://%s" % registry_hostname
        self.repository_name = repository_name
        self.token = None
        self.tag = tag
        self.create_date = None
        self.layers = set()
        self.layer_sizes = {}
        self.tags = []
        self.manifest = None
        self.get_tags()
        self.get_manifest()

    def get_tags(self):
        url = "{base_url}/v2/{name}/tags/list".format(
                base_url=self.base_url,
                name=self.repository_name)
        headers = {}
        if self.token is not None:
            headers["Authorization"] = "Bearer %s" % self.token
        r = requests.get(url, headers=headers, timeout=(3.05,10))
        r.raise_for_status()
        self.tags = r.json()["tags"]

    def get_manifest(self):
        url = "{base_url}/v2/{name}/manifests/{reference}".format(
                base_url=self.base_url,
                name=self.repository_name,
                reference=self.tag)
        headers = {}
        if self.token is not None:
            headers["Authorization"] = "Bearer %s" % self.token
        r = requests.get(url, headers=headers, timeout=(3.05,10))
        r.raise_for_status()
        self.manifest = r.json()
        for l in self.manifest["fsLayers"]:
            self.layers.add(l["blobSum"])
        if "history" in self.manifest:
            if "v1Compatibility" in self.manifest["history"][0]:
                hist = json.loads(self.manifest["history"][0]["v1Compatibility"])
                self.create_date = dateutil.parser.parse(hist["created"])
        self.manifest_content_type = r.headers["content-type"]

    def get_layer_size(self, layer_hash):
        """
        Attempt to return the size of the given layer
        """
        url = "{base_url}/v2/{name}/blobs/{layer_hash}".format(
              base_url=self.base_url,
              name=self.repository_name,
              layer_hash=layer_hash)
        headers = {}
        if self.token is not None:
            headers["Authorization"] = "Bearer %s" % self.token
        r = requests.head(url, headers=headers, allow_redirects=True, timeout=(3.05,5))
        r.raise_for_status()
        if "content-length" in r.headers:
            self.layer_sizes[layer_hash] = int(r.headers["content-length"])
        else:
            self.layer_sizes[layer_hash] = None
        return self.layer_sizes[layer_hash]


class DockerHubImageInspector(DockerImageInspector):

    def __init__(self, repository_name, tag="latest"):
        self.base_url = "https://registry.hub.docker.com"
        self.repository_name = repository_name
        self.__get_token()
        self.tag = tag
        self.layers = set()
        self.layer_sizes = {}
        self.tags = []
        self.manifest = None
        self.get_tags()
        self.get_manifest()

    def __get_token(self):
        url = "https://auth.docker.io/token"
        params = {
            "service": "registry.docker.io",
            "scope": "repository:{name}:pull".format(
                name=self.repository_name)
        }
        r = requests.get(url, params=params)
        r.raise_for_status()
        self.token = r.json()["token"]



if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Inspect an image from DockerHub')
    parser.add_argument('image', metavar='IMAGE',
                        help='The image to look for, e.g. "library/redis"')

    args = parser.parse_args()
    if ":" in args.image:
        (image, tag) = args.image.split(":")
    else:
        image = args.image
        tag = "latest"

    image_parts = image.split("/")
    registry = None
    namespace = None
    repository = None
    if len(image_parts) == 3:
        registry = image_parts[-3]
    else:
        registry = "index.docker.io"
    if len(image_parts) >= 2:
        namespace = image_parts[-2]
    else:
        namespace = "library"
    repository = image_parts[-1]

    image = "/".join([registry, namespace, repository])

    try:
        if registry == "index.docker.io":
            dii = DockerHubImageInspector(namespace + "/" + repository, tag)
        else:
            dii = DockerImageInspector(registry, namespace + "/" + repository, tag)
    except HTTPError, e:
        sys.stderr.write(str(e) + "\n")
        sys.exit(1)
    except ConnectTimeout, e:
        sys.stderr.write(str(e) + "\n")
        sys.exit(2)
    except Exception, e:
        sys.stderr.write("Unknown error: " + str(e) + "\n")
        sys.exit(3)

    print("Schema version: %s" % dii.manifest["schemaVersion"])
    print("Image name: %s" % dii.manifest["name"])
    print("Tag: %s" % dii.manifest["tag"])
    print("Architecture: %s" % dii.manifest["architecture"])
    print("Number of history entries: %d" % len(dii.manifest["history"]))
    print("Create date: %s" % dii.create_date.strftime("%Y-%m-%d %H:%M:%S"))
    print("Configuration:")
    print(json.dumps(json.loads(dii.manifest["history"][0]["v1Compatibility"])["container_config"], indent=2))
    print("Number of layers: %d" % len(dii.layers))
    print("Layers:")
    size = 0
    for l in dii.layers:
        bytes = dii.get_layer_size(l)
        if bytes is not None:
            print("  %s - %s" % (l, humanize.naturalsize(bytes)))
            size += bytes
        else:
            print("  %s - unknown" % l)
    print("Image size: %s" % humanize.naturalsize(size))
