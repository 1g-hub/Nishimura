import gym
import numpy as np
import random


class MCS():
    def __init__(self, env):

        self.nb_action = env.action_space.n # アクション数
        self.max_turn = 20  # 最大ターン数

        self.epsilon = 0.1
        self.simulation_times = 20

        self.actions = [i for i in range(self.nb_action)]

    # state から実環境へのアクションを返す
    def sample_action(self, env, state, actionlist, training=False):
        
        # Q値を計算する
        q_vals = self.compute_q_vals(env, state, actionlist)

        if training:
            # トレーニング中はε-greedy
            if np.random.random() < self.epsilon:
                # epsilonより低いならランダムに移動
                return np.random.randint(self.nb_action)
            else:
                # Q値が最大のアクションを実行
                select_actions = []
                for i, v in enumerate(q_vals):
                    if v == max(q_vals):
                        select_actions.append(i)
                return random.sample(select_actions, 1)[0]
        else:
            return np.argmax(q_vals)


    #Q値を計算する
    def compute_q_vals(self, env, init_state,actionlist):
        q_vals = []
        default_state = init_state
        previous_action_list = actionlist
        print(default_state)
        # 全アクション
        for action in self.actions:
            total_reward = 0
            #print("Q値計算の時のstate")
            #print(env.observation)
            env.observation = default_state

            # シミュレーション
            for _ in range(self.simulation_times):
                
                simu_action_list = []
                simu_action_list.append(action)
                obs, re, don, info = env.step(action)
                done = don
                step = 0
                
                # 1episode
                while not done and step < self.max_turn:
                    step += 1

                    # π(ランダム)
                    action = np.random.randint(self.nb_action)
                    simu_action_list.append(action)

                    obs, re, don, info = env.step(action)

                    total_reward += re
                    done = don
                    state = env.observation
                
            # Kエピソードの平均報酬、これが行動価値になる
            reward = total_reward / self.simulation_times
            q_vals.append(reward)
            #print("q_vals")
            #print(q_vals)
            env.observation = default_state
            print(env.observation)

        return q_vals