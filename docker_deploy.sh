#!/bin/bash
echo "running login"
docker login -u "$DOCKER_USERNAME" --password "$DOCKER_PASSWORD"
echo "running push"
docker push --all-tags "$DOCKER_USERNAME"/log680-lab2
echo "good"