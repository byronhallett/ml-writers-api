REGISTRY_ID=asia.gcr.io/cl-syd-ml-writers/ml-api
docker build . -t ml-api
docker tag ml-api $REGISTRY_ID
docker push $REGISTRY_ID