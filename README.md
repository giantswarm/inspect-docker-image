# Dockerhub Image Inspector

A little utility/POC to fetch info on a particular image from the public Docker registry

## Running it the Docker way

Pull the image:

```nohighlight
docker pull giantswarm/inspect-docker-image
```

Execute, to fetch info on `redis:3.2`, for example:

```nohighlight
docker run --rm -ti giantswarm/inspect-docker-image redis:3.2
```

## Install

```nohighlight
git clone https://github.com/giantswarm/inspect-docker-image.git
cd inspect-docker-image/
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run

```nohighlight
python imageinspector.py redis:3.2
```

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