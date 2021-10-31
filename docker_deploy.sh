#!/bin/bash
project_version=0.0.1
echo "running login"
docker login -u "$DOCKER_USERNAME" --password "$DOCKER_PASSWORD"
echo "running push"
docker tag projetsplets1/log680-lab2 "$DOCKER_USERNAME"/log680-lab2:$project_version
docker tag projetsplets1/log680-lab2 "$DOCKER_USERNAME"/log680-lab2:latest
docker push -a "$DOCKER_USERNAME"/log680-lab2
echo "good"