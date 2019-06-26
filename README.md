# BLURB BLOCKS API

## INSTALL (TAKES PLACE AUTOMATTICALLY ON APP-ENGINE)
Install python packages:
```
pip3 install -r requirements.txt
```
Download the model data from URI, eg
```
python3 download_model.py https://storage.cloud.google.com/cl-syd-playground/blurb-blocks-data
```

# CONFIG
```sh
# override text encoding
export PYTHONIOENCODING=UTF-8
```

## Sample generation
To generate unconditional samples:
```sh
# See flags
python3 src/generate_unconditional_samples.py -- --help
# Generate into stout
python3 src/generate_unconditional_samples.py --top_k 40 --temperature 0.7
```

To give the model custom prompts, you can use:
```sh
# See flags
python3 src/interactive_conditional_samples.py -- --help
# Generate into stout
python3 src/interactive_conditional_samples.py --top_k 40
```

