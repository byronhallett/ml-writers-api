from os import getenv
from flask import Flask, request, jsonify
import modules.generate as gen
from re import findall, escape
from modules.download_model import download_model
from modules.generate import State, predict
from flask_cors.decorator import cross_origin

BATCH_LENGTH = 8
DEFAULT_LENGTH = 512

app = Flask(__name__)
loaded_model: State = None


class Check:
    def __init__(self, found: bool = False, prediction: str = "no prediction"):
        self.found: bool = found
        self.sub_prediction: bool = prediction


def load_model():
    global loaded_model
    if loaded_model is None:
        download_model(bucket_name=getenv('BUCKET_NAME'), skip_if_exists=True)
        loaded_model = gen.interact_model(
            length=int(BATCH_LENGTH),
            temperature=float(getenv("TEMPERATURE")))


@app.route('/predict')
@cross_origin()
def predict_from_seed() -> str:
    # Get user args and complain if incorrect
    r_seed = request.args.get('seed')
    r_length = request.args.get('length')
    r_stop_chars = request.args.get('stop_chars')
    r_stop_string = request.args.get('stop_string')
    r_stop_count = request.args.get('stop_count')
    if (r_seed is None or
            (r_length is None and r_stop_chars is None and
             r_stop_string is None)):
        return ("PARAMS: <BR>"
                "seed str eg. hows%20it%20going AND<br>"
                "length int eg. 32 OR<br>"
                "stop_chars str eg. ?!. OR<br>"
                "stop_string str eg. <EOS>"
                "(optional) stop_count eg. 2")

    # Ensure we have the global model in mem
    if loaded_model is None:
        load_model()

    # Clean up args for usewith defaults
    tmp_seed: str = r_seed
    length: int = DEFAULT_LENGTH if r_length is None else int(r_length)
    stop_chars: str = r_stop_chars
    stop_string: str = r_stop_string
    stop_count: int = 1 if r_stop_count is None else int(r_stop_count)

    # iterate to produce results stopping when requested
    prediction: str = ""
    stop_reason: str = "length_met"
    for _ in range(0, length + 1, BATCH_LENGTH):
        # Make next prediction and update seed
        tmp_prediction = predict(loaded_model, tmp_seed)
        prediction += tmp_prediction
        tmp_seed += tmp_prediction

        # check for stop conditions in the new prediction
        string_check = check_stop_string(stop_string, prediction, stop_count)
        chars_check = check_stop_char(stop_chars, prediction, stop_count)

        # break if any met
        if string_check.found:
            stop_reason = "stop_string_found"
            # prediction = string_check.sub_prediction
            break
        if chars_check.found:
            stop_reason = "stop_char_found"
            # prediction = chars_check.sub_prediction
            break
    response = jsonify({
        "seed": r_seed,
        "prediction": prediction,
        "reason": stop_reason
    })
    return response


def check_stop_string(stop_string: str, prediction: str, count: int) -> Check:
    '''
    Returns true if the requisite number of exact matches are found
    returns the string up to the last match
    '''
    check = Check()
    if (stop_string is not None and
            len(findall(escape(stop_string), prediction)) >= count):
        check.found = True
        # check.sub_prediction = sub(
        #     stop_string+".*?$", stop_string, prediction)
    return check


def check_stop_char(stop_chars: str, prediction: str, count: int) -> Check:
    '''
    Returns true if the requisite number of match on any char is found
    returns the string up to the last match
    '''
    check = Check()
    if (stop_chars is not None and
            len(findall("["+stop_chars+"]", prediction)) >= count):
        check.found = True
        # check.sub_prediction = sub(
        #     "(["+stop_chars+"]).*?$", "\\1", prediction)
    return check


if __name__ == '__main__':
    # not used on app engine
    from dotenv import load_dotenv
    load_dotenv()
    app.run(host='127.0.0.1', port=8080, debug=True)
