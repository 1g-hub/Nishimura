import gym
from rl.agents.dqn import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.policy import EpsGreedyQPolicy
from rl.memory import SequentialMemory
from rl.processors import MultiInputProcessor
from CardGameEnv import CardGameEnv
from tensorflow import keras
from keras.optimizers import Adam
from keras.layers import Dense, Activation, Flatten, Input, concatenate
from keras.models import Sequential,Model
from keras.utils import plot_model
import numpy as np
import sys
import rl.callbacks
import matplotlib.pyplot as plt
 
# ログを記録するためのクラスの定義
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
env = CardGameEnv()
action_history = []
reward_history = []
nb_actions = env.action_space.n
#print(nb_actions)
print(env.observation_space)
#observation_value_list = list(env.observation_space.values())
#bservation_arr = np.empty(1,len(observation_value_list))
#for i in observation_value_list:
#    observation_arr.append(i)
#print(observation_arr)


#環境デバック用テストコード(CPUでも動く)
'''
for _ in range(200):
    action = env.action_space.sample()
    action_history.append(action)
    print("action.history: ")
    print(action_history)
    obs, re, done, info = env.step(action)
    reward_history.append(re)
    if done:
        action_history = []
        env.reset()
print(reward_history)
'''

# モデルの定義

model = Sequential()
model.add(Flatten(input_shape=(1,) + env.observation_space.shape))
model.add(Dense(16))
model.add(Activation('relu'))
model.add(Dense(16))
model.add(Activation('relu'))
model.add(Dense(16))
model.add(Activation('relu'))
model.add(Dense(nb_actions))
model.add(Activation('linear'))
plot_model(model, to_file='model.png')


# エージェントの設定
memory = SequentialMemory(limit=1000000, window_length=1)
policy = EpsGreedyQPolicy(eps=0.1)
dqn = DQNAgent(model=model, nb_actions=nb_actions, memory=memory, nb_steps_warmup=10,target_model_update=1e-2, policy=policy)
dqn.compile(Adam(lr=1e-3), metrics=['mae'])

# 学習
history = dqn.fit(env, nb_steps=10000, visualize=False, verbose=1)

# 評価
dqn.test(env, nb_episodes=10, visualize=False,nb_max_episode_steps=1000)

plt.subplot(2,1,1)
plt.plot(history.history["nb_episode_steps"])
plt.ylabel("step")

plt.subplot(2,1,2)
plt.plot(history.history["episode_reward"])
plt.xlabel("episode")
plt.ylabel("reward")

plt.savefig("sin.png", format="png", dpi=300)

sys.exit("学習おわ")

