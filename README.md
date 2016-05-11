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
python inspect.py redis:3.2
```
