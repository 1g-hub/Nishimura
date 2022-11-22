import gym
import numpy as np
from collections import defaultdict
from CardGameEnv import CardGameEnv

env = CardGameEnv()
#Q\table
Q = {}
Q[""] = [np.random.uniform(low=-1, high=1) for _ in range(env.action_space.n)]
#割引率
gamma = 0.9
#学習率
alpha = 0.02
num_episodes = 500000

for e in range(num_episodes):                                        # テスト開始
    if e % 10000 == 0 : print(e, "," , end="")                 # プログラム進捗確認用
    epsi    = 0.1                                                              # ε-greedy法
    episode = []
    state   = env.reset()    
    done = False                                                  # ゲーム開始、初回カード配り

    while True:
        print(Q)
        print(state)                                                                # カード引いていく
        action = np.argmax(Q[state]) if epsi <= np.random.uniform(0,1) and state in Q \
                 else np.random.choice(2)                                      # epsiが大きい時はランダムアクション
        next_state, reward, done, info = env.step(action)                      # 行動に応じた状態、報酬を算出
        episode.append((state, action))                                        # 結果を結合
        state = next_state
        if done: break                                                         # ゲーム終了

    states, actions = zip(*episode)                                            # 結果を分解
    reward_sum.append(reward)                                                  # 報酬値を追加
    disco = np.array([gamma**i for i in range(len(actions))])[::-1]            # 割引率

    for i, state in enumerate(states):
        Q[state][actions[i]] += alpha*(reward*disco[i] - Q[state][actions[i]]) # Q値更新

np.savetxt('test.txt', reward_sum,fmt="%.0f")                                  # 報酬結果をテキストに保存


# http://arduinopid.web.fc2.com/N67.html