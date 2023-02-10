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
import math
from tqdm import tqdm

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
model = load_model('0131EnemyRandom.h5')

# エージェントの設定
memory = SequentialMemory(limit=100000, window_length=1)
policy = CustomAnnealedPolicy(EpsGreedyQPolicy(), attr='eps',
                                    value_max=1.0, value_min=0.05, value_decay = 50.0,value_test=0.00)
dqn = DQNAgent(model=model, nb_actions=env.action_space.n, memory=memory, gamma=.99, nb_steps_warmup=10000,target_model_update=0.5, policy=policy)
dqn.compile(Adam(lr=1e-3), metrics=['mae'])
dqn.training = False

#param
NB_EPISODES = 10000

#Env の isFirst をTrueにしておく！！
win_cnt = 0
lose_cnt = 0
win_rate = []
for i in tqdm(range(2)):
    i += 13
    win_rate = []
    for j in range(15):
        win_cnt = 0
        lose_cnt = 0
        for episode in range(NB_EPISODES):
            observation = env.load_model_reset(is_eilm=True, elim_num_pla=i, elim_num_ene=j)
            #print("Initial State")
            #print(observation)
            episode_reward = 0.0
            turn_num = 1
            while 1:
                #先攻プレイヤーの行動
                ###########################################
                #1ターン以降はドロー
                if turn_num != 1:
                    env.player.draw()
                valid_moves = env.get_valid_moves() 
                next_action = dqn.forward(observation)
                next_observation = env.get_state()
                #print("observation")
                #print(next_observation)
                #enemy_observation = env.get_enemy_observation()
                while valid_moves[next_action] != 39:
                    #print("action")
                    #print(valid_moves[next_action])
                    next_observation, reward, done , _  = env.step(next_action)
                    if done:
                        episode_reward = reward
                        break
                    #print("observation")
                    #print(next_observation)
                    next_action = dqn.forward(next_observation)
                    valid_moves = env.get_valid_moves()
                #ターン処理
                env.updatecost(env.player)
                env.reset_use(env.player)
                env.reset_see(env.player)
                if env.get_done():
                    break
                #print("actionが39や")
                #後攻プレイヤー
                #####################################################
                #ドロー
                env.player.enemy.draw()
                enemy_observation = env.get_enemy_state()
                #print("enemy_observation")
                #print(enemy_observation)
                enemy_valid_moves = env.get_enemy_valid_moves()
                enemy_next_action = dqn.forward(enemy_observation)
                while enemy_valid_moves[enemy_next_action] != 39:
                    #print("enemy_action")
                    #print(enemy_valid_moves[enemy_next_action])
                    enemy_observation, reward, done = env.enemy_step(enemy_next_action)
                    if done:
                        episode_reward = reward
                        break
                    #print("enemy_observation")
                    #print(enemy_observation)
                    enemy_next_action = dqn.forward(enemy_observation)
                    enemy_valid_moves = env.get_enemy_valid_moves()
                #ターン処理
                env.updatecost(env.player.enemy)
                env.reset_use(env.player.enemy)
                env.reset_see(env.player.enemy)
                if env.get_done():
                    break
                #print("enemy の action が 39 や")
                turn_num += 1
            if episode_reward == 1.0:
                win_cnt += 1
                #print("win")
            elif episode_reward == -1.0:
                lose_cnt += 1
                #print("lose")
            else:
                print("rewardが0のまま,バグってるぞ")
        #print("win_cnt")
        #print(win_cnt)
        #print("lose_cnt")
        #print(lose_cnt)
        #print("win_rate")
        #print(win_cnt / NB_EPISODES)
        win_rate.append(win_cnt / NB_EPISODES)
    print(str(i) + " : ")
    print(win_rate)

