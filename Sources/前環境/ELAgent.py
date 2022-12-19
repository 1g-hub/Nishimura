import numpy as np
import matplotlib.pyplot as plt

class ELAgent():

    def __init__(self, epsilon):
        self.Q = {}
        self.epsilon = epsilon
        self.reward_log = []

    def policy(self, s, actions):
        if np.random.random() < self.epsilon:
            # ランダムな行動（探索）
            return np.random.randint(len(actions))
        else:
            # self.Q => 状態における行動の価値
            # self.Q[s] => 状態sで行動aをとる場合の価値
            if s in self.Q and sum(self.Q[s]) != 0:
                # 価値評価に基づき行動（活用）
                return np.argmax(self.Q[s])
            else:
                # ランダムな行動（探索）
                return np.random.randint(len(actions))

    # 報酬の記録を初期化
    def init_log(self):
        self.reward_log = []

    # 報酬の記録
    def log(self, reward):
        self.reward_log.append(reward)

    def show_reward_log(self, interval=6000, episode=-1):
        # そのepsilonの報酬をグラフ表示
        if episode > 0:
            rewards = self.reward_log[-interval:]
            mean = np.round(np.mean(rewards), 3)
            std = np.round(np.std(rewards), 3)
            print("At Episode {} average reward is {} (+/-{}).".format(
                   episode, mean, std))
        # 今までに獲得した報酬をグラフ表示
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
            plt.grid()
            plt.fill_between(indices, means - stds, means + stds,
                             alpha=0.1, color="g")
            plt.plot(indices, means, "o-", color="g",
                     label="Rewards for each {} episode".format(interval))
            plt.legend(loc="best")
            plt.savefig("MCS.png", format="png", dpi=300)