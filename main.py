from os import getenv
from typing import List, Dict
from re import findall, escape, sub, MULTILINE

from flask import Flask, request, Response, Request
from flask_cors.decorator import cross_origin

from modules.download_model import download_model
from modules.generate import State, predict
import modules.generate as gen

DEFAULT_BATCH_LENGTH = 8
DEFAULT_LENGTH = 512

app = Flask(__name__)
loaded_model: State = None


@app.route('/touch', methods=["GET", "POST"])
@cross_origin()
def touch_server():
    '''
    Can be optionally called from a frontend to pre-load the model
    '''
    # Ensure we have the global model in mem
    load_model()
    return "No Touch"


@app.route('/predict', methods=["POST"])
@cross_origin()
def predict_from_seed() -> str:
    req: Request = request
    data_json: Dict[str, str] = req.json
    # Get user args and complain if incorrect
    r_seed = data_json.get('seed')
    r_length = data_json.get('length')
    r_stop_chars = data_json.get('stop_chars')
    r_stop_string = data_json.get('stop_string')
    r_stop_count = data_json.get('stop_count')

    if (r_seed is None or
            (r_length is None and r_stop_chars is None and
             r_stop_string is None)):
        return ("PARAMS: <BR>"
                "seed str eg. hows%20it%20going AND<br>"
                "length int eg. 32 OR<br>"
                "stop_chars str eg. ?!. OR<br>"
                "stop_string str eg. <EOS><br>"
                "(optional) stop_count eg. 2")

    # Ensure we have the global model in mem
    load_model()

    # Clean up args for usewith defaults
    length: int = DEFAULT_LENGTH if r_length is None else int(r_length)
    stop_chars: str = r_stop_chars
    stop_string: str = r_stop_string
    stop_count: int = 1 if r_stop_count is None else int(r_stop_count)

    def generate():
        # iterate to produce results stopping when requested
        tmp_seed: str = r_seed
        prediction: str = ""
        # stop_reason: str = "length_met"
        for _ in range(0, length + 1, batch_length()):
            # Make next prediction and update seed
            tmp_prediction = predict(loaded_model, tmp_seed)
            prediction += tmp_prediction
            tmp_seed += tmp_prediction

            # check for stop conditions in the new prediction
            string_check = check_stop_string(stop_string, prediction,
                                             stop_count)
            chars_check = check_stop_char(stop_chars, prediction, stop_count)

            # trim from end delimiter for our last iteration only
            # last iter will have one of the following
            if string_check:
                tmp_prediction = stripFromLastOf([stop_string], tmp_prediction)
            if chars_check:
                tmp_prediction = stripFromLastOf([c for c in stop_chars],
                                                 tmp_prediction)

            yield tmp_prediction
            # break if any met
            if string_check or chars_check:
                break

    if bool(getenv("STREAM")):
        return Response(generate())
    else:
        return "".join([x for x in generate()])


def stripFromLastOf(patterns: List[str], string: str) -> str:
    temp = string
    for p in patterns:
        temp = sub(escape(p)+".*?$", p, temp, flags=MULTILINE)
    return temp


def check_stop_string(stop_string: str, prediction: str, count: int) -> bool:
    '''
    Returns true if the requisite number of exact matches are found
    returns the string up to the last match
    '''
    return (stop_string is not None and
            len(findall(escape(stop_string), prediction)) >= count)


def check_stop_char(stop_chars: str, prediction: str, count: int) -> bool:
    '''
    Returns true if the requisite number of match on any char is found
    returns the string up to the last match
    '''
    return (stop_chars is not None and
            len(findall("["+escape(stop_chars)+"]", prediction)) >= count)


def load_model():
    global loaded_model
    if loaded_model is None:
        download_model(bucket_name=getenv('BUCKET_NAME'), skip_if_exists=True)
        loaded_model = gen.interact_model(
            length=batch_length(),
            temperature=float(getenv("TEMPERATURE")))


def batch_length() -> int:
    if getenv("BATCH_LENGTH") is None:
        return DEFAULT_BATCH_LENGTH
    else:
        return int(getenv("BATCH_LENGTH"))


if __name__ == '__main__':
    # not used on app engine
    from dotenv import load_dotenv
    load_dotenv()
    app.run(host='127.0.0.1', port=8080, debug=True)
