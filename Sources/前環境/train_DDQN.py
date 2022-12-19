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
env = CardGameEnv()
action_history = []
reward_history = []
nb_actions = env.action_space.n
step_count = 200000
#print(nb_actions)
print(env.observation)
#observation_value_list = list(env.observation_space.values())
#bservation_arr = np.empty(1,len(observation_value_list))
#for i in observation_value_list:
#    observation_arr.append(i)
#print(observation_arr)


#環境デバック用テストコード(CPUでも動く)
'''
for _ in range(10000):
    env.player.printisplayed()
    env.player.enemy.printisplayed()
    action = env.action_space.sample()
    action_history.append(action)
    #print("action.history: ")
    #print(action_history)
    obs, re, done, info = env.step(action)
    print("observation")
    print(env.observation)
    reward_history.append(re)
    if done:
        print("GAME END")
        print(reward_history)
        sys.exit("GAME END")
        env.reset()
print(reward_history)

'''
# モデルの定義

model = Sequential()
model.add(Flatten(input_shape=(1,) + env.observation_space.shape))
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dense(64))
model.add(Activation('relu'))
model.add(Dense(nb_actions))
model.add(Activation('linear'))
#plot_model(model, to_file='model.png')


# エージェントの設定
memory = SequentialMemory(limit=1000000, window_length=1)
policy = EpsGreedyQPolicy(eps=0.1)
dqn = DQNAgent(model=model, nb_actions=nb_actions, memory=memory, nb_steps_warmup=10,target_model_update=1e-2, policy=policy, enable_double_dqn=True)
dqn.compile(Adam(lr=1e-3), metrics=['mae'])

# 学習
history = dqn.fit(env, nb_steps=step_count, visualize=False, verbose=1)

# 評価
dqn.test(env, nb_episodes=10000, visualize=False,nb_max_episode_steps=100, callbacks = [episode_logger])

#モデルの保存
model.save(str(step_count)+'stepDDQNFirst.h5')

plt.subplot(2,1,1)
plt.plot(history.history["nb_episode_steps"])
plt.yscale("log")
plt.ylabel("step")

plt.subplot(2,1,2)
plt.plot(history.history["episode_reward"])
plt.xlabel("episode")

plt.ylabel("reward")

plt.savefig(str(step_count) + "DDQN.png", format="png", dpi=300)

win_sum = 0
loss_sum = 0

for obs in episode_logger.rewards.values():
    print(obs[-1])
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
sys.exit("学習おわり")
