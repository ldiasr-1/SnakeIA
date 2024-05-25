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
        self.last_action = None
    
    def reset(self):
        self.last_action = None
        return self.game.reset()
    
    def step(self, action):
        state, reward, done = self.game.step(action)
        
        # Calcula a distância entre a cabeça da cobra e a comida
        distance = np.sqrt((state[0] - state[2])**2 + (state[1] - state[3])**2)
        
        # Ajusta a recompensa com base na proximidade da cobra à comida
        if distance < 20:  # Se estiver muito perto da comida
            reward += 5  # Aumenta a recompensa
        
        return state, reward, done, {}
