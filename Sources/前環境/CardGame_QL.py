import gym
import pickle
import os
import rl.core
import numpy as np
import matplotlib.pyplot as plt
from QLAgent import QLAgent
from CardGameEnv import CardGameEnv
import rl.callbacks
# call back も設定できる
class EpisodeLogger(rl.callbacks.Callback):
    def __init__(self):
        self.observations = {}
        self.rewards = {}
        self.actions = {}
 
    def on_episode_begin(self, episode, logs):
        self.observations[episode] = []
        self.rewards[episode] = []
        self.actions[episode] = []
 
    def on_step_end(self, step, logs):
        episode = logs['episode']
        self.observations[episode].append(logs['observation'])
        self.rewards[episode].append(logs['reward'])
        self.actions[episode].append(logs['action'])
cb_ep = EpisodeLogger()

env = CardGameEnv()
nb_actions = env.action_space.n  # PendulumProcessorで5個と定義しているので5

# processorはAgentのコンストラクタの引数で渡します。
agent = QLAgent(nb_actions=nb_actions, traning_rate=0.5, gamma=0.99, epsilon=0.1)
agent.compile()


# 訓練
print("--- start ---")
print("'Ctrl + C' is stop.")
history = agent.fit(env, nb_steps=1000000, visualize=False, verbose=1)

# 結果を表示
'''
plt.subplot(2,1,1)
plt.plot(history.history["nb_episode_steps"])
plt.yscale("log")
plt.ylabel("step")

plt.subplot(2,1,2)
plt.plot(history.history["episode_reward"])
plt.xlabel("episode")
plt.yscale("log")
plt.ylabel("reward")

plt.savefig("cardgameQL.png", format="png", dpi=300)
'''

# 訓練結果を見る
scores = agent.test(env, nb_episodes=1000, visualize=False, callbacks=[cb_ep])
#print(np.mean(scores.history['episode_reward']))

win_sum = 0
draw_sum = 0
loss_sum = 0

for obs in cb_ep.rewards.values():
    if obs[-1] == 10.0:
        win_sum += 1
    elif obs[-1] == -10.0:
        loss_sum += 1
    else:
        draw_sum += 1

print("win_sum")
print(win_sum)
print("draw_sum")
print(draw_sum)
print("loss_sum")
print(loss_sum)


print("win rate")
print(win_sum / 10.0)
plt.savefig("score.png", format="png", dpi=300)