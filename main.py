from os import getenv
from flask import Flask, request, Response
import modules.generate as gen
# from modules.download_model import download_model
from modules.generate import State, predict

BATCH_LENGTH = 16

app = Flask(__name__)

loaded_model: State = None


def load_model():
    global loaded_model
    if loaded_model is None:
        # download_model(bucket_name=getenv('BUCKET_NAME'))
        loaded_model = gen.interact_model(
            length=int(BATCH_LENGTH),
            temperature=float(getenv("TEMPERATURE")))


@app.route('/predict')
def predict_from_seed() -> str:
    # Get user args

    try:
        request_seed = request.args.get('seed')
        length = int(request.args.get('length'))
    except Exception:
        return "please pass a seed (str) and length (int) param"
    # Ensure we have the global model in mem
    if loaded_model is None:
        load_model()

    # a nested generator for streamed results
    def gen(req_seed):
        seed: str = req_seed
        for _ in range(length // BATCH_LENGTH):
            prediction = predict(loaded_model, seed)
            seed += prediction
            yield prediction

    return Response(gen(request_seed))


if __name__ == '__main__':
    # not used on app engine
    from dotenv import load_dotenv
    load_dotenv()
    app.run(host='127.0.0.1', port=8080, debug=True)
