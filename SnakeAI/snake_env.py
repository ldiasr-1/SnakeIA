import gym
from gym import spaces
from snake_game import SnakeGame
import numpy as np

class SnakeEnv(gym.Env):
    def __init__(self):
        super(SnakeEnv, self).__init__()
        self.game = SnakeGame()
        self.observation_space = spaces.Box(low=0, high=max(600, 400), shape=(6,), dtype=np.float32)
        self.action_space = spaces.Discrete(4)
    
    def reset(self):
        return self.game.reset()
    
    def step(self, action):
        state, reward, done = self.game.step(action)
        return state, reward, done, {}
    
    def render(self, mode='human', close=False):
        self.game.render()

env = SnakeEnv()
