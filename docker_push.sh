#!/bin/bash

echo $DOCKER_USERNAME
echo $DOCKER_PASSWORD

docker login -u $DOCKER_USERNAME -p $DOCKER_PASSWORD
docker push girleffect/core-access-control