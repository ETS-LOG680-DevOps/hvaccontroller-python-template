#!/bin/bash
echo "running login"
docker login -u "$DOCKER_USERNAME" --password "$DOCKER_PASSWORD"
echo "running push"
docker push "$DOCKER_USERNAME"/log680-lab2:latest
echo "good"