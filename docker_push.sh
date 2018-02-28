#!/bin/bash

REPO=girleffect/core-access-control
# Map "master" branch to "latest" tag. "develop" branch will have the "develop" tag.
TAG=${TRAVIS_BRANCH/master/latest}
if [ "${TAG}" != "master" ]; then TAG="test"; fi

docker build -t ${REPO}:${TAG} .
docker login -u="${DOCKER_USERNAME}" -p="${DOCKER_PASSWORD}"
docker push ${REPO}
