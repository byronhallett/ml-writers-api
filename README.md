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

## Kubernetes engine config

Head to the technology section of this drive project for the json security key
https://drive.google.com/open?id=1IYHRGzLtGaKB7WK1KyBwQ8x92dsj8nLT

```sh
gcloud beta container --project "cl-syd-ml-writers" clusters create "blurb-blocks-api" --zone "australia-southeast1-c" --no-enable-basic-auth --cluster-version "1.12.8-gke.10" --machine-type "n1-highmem-2" --accelerator "type=nvidia-tesla-p100,count=1" --image-type "COS" --disk-type "pd-standard" --disk-size "100" --metadata disable-legacy-endpoints=true --scopes "https://www.googleapis.com/auth/devstorage.read_only","https://www.googleapis.com/auth/logging.write","https://www.googleapis.com/auth/monitoring","https://www.googleapis.com/auth/servicecontrol","https://www.googleapis.com/auth/service.management.readonly","https://www.googleapis.com/auth/trace.append" --num-nodes "1" --enable-cloud-logging --enable-cloud-monitoring --no-enable-ip-alias --network "projects/cl-syd-ml-writers/global/networks/default" --subnetwork "projects/cl-syd-ml-writers/regions/australia-southeast1/subnetworks/default" --addons HorizontalPodAutoscaling,HttpLoadBalancing --no-enable-autoupgrade --enable-autorepair
```