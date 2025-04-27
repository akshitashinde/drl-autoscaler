from flask import Flask, request, jsonify
from stable_baselines3 import DQN
import numpy as np

app = Flask(__name__)
model = DQN.load("drl_scaler")

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    load = np.array([data['load']])
    action, _ = model.predict(load, deterministic=True)
    return jsonify({'action': int(action)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
