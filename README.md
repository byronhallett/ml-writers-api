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
```

For gcloud app engine, edit the to of **app.yaml**
```yaml
service: blurb-blocks-api
env_variables:
  BUCKET_NAME: "blurb-blocks"
  TEMPERATURE: "0.8"
```

## GAE flex deployment

## THIS IS THE MAIN DEPLOYMENT TYPE AT THE MOMENT

```sh
gcloud app deploy --quiet --project cl-syd-ml-writers
```

## GCE deployment (Currently not working)

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

## GCE Docker container deployment

Head to the technology section of this drive project for the json security key
https://drive.google.com/open?id=1IYHRGzLtGaKB7WK1KyBwQ8x92dsj8nLT

** INCOMPLETE **

