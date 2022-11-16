#!/bin/bash

podman stop PHQuery

podman rm PHQuery

podman image rm query-projeto-horizonte

podman build -t=query-projeto-horizonte .

podman run -dt -p 40002:2000 --cpus=0.25 -m=256m --name=PHQuery query-projeto-horizonte