from CardGameEnv import CardGameEnv
import numpy as np
import sys
import matplotlib.pyplot as plt
from collections import defaultdict

class Agent():
    def __init__(self, epsilon):
        self.Q = {}
        self.epsilon = epsilon
        self.reward_log = []

    def policy(self, state, actions):
        if np.random.random() < self.epsilon:
            return np.random.randint(len(actions))
        else:
            print(state)
            print(self.Q)
            if state in self.Q and sum(self.Q[state]) != 0:
                return np.argmax(self.Q[state])
            else:
                return np.random.randint(len(actions))

    def init_log(self):
        self.reward_log = []

    def log(self, reward):
        self.reward_log.append(reward)

    def show_reward_log(self, interval=100, episode=-1):
        if episode > 0:
            rewards = self.reward_log[-interval:]
            mean = np.round(np.mean(rewards), 3)
            std = np.round(np.std(rewards), 3)
            print("At Episode {} average reward is {} (+/-{}).".format(episode, mean, std))
        else:
            indices = list(range(0, len(self.reward_log), interval))
            means = []
            stds = []
            for i in indices:
                rewards = self.reward_log[i:(i + interval)]
                means.append(np.mean(rewards))
                stds.append(np.std(rewards))
            means = np.array(means)
            stds = np.array(stds)
            plt.figure()
            plt.title("Reward History")
            plt.xlabel("episode")
            plt.ylabel("reward")
            plt.grid()
            plt.fill_between(indices, means - stds, means + stds, alpha=0.2, color="g")
            plt.plot(indices, means, "o-", color="g", label="Rewards for each {} episode".format(interval))
            plt.legend(loc="best")
            plt.savefig("Reward_History.png")
            plt.show()

class QLearningAgent(Agent):
    def __init__(self, epsilon=0.1):
        super().__init__(epsilon)

    def learn(self, env, episode_count=1000, gamma=0.9,
              learning_rate=0.1, render=False, report_interval=5000):
        self.init_log()
        actions = list(range(env.action_space.n))
        self.Q = defaultdict(lambda: [0] * len(actions))
        for e in range(episode_count):
            s = env.reset()
            done = False
            reward_history = []
            while not done:
                if render:
                    env.render()
                a = self.policy(s, actions)
                n_state, reward, done, info = env.step(a)

                reward_history.append(reward)
                gain = reward + gamma * max(self.Q[n_state])
                estimated = self.Q[s][a]
                self.Q[s][a] += learning_rate * (gain - estimated)
                s = n_state
            else:
                self.log(sum(reward_history))

            if e != 0 and e % report_interval == 0:
                self.show_reward_log(episode=e, interval=50)
        env.close()

def train():
    agent = QLearningAgent()
    env = CardGameEnv()
    agent.learn(env, episode_count=50000, report_interval=1000)
    #agent.save_Q()
    agent.show_reward_log(interval=500)

if __name__ == "__main__":
    train()
