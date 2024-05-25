from snake_env import SnakeEnv
from dqn_agent import DQNAgent
import numpy as np

if __name__ == "__main__":
    env = SnakeEnv()
    state_size = env.observation_space.shape[0]
    action_size = env.action_space.n
    agent = DQNAgent(state_size, action_size)
    batch_size = 1

    for e in range(1000):
        state = env.reset()  # Reinicializa o ambiente
        state = np.reshape(state, [1, state_size])
        done = False
        time = 0
        
        while not done and time < 500:
            env.game.render(e)
            action = agent.act(state)
            next_state, reward, done, _ = env.step(action)
            reward = reward if not done else -10
            next_state = np.reshape(next_state, [1, state_size])
            agent.remember(state, action, reward, next_state, done)
            state = next_state
            time += 1

            if len(agent.memory) > batch_size:
                agent.replay(batch_size)
        
        # Exibe estatísticas após cada episódio
        if done:
            print(f"Episode: {e}/{1000}, Score: {time}, Epsilon: {agent.epsilon:.2f}")

        # Salva o modelo a cada 50 episódios
        if e % 50 == 0:
            agent.save(f"snake-dqn-{e}.weights.h5")
