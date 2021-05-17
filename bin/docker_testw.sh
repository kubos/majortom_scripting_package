#!/bin/bash -e

docker build -t scripting_api .
docker run --rm -it \
  -v $(pwd):/app \
  scripting_api ptw --poll -- --log-level=INFO --verbose --capture=no --cache-clear