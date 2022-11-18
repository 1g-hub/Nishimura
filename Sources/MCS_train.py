import matplotlib.pyplot as plt
import gym
from CardGameEnv import CardGameEnv
import numpy as np
import random
from MCS import MCS


env = CardGameEnv()
#a_mdp = A_MDP(env)  # 近似モデル(詳細は第10回を参照)

rl_mc = MCS(env)

total_reward_history = []


# 学習ループ
for episode in range(1):
    state = env.reset()
    done = False
    total_reward = 0
    action_history_train = []

    # 1episode 最大20stepで終わりにする
    for step in range(20):

        # アクションを決定
        action = rl_mc.sample_action(env, state, action_history_train,training=True)
        action_history_train.append(action)
        # 環境の1step
        n_state, reward, done, _ = env.step(action)
        total_reward += reward

        # 近似モデルの学習
        #a_mdp.train(state, action, n_state, reward, done)

        state = n_state
        #print("action_history_train")
        #print(action_history_train)

        if done:
            break
    
    #total_reward_history.append(total_reward)
    #print(total_reward_history)
    

# 5回テストする例
for episode in range(1):
    state = env.reset()
    #env.render()
    done = False
    total_reward = 0
    action_history_test = []

    # 1episode
    for step in range(20):
        action = rl_mc.sample_action(env, state,action_history_test)
        action_history_test.append(action)
        #print("observation")
        #print(env.observation)
        n_state, reward, done, _ = env.step(action)
        #env.render()
        state = n_state
        total_reward += reward
        #print(reward)
        #print("action_history_test")
        #print(action_history_test)

    print("{} reward: {}".format(episode, total_reward))
env.close()

# 報酬の推移をグラフで表示
plt.plot(total_reward_history)
plt.ylim((-2, 1))
plt.grid()
plt.show()