# BLURB BLOCKS API

## INSTALL

locally
```sh
# USE A PYTHON3 ENV
pip install -r requirements.txt
python main.py
```

Forget about it, just push to gcloud in your project
```sh
gcloud app deploy --quiet --project cl-syd-ml-writers
```

## CONFIG

Locally, add a .env with
```sh
BUCKET_NAME=blurb-blocks-data
SEED_LENGTH=48
TEMPERATURE=0.8
```

For gcloud app engine, edit the **app.yaml**

## GCE deployment
Create a GCE instance based on the `ml-api-template` template
then
```sh
gcloud source repos clone gpt2-GAE-api --project=cl-syd-ml-writers
cd gpt2-GAE-api
sudo apt install python3-pip
sudo apt install uwsgi-core
pip3 install -r requirements.txt
NVIDIA_VISIBLE_DEVICES=all \
  NVIDIA_DRIVER_CAPABILITIES=compute,utility \
  NVIDIA_REQUIRE_CUDA="cuda>=8.0" \
  LANG=C.UTF-8 \
  BUCKET_NAME=blurb-blocks \
  TEMPERATURE=0.8 \
  GOOGLE_APPLICATION_CREDENTIALS=/gpt-2-server/cl-syd-ml-writers-881b263b3fbb.json
uwsgi --http-socket 3389 --wsgi-file main.py --callable app --master --processes 1 --threads 2
```

## Kubernetes engine config

Head to the technology section of this drive project for the json security key
https://drive.google.com/open?id=1IYHRGzLtGaKB7WK1KyBwQ8x92dsj8nLT

```sh
gcloud beta container --project "cl-syd-ml-writers" clusters create "blurb-blocks-api" --zone "australia-southeast1-c" --no-enable-basic-auth --cluster-version "1.12.8-gke.10" --machine-type "n1-highmem-2" --accelerator "type=nvidia-tesla-p100,count=1" --image-type "COS" --disk-type "pd-standard" --disk-size "100" --metadata disable-legacy-endpoints=true --scopes "https://www.googleapis.com/auth/devstorage.read_only","https://www.googleapis.com/auth/logging.write","https://www.googleapis.com/auth/monitoring","https://www.googleapis.com/auth/servicecontrol","https://www.googleapis.com/auth/service.management.readonly","https://www.googleapis.com/auth/trace.append" --num-nodes "1" --enable-cloud-logging --enable-cloud-monitoring --no-enable-ip-alias --network "projects/cl-syd-ml-writers/global/networks/default" --subnetwork "projects/cl-syd-ml-writers/regions/australia-southeast1/subnetworks/default" --addons HorizontalPodAutoscaling,HttpLoadBalancing --no-enable-autoupgrade --enable-autorepair
```

