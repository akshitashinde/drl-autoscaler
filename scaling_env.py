import gym
from gym import spaces
import numpy as np

class ScalingEnv(gym.Env):
    def __init__(self):
        super(ScalingEnv, self).__init__()
        
        # 3 actions: scale down (0), stay (1), scale up (2)
        self.action_space = spaces.Discrete(3)

        # 1 observation: CPU load (from 0 to 100)
        self.observation_space = spaces.Box(low=0, high=100, shape=(1,), dtype=np.float32)

        # Start with medium CPU load
        self.state = 50.0
        self.replicas = 3

    def step(self, action):
        # Apply the action
        if action == 0:
            self.replicas = max(1, self.replicas - 1)
        elif action == 2:
            self.replicas += 1
        
        # Simulate new load
        workload = np.random.normal(50, 10)  # random load
        self.state = workload / self.replicas  # more replicas = less load per replica

        # Calculate reward
        reward = -(self.replicas * 0.2)  # cost for each replica
        if self.state > 70:
            reward -= 5  # penalty for too high CPU load

        done = False  # We don't "end" this simulation, it keeps going
        info = {}

        return np.array([self.state], dtype=np.float32), reward, done, info

    def reset(self):
        # Reset environment to starting conditions
        self.state = 50.0
        self.replicas = 3
        return np.array([self.state], dtype=np.float32)