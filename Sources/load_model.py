import gym
from rl.agents.dqn import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.policy import EpsGreedyQPolicy
from rl.memory import SequentialMemory
from rl.processors import MultiInputProcessor
from CardGameEnv import CardGameEnv
from CardGameEnv2 import CardGameEnv2
from tensorflow import keras
from keras.optimizers import Adam
from keras.layers import Dense, Activation, Flatten, Input, concatenate
from keras.models import Sequential,Model
from keras.utils import plot_model
from CustomEpsGreedy import CustomAnnealedPolicy
import numpy as np
import sys
import rl.callbacks
import matplotlib.pyplot as plt
from tensorflow.python.keras.models import load_model

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


episode_logger = EpisodeLogger()
# 環境の生成
env = CardGameEnv2()

#モデルを読み込み
model = load_model('01170101NewDeck.h5')

# エージェントの設定
memory = SequentialMemory(limit=100000, window_length=1)
policy = CustomAnnealedPolicy(EpsGreedyQPolicy(), attr='eps',
                                    value_max=1.0, value_min=0.05, value_decay = 50.0,value_test=0.00)
dqn = DQNAgent(model=model, nb_actions=env.action_space.n, memory=memory, gamma=.99, nb_steps_warmup=10000,target_model_update=0.5, policy=policy)
dqn.compile(Adam(lr=1e-3), metrics=['mae'])

'''
winratelist = []
for _ in range(5):

print(winratelist)
'''
'''
# ( 5 エピソード実行確認用)
history = dqn.test(env, nb_episodes=3, visualize=False,nb_max_episode_steps=200, callbacks = [episode_logger])
print(history.history["episode_reward"])
'''
# 評価(10000回勝率計算)
dqn.test(env, nb_episodes=10000, visualize=False,nb_max_episode_steps=500, callbacks = [episode_logger])


win_sum = 0
loss_sum = 0

for obs in episode_logger.rewards.values():
    #print(obs)
    if obs[-1] > 0.0:
        win_sum += 1
    else:
        loss_sum += 1

print("win_sum")
print(win_sum)
print("loss_sum")
print(loss_sum)


print("win rate")
print(win_sum / 10000.0)
