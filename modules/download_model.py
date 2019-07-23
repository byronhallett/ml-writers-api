from google.cloud import storage
from os import getenv, path


# CONSTS
FILES = [
    'checkpoint', 'encoder.json', 'hparams.json',
    'model.ckpt.data-00000-of-00001', 'model.ckpt.index',
    'model.ckpt.meta', 'vocab.bpe'
]


def download_model(bucket_name: str, skip_if_exists: bool = False):
    """Downloads model data from our bucket"""
    # Instantiates a client
    storage_client = storage.Client.from_service_account_json(
        'service_account.json')
    bucket = storage_client.get_bucket(bucket_name)
    for filename in FILES:
        blob = bucket.blob(filename)
        filepath = "./"+filename
        # save startup time if we already have the file
        if skip_if_exists and path.exists(filepath):
            print("=== Skipped ", filename)
            continue
        print("=== downloading " + filename)
        blob.download_to_filename(filepath)
        print("Done;", filename)


if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv()
    download_model(bucket_name=getenv('BUCKET_NAME'), skip_if_exists=False)
