import gym
import pickle
import os
import rl.core
import numpy as np
import matplotlib.pyplot as plt


class QLAgent(rl.core.Agent):
    def __init__(self, nb_actions, traning_rate=0.5, gamma=0.99, epsilon=0.1, **kwargs):
        super(QLAgent, self).__init__(**kwargs)
        self.compiled = False

        self.nb_actions = nb_actions

        self.q_table = {}
        self.q_table[""] = [np.random.uniform(low=-1, high=1) for _ in range(self.nb_actions)]

        self.traning_rate = traning_rate
        self.gamma = gamma

        self.epsilon = epsilon

    
    def reset_states(self):
        self.prev_observation  = ""
        self.prev_action = 0
        self.prev_reward = 0
        #print("q_table")
        #print(self.q_table)

    def compile(self, optimizer=None, metrics=[]):
        self.compiled = True
   
    def load_weights(self, filepath):
        with open(filepath, 'rb') as f:
            self.q_table = pickle.load(f)

    def save_weights(self, filepath, overwrite=False):
        if overwrite or not os.path.isfile(filepath):
            with open(filepath, 'wb') as f:
                pickle.dump(self.q_table, f)

    def forward(self, observation):
        # 文字列化して一意にする。
        observation = "_".join([str(o) for o in observation])
        
        # Qテーブルになければ追加(無限に増えます)
        if observation not in self.q_table:
            # Q値の初期化
            self.q_table[observation] = [ np.random.uniform(low=-1, high=1) for _ in range(self.nb_actions) ]
        
        
        if self.training:
            q_val = self.q_table[self.prev_observation][self.prev_action]  # Q(St,At)
            next_maxq = self.q_table[observation][np.argmax(self.q_table[observation])]  # MAX(Q(St+1,At))
            
            # 更新
            self.q_table[self.prev_observation][self.prev_action] = q_val + self.traning_rate * (self.prev_reward + self.gamma * next_maxq - q_val)
        
        if self.training:
            if self.epsilon > np.random.uniform(0, 1):
                # ランダム
                action = np.random.randint(0, self.nb_actions)
            else:
                # Q値が最大のindex(アクション)を取得
                action = np.argmax(self.q_table[observation])
            
        else:
            action = np.argmax(self.q_table[observation])
        
        self.prev_observation = observation
        self.prev_action = action
        return action

    def backward(self, reward, terminal):
        self.prev_reward = reward
        return []
    
    @property
    def layers(self):
        return []

# https://qiita.com/pocokhc/items/8ed40be84a144b28180d#q%E3%83%86%E3%83%BC%E3%83%96%E3%83%AB%E3%81%AE%E5%AE%9F%E8%A3%85