from stable_baselines3 import DQN
from simulator import WorkloadSimulator
import gym
from gym import spaces
import numpy as np

class ScalingEnv(gym.Env):
    def __init__(self):
        super(ScalingEnv, self).__init__()
        self.sim = WorkloadSimulator()
        self.action_space = spaces.Discrete(3)  # down, up, nothing
        self.observation_space = spaces.Box(low=0, high=1, shape=(1,), dtype=np.float32)

    def reset(self):
        self.sim = WorkloadSimulator()
        return self.sim.load

    def step(self, action):
        obs, reward, done, info = self.sim.step(action)
        return obs, reward, done, info

env = ScalingEnv()
model = DQN('MlpPolicy', env, verbose=1)
model.learn(total_timesteps=50000)
model.save("drl_scaler")
