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

For gcloud, edit the **app.yaml**