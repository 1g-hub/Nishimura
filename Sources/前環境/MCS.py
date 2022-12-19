import math
import gym
from ELAgent import ELAgent
import numpy as np
from CardGameEnv import CardGameEnv

class MonteCarloAgent(ELAgent):

    def __init__(self, epsilon=0.1):
        super().__init__(epsilon)

    def learn(self, env, episode_count=1000, gamma=0.9,traning_rate = 0.5,
              render=False, report_interval=50):
        self.init_log()
        actions = list(range(env.action_space.n))
        self.Q[""] = [np.random.uniform(low=-1, high=1) for _ in range(env.action_space.n)]

        for e in range(episode_count):
            s = env.reset()
            done = False
            # エピソードの終了まで実行する
            experience = []
            while not done:
                # 文字列化して一意にする。
                s = "_".join([str(o) for o in s])
                # Qテーブルになければ追加(無限に増えます)
                if s not in self.Q:
                    # Q値の初期化
                    self.Q[s] = [ np.random.uniform(low=-1, high=1) for _ in range(env.action_space.n) ]
                a = self.policy(s, actions)
                n_state, reward, done, info = env.step(a)
                experience.append({"state": s, "action": a, "reward": reward})
                s = n_state
            else:
                self.log(reward)

            #print(experience)
            # 各状態・各行動を評価する。
            for i, x in enumerate(experience):
                s, a = x["state"], x["action"]
            
                # Calculate discounted future reward of s.
                # 状態ｓ
                G ,t = 0 , 0
                for j in range(i, len(experience)):
                    G += math.pow(gamma,t) * experience[j]["reward"]

                self.Q[s][a] += traning_rate * (G - self.Q[s][a])

            if e != 0 and e % report_interval == 0:
                self.show_reward_log(episode=e)

    def test(self, env, episode_count = 10000):
        win_count = 0
        loss_count = 0
        for e in range(episode_count):
            s = env.reset()
            done = False
            final_reward = 0
            while not done:
                # 文字列化して一意にする。
                s = "_".join([str(o) for o in s])
                # Qテーブルになければ追加(無限に増えます)
                if s not in self.Q:
                    # Q値の初期化
                    self.Q[s] = [ np.random.uniform(low=-1, high=1) for _ in range(env.action_space.n) ]
                a = np.argmax(self.Q[s])
                n_state, reward, done, info = env.step(a)
                s = n_state
                final_reward = reward
            #print(reward)
            if reward > 0.0:
                win_count += 1
            else:
                loss_count += 1
        print("win_count")
        print(win_count)
        print("loss_count")
        print(loss_count)
        print("win rate")
        print(win_count / episode_count)


def train():
    agent = MonteCarloAgent(epsilon=0.1)
    env = CardGameEnv()
    agent.learn(env, episode_count=600000)
    agent.show_reward_log()
    agent.test(env, episode_count = 10000)

if __name__ == "__main__":
    train()