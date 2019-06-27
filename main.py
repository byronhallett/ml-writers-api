from os import getenv
from flask import Flask, request, jsonify
import neural_net.generate as gen
from download_model import download_model
from neural_net.generate import State, predict

app = Flask(__name__)

loaded_model: State = None


@app.before_request
def load_model():
    global loaded_model
    if loaded_model is None:
        download_model(bucket_name=getenv('BUCKET_NAME'))
        loaded_model = gen.interact_model(
            length=int(getenv("SEED_LENGTH")),
            temperature=float(getenv("TEMPERATURE")))


@app.route('/predict')
def predict_from_seed() -> str:
    seed: str = request.args.get('seed')
    prediction = predict(loaded_model, seed)
    return jsonify({
        "seed": seed,
        "prediction": prediction
    })


if __name__ == '__main__':
    # not used on app engine
    from dotenv import load_dotenv
    load_dotenv()
    app.run(host='127.0.0.1', port=8080, debug=True)
