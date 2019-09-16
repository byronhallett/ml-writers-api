# BLURB BLOCKS API

## INSTALL

```sh
# USE A PYTHON3 ENV
BUCKET_NAME=blurb-blocks
TEMPERATURE=0.8
BATCH_LENGTH=16
CUDA_VISIBLE_DEVICES=0
pip install -r requirements.txt
python main.py
```

## GCE Docker container deployment

- Head to the technology section of this drive project for the json security key
https://drive.google.com/open?id=1IYHRGzLtGaKB7WK1KyBwQ8x92dsj8nLT

- To get the image to gcloud, run push_to_container.sh

- Place the appropriate GPT2 data into a gcloud storage bucket in the same project

- Set up a GCE VM on gcloud

- run push_to_vm.sh, edit as required

- ssh into container eg `gcloud beta compute --project "cl-syd-ml-writers" ssh --zone "australia-southeast1-a" "ml-api-vm-1"`

- edit docker-compose.yml so that each BUCKET_NAME variable points at the same buckets as above.

- start the containers with `docker-compose up`

## Updating models

To update, SSH into the VM as above, locate the folder with the same name as the relevant model's bucket. Delete or rename that folder. Restart the docker containers by runnning `docker-compose restart`

## Licenses

This repo is a modified version of https://github.com/openai/gpt-2

Main changes:
- Addition of uwsgi server (flask) to serve over http
  - Includes optimisations
    - Load models once into GPU mem on startup
    - Make much smaller predictions on GPT2 to facilitate iterative prediction, streamed responses and allow internal context aware prediction limiting (users can specific strings to end prediction before response is returned)
- Addtion of gcloud specific logic to download models from cloud storage buckets
- Additon of the following files to configure host VM on gcloud:
  - docker-compose.yml
  - push_to_container_reg.sh
  - push_to_vm.sh
  - tmux.sh
  - traefik.toml

| Name        | Version  | Modified?  | License and URL
| ----------- |:--------:|:--:| -----:|
| google-cloud-storage | 1.16.1 | NO | [Apache 2.0](https://github.com/googleapis/google-cloud-python/blob/master/LICENSE) |
| Flask | 1.1.1 | NO | [BSD-3-Clause ](https://palletsprojects.com/license/) |
| Flask-Cors | 3.0.8 | NO | [MIT](https://github.com/corydolphin/flask-cors/blob/master/LICENSE) |
| requests| 2.22.0 | NO | [Apache 2.0](https://pypi.org/project/requests/) |
| uWSGI | 2.0.18 | NO | [GPLv2+](https://uwsgi-docs.readthedocs.io/en/latest/) |
| tensorflow | 1.14.0 | NO | [Apache 2.0](https://github.com/tensorflow/tensorflow/blob/master/LICENSE) |
