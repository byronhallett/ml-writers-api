from os import getenv
from flask import Flask, request, jsonify
import modules.generate as gen
from re import sub
from modules.download_model import download_model
from modules.generate import State, predict

BATCH_LENGTH = 8
MAX_LENGTH = 512

app = Flask(__name__)

loaded_model: State = None


def load_model():
    global loaded_model
    if loaded_model is None:
        download_model(bucket_name=getenv('BUCKET_NAME'))
        loaded_model = gen.interact_model(
            length=int(BATCH_LENGTH),
            temperature=float(getenv("TEMPERATURE")))


@app.route('/predict')
def predict_from_seed() -> str:
    # Get user args and complain if incorrect
    r_seed = request.args.get('seed')
    r_length = request.args.get('length')
    r_stop_chars = request.args.get('stop_chars')
    r_stop_string = request.args.get('stop_string')
    if (r_seed is None or
            (r_length is None and r_stop_chars is None and
             r_stop_string is None)):
        return ("PARAMS: <BR>"
                "seed str eg. hows%20it%20going AND<br>"
                "length int eg. 32 OR<br>"
                "stop_chars str eg. ?!. OR<br>"
                "stop_string str eg. <EOS>")

    # Ensure we have the global model in mem
    if loaded_model is None:
        load_model()

    # Clean up args for usewith defaults
    tmp_seed: str = r_seed
    length: int = MAX_LENGTH if r_length is None else int(r_length)
    stop_chars: str = r_stop_chars
    stop_string: str = r_stop_string

    # iterate to produce results stopping when requested
    prediction: str = ""
    stop_reason: str = "length_met"
    for _ in range(0, length+1, BATCH_LENGTH):
        tmp_prediction = predict(loaded_model, tmp_seed)
        prediction += tmp_prediction
        if stop_string is not None and stop_string in prediction:
            stop_reason = "stop_string_found"
            prediction = sub(stop_string+r".*", stop_string, prediction)
            break
        if (stop_chars is not None and
                any(x in prediction for x in stop_chars)):
            stop_reason = "stop_char_found"
            prediction = sub(r"(["+stop_chars+r"]).*", r"\1", prediction)
            break
        tmp_seed += tmp_prediction

    return jsonify({
        "seed": r_seed,
        "prediction": prediction,
        "reason": stop_reason
    })


if __name__ == '__main__':
    # not used on app engine
    from dotenv import load_dotenv
    load_dotenv()
    app.run(host='127.0.0.1', port=8080, debug=True)
