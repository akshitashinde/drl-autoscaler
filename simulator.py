import numpy as np

class WorkloadSimulator:
    def __init__(self):
        self.load = np.random.uniform(0.3, 0.7)

    def step(self, action):
        if action == 0:  # Scale down
            self.load += np.random.uniform(-0.05, 0.1)
        elif action == 1:  # Scale up
            self.load += np.random.uniform(-0.1, 0.05)
        else:  # Do nothing
            self.load += np.random.uniform(-0.02, 0.02)

        self.load = np.clip(self.load, 0, 1)
        reward = -self.load if self.load > 0.8 else 1 - self.load
        return np.array([self.load]), reward, False, {}
