# BLURB BLOCKS API

## INSTALL

locally
```sh
# USE A PYTHON3 ENV
pip install -r requirements.txt
python main.py
```

## CONFIG

Locally, add a .env with example
```sh
BUCKET_NAME=blurb-blocks
TEMPERATURE=0.8
BATCH_LENGTH=16
CUDA_VISIBLE_DEVICES=0
```

## GCE Docker container deployment

- Head to the technology section of this drive project for the json security key
https://drive.google.com/open?id=1IYHRGzLtGaKB7WK1KyBwQ8x92dsj8nLT

- To get the image to gcloud, run push_to_container.sh

- after setting up a VM, install docker-compose there
- run push_to_vm.sh, edit as required

- ssh into container and run:

```sh
docker-compose up
```