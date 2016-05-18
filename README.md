[![This image on DockerHub](https://img.shields.io/docker/pulls/giantswarm/inspect-docker-image.svg)](https://hub.docker.com/r/giantswarm/inspect-docker-image/) [![IRC Channel](https://img.shields.io/badge/irc-%23giantswarm-blue.svg)](https://kiwiirc.com/client/irc.freenode.net/#giantswarm)

# Dockerhub Image Inspector

A little utility/POC to fetch info on a particular image from the public Docker registry. Works both in CLI and web API mode.

## Running the CLI

A public Docker image is available. Pull the image and create an alias:

```nohighlight
docker pull giantswarm/inspect-docker-image
alias idi="docker run --rm giantswarm/inspect-docker-image"
```

Execute, to fetch info on `redis:3.2`, for example:

```nohighlight
idi redis:3.2
```

See below for example output.

## Running the Webservice

A `docker-compose.yml` file is provided, so you can simply launch the service like this:

```nohighlight
docker-compose up
```

This will make the API available on port 5000 via your docker IP.

Here are a few cases to test:

- `http://<docker_ip>:5000/nginx`
- `http://<docker_ip>:5000/redis:3.2`
- `http://<docker_ip>:5000/library/redis`
- `http://<docker_ip>:5000/index.docker.io/library/redis`
- `http://<docker_ip>:5000/index.docker.io/library/ubuntu:latest`
- `http://<docker_ip>:5000/index.docker.io/giantswarm/helloworld`
- `http://<docker_ip>:5000/quay.io/giantswarm/helloworld`

## Development

Set up your python environment for development like this:

```nohighlight
git clone https://github.com/giantswarm/inspect-docker-image.git
cd inspect-docker-image/
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

You can then execute the CLI like this:

```nohighlight
python imageinspector.py redis:3.2
```

and the service:

```nohighlight
DEBUGGING=1 python service.py
```

## CLI example output

The output looks something like this:

```nohighlight
Schema version: 1
Image name: library/redis
Tag: 3.2
Architecture: amd64
Number of history entries: 17
Configuration:
{
  "Tty": false, 
  "Cmd": [
    "/bin/sh", 
    "-c", 
    "#(nop) CMD [\"redis-server\"]"
  ], 
  "Volumes": {
    "/data": {}
  }, 
  "Domainname": "", 
  "WorkingDir": "/data", 
  "Image": "9b8288e1a4bf007bec3c9778b4833ca75a6c4c9a708a07c8e28f5cd7bb64704b", 
  "Hostname": "f416997e8b71", 
  "StdinOnce": false, 
  "Labels": {}, 
  "AttachStdin": false, 
  "User": "", 
  "Env": [
    "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin", 
    "GOSU_VERSION=1.7", 
    "REDIS_VERSION=3.2.0", 
    "REDIS_DOWNLOAD_URL=http://download.redis.io/releases/redis-3.2.0.tar.gz", 
    "REDIS_DOWNLOAD_SHA1=0c1820931094369c8cc19fc1be62f598bc5961ca"
  ], 
  "ExposedPorts": {
    "6379/tcp": {}
  }, 
  "OnBuild": [], 
  "AttachStderr": false, 
  "Entrypoint": [
    "docker-entrypoint.sh"
  ], 
  "AttachStdout": false, 
  "OpenStdin": false
}
Number of layers: 8
Layers:
  sha256:89fd7ac1e6768d1dd82e596e9dade676e87f1309da2a07f6e748c657b3c634b6 - 647 Bytes
  sha256:8c429fec161a6c1042680f2033c2f7f5efc9b666f9c9ee22bded5d00e43f87f7 - 807933 Bytes
  sha256:4f93af242dfb5159fb9b2a303a1e71df5a39bd1a9a6561c746216897924b8dbf - 16615562 Bytes
  sha256:a3ed95caeb02ffe68cdd9fd84406680ae93d633cb16422d00e8a7c22955b46d4 - 32 Bytes
  sha256:8b87079b7a06f9b72e3cca2c984c60e118229c60f0bff855d822f758c112b485 - 51355855 Bytes
  sha256:284e33235544c2285bd64ce90c1d8c909c92823ab76199dc33bbfe82f74e1870 - 2040 Bytes
  sha256:77b759f85e4a66409a1765a074e3d71edb417ca2e4fdf67fc5c02d7d0a6088ad - 5447529 Bytes
  sha256:53c576ba5eccafa633606c947a44fed94a7ff4b8f965b8fdf10e0109cf64d9ff - 96 Bytes
Image size: 74229694 Bytes
```

## Webservice example output

```json

{
  "duration": 3.5770351886749268, 
  "error": null, 
  "metadata": {
    "architecture": "amd64", 
    "config": {
      "AttachStderr": false, 
      "AttachStdin": false, 
      "AttachStdout": false, 
      "Cmd": [
        "/bin/sh", 
        "-c", 
        "#(nop) CMD [\"nginx\" \"-g\" \"daemon off;\"]"
      ], 
      "Domainname": "", 
      "Entrypoint": null, 
      "Env": [
        "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin", 
        "NGINX_VERSION=1.9.15-1~jessie"
      ], 
      "ExposedPorts": {
        "443/tcp": {}, 
        "80/tcp": {}
      }, 
      "Hostname": "f416997e8b71", 
      "Image": "317a0530f60c747e425f5a011a943939db69d53beaad8f89c81ace4b487442df", 
      "Labels": {}, 
      "OnBuild": [], 
      "OpenStdin": false, 
      "StdinOnce": false, 
      "Tty": false, 
      "User": "", 
      "Volumes": null, 
      "WorkingDir": ""
    }, 
    "history_length": 8, 
    "image_size": 71175964, 
    "layers": [
      {
        "digest": "sha256:31c7abf879e0ca73db0d8cf61f06343aa653efd1be8cf1dec67f839a9beb71fa", 
        "size": 19819882
      }, 
      {
        "digest": "sha256:4ef177b369db36e463a9bd44b64669f2da2c80436d9d52178840c37783edcf0b", 
        "size": 195
      }, 
      {
        "digest": "sha256:8b87079b7a06f9b72e3cca2c984c60e118229c60f0bff855d822f758c112b485", 
        "size": 51355855
      }, 
      {
        "digest": "sha256:a3ed95caeb02ffe68cdd9fd84406680ae93d633cb16422d00e8a7c22955b46d4", 
        "size": 32
      }
    ], 
    "name": "library/nginx", 
    "num_layers": 4, 
    "schema_version": 1, 
    "tag": "latest"
  }
}
```
