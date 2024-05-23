from snake_env import SnakeEnv
from dqn_agent import DQNAgent
import numpy as np

if __name__ == "__main__":
    env = SnakeEnv()
    state_size = env.observation_space.shape[0]
    action_size = env.action_space.n
    agent = DQNAgent(state_size, action_size)
    done = False
    batch_size = 32
    

    for e in range(1000):
        state = env.reset()
        state = np.reshape(state, [1, state_size])
        for time in range(500):
            env.render()
            action = agent.act(state)
            next_state, reward, done, _ = env.step(action)
            reward = reward if not done else -10
            next_state = np.reshape(next_state, [1, state_size])
            agent.remember(state, action, reward, next_state, done)
            state = next_state
            if done:
                break  # Exit the loop when the game is over
            
            if len(agent.memory) > batch_size:
                agent.replay(batch_size)
        
        if e % 50 == 0:
            agent.save(f"snake-dqn-{e}.h5")