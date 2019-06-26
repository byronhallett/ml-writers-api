from flask import Flask, request
import neural_net.generate as gen
from download_model import download_model
from neural_net.generate import State

app = Flask(__name__)

loaded_model: State = None


@app.before_request
def load_model():
    global loaded_model
    if loaded_model is None:
        download_model()
        loaded_model = gen.interact_model(length=32, temperature=0.8)


@app.route('/generate_from')
def generate_from() -> str:
    seed: str = request.args.get('seed')
    return "based on {}, I am your predicted output!".format(seed)


if __name__ == '__main__':
    # not used on app engine
    app.run(host='127.0.0.1', port=8080, debug=True)
