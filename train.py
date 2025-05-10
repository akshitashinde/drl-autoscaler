from stable_baselines3 import DQN
from scaling_env import ScalingEnv

# Create an instance of your environment
env = ScalingEnv()

# Create a DQN agent with MLP policy
model = DQN('MlpPolicy', env, verbose=1)

# Train the model for 50,000 time steps
model.learn(total_timesteps=50000)

# Save the trained model
model.save("drl_scaler_model")