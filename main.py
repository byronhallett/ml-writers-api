from os import getenv
from flask import Flask, request, jsonify
import modules.generate as gen
from modules.download_model import download_model
from modules.generate import State, predict

app = Flask(__name__)

loaded_model: State = None


@app.before_request
def load_model():
    try:
        global loaded_model
        if loaded_model is None:
            download_model(bucket_name=getenv('BUCKET_NAME'))
            loaded_model = gen.interact_model(
                length=int(getenv("SEED_LENGTH")),
                temperature=float(getenv("TEMPERATURE")))
    except Exception as e:
        app.log_exception(e)


@app.route('/predict')
def predict_from_seed() -> str:
    try:
        seed: str = request.args.get('seed')
        prediction = predict(loaded_model, seed)
        return jsonify({
            "seed": seed,
            "prediction": prediction
        })
    except Exception as e:
        app.log_exception(e)


if __name__ == '__main__':
    # not used on app engine
    from dotenv import load_dotenv
    load_dotenv()
    app.run(host='127.0.0.1', port=8080, debug=True)
