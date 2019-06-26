import os
from google.cloud import storage

# CONSTS
FILES = [
    'checkpoint', 'encoder.json', 'hparams.json',
    'model.ckpt.data-00000-of-00001', 'model.ckpt.index',
    'model.ckpt.meta', 'vocab.bpe'
]
# Instantiates a client
storage_client = storage.Client()


def download_model(bucket_name=os.environ['BUCKET_NAME']):
    """Downloads model data from our bucket"""
    bucket = storage_client.get_bucket(bucket_name)
    for filename in FILES:
        print("=== downloading " + filename, end='\r')
        blob = bucket.blob(filename)
        blob.download_to_filename("/tmp/"+filename)
        print("=== Finished downloading ", filename)

