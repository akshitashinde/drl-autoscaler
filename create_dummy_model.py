from stable_baselines3 import DQN
import gymnasium as gym  # updated!
import numpy as np

# Create environment
env = gym.make('CartPole-v1')

# Create model
model = DQN('MlpPolicy', env, verbose=1)
model.learn(total_timesteps=1000)

# Save model
model.save("drl_scaler")
