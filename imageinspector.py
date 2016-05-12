import requests
import json
import humanize


class DockerHubImageInspector(object):

    def __init__(self, repository_name, tag="latest"):
        self.base_url = "https://registry.hub.docker.com"
        self.repository_name = repository_name
        self.tag = tag
        self.layers = set()
        self.layer_sizes = {}
        self.tags = []
        self.manifest = None
        self.__get_token()
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

    def get_tags(self):
        url = "{base_url}/v2/{name}/tags/list".format(
                base_url=self.base_url,
                name=self.repository_name)
        headers = {
            "Authorization": "Bearer %s" % self.token
        }
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        self.tags = r.json()["tags"]

    def get_manifest(self):
        url = "{base_url}/v2/{name}/manifests/{reference}".format(
                base_url=self.base_url,
                name=self.repository_name,
                reference=self.tag)
        headers = {
            "Authorization": "Bearer %s" % self.token
        }
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        for l in r.json()["fsLayers"]:
            self.layers.add(l["blobSum"])
        self.manifest = r.json()
        self.manifest_content_type = r.headers["content-type"]

    def get_layer_size(self, layer_hash):
        """
        Attempt to return the size of the given layer
        """
        url = "{base_url}/v2/{name}/blobs/{layer_hash}".format(
              base_url=self.base_url,
              name=self.repository_name,
              layer_hash=layer_hash)
        headers = {
            "Authorization": "Bearer %s" % self.token
        }
        r = requests.head(url, headers=headers, allow_redirects=True)
        r.raise_for_status()
        if "content-length" in r.headers:
            self.layer_sizes[layer_hash] = int(r.headers["content-length"])
        return int(r.headers["content-length"])


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

    if "/" not in image:
        image = "library/%s" % image

    dhii = DockerHubImageInspector(image, tag)
    print("Schema version: %s" % dhii.manifest["schemaVersion"])
    print("Image name: %s" % dhii.manifest["name"])
    print("Tag: %s" % dhii.manifest["tag"])
    print("Architecture: %s" % dhii.manifest["architecture"])
    print("Number of history entries: %d" % len(dhii.manifest["history"]))
    print("Configuration:")
    print(json.dumps(json.loads(dhii.manifest["history"][0]["v1Compatibility"])["container_config"], indent=2))
    print("Number of layers: %d" % len(dhii.layers))
    print("Layers:")
    size = 0
    for l in dhii.layers:
        bytes = dhii.get_layer_size(l)
        size += bytes
        print("  %s - %s" % (l, humanize.naturalsize(bytes)))
    print("Image size: %s" % humanize.naturalsize(size))
