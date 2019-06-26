import os
import sys
import requests
from tqdm import tqdm

# CONSTS
SUBDIR = 'model'
FILES = [
    'checkpoint', 'encoder.json', 'hparams.json',
    'model.ckpt.data-00000-of-00001', 'model.ckpt.index',
    'model.ckpt.meta', 'vocab.bpe'
]


def download(BUCKET_FOLDER_URI):
    for filename in FILES:
        r = requests.get(BUCKET_FOLDER_URI + "/" + filename, stream=True)
        with open(os.path.join(SUBDIR, filename), 'wb') as f:
            file_size = int(r.headers["content-length"])
            chunk_size = 1000
            with tqdm(ncols=100, desc="Fetching " + filename,
                      total=file_size, unit_scale=True) as pbar:
                # 1k for chunk_size,
                # since Ethernet packet size is around 1500 bytes
                for chunk in r.iter_content(chunk_size=chunk_size):
                    f.write(chunk)
                    pbar.update(chunk_size)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print('You must enter the model URI as arg')
        sys.exit(1)
    if not os.path.exists(SUBDIR):
        os.makedirs(SUBDIR)
    download(BUCKET_FOLDER_URI=sys.argv[1])
