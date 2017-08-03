set -ev

if [ "$TRAVIS_BRANCH" = "master" ]
then
  docker build -t apinf/openapi-space:$DOCKER_TAG .
  docker login -u="$DOCKER_USERNAME" -p="$DOCKER_PASSWORD"
  docker push apinf/openapi-space:$DOCKER_TAG
fi
