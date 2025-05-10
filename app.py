from flask import Flask, request, jsonify
from stable_baselines3 import DQN
import numpy as np
import os

app = Flask(__name__)

MODEL_PATH = "drl_scaler.zip"

# Check model existence
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model file {MODEL_PATH} not found")

# Load the model
model = DQN.load(MODEL_PATH)

@app.route('/')
def home():
    return "✅ Flask DRL Scaler Service is Running!"

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json(force=True)

        if 'load' not in data:
            return jsonify({'error': "Missing 'load' in request"}), 400

        obs = np.array([[data['load']]], dtype=np.float32)  # shape (1, 1)
        obs = obs.reshape(1, 1)  # DQN expects (n_env, obs_dim)
        action, _ = model.predict(obs, deterministic=True)
        return jsonify({'action': int(action)})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
