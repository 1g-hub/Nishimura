import math
import gym
from ELAgent import ELAgent
import numpy as np
from CardGameEnv import CardGameEnv
import itertools
import copy
from math import sqrt, log
from time import time
import random
import sys

def moving_average(v, n):
    n = min(len(v), n)
    ret = [.0]*(len(v)-n+1)
    ret[0] = float(sum(v[:n]))/n
    for i in range(len(v)-n):
        ret[i+1] = ret[i] + float(v[n+i] - v[i])/n
    return ret


def ucb(node):
    return node.value / node.visits + sqrt(log(node.parent.visits)/node.visits)


def combinations(space):
    if isinstance(space, gym.spaces.Discrete):
        return range(space.n)
    elif isinstance(space, gym.spaces.Tuple):
        return itertools.product(*[combinations(s) for s in space.spaces])
    else:
        raise NotImplementedError


class Node:
    def __init__(self, parent, action):
        self.parent = parent
        self.action = action
        self.children = []
        self.explored_children = 0
        self.visits = 0
        self.value = 0

class MonteCarloAgent(ELAgent):

    def __init__(self, epsilon=0.1,loops=300, max_depth=1000, playouts=10000):
        super().__init__(epsilon)

        self.loops = loops
        self.max_depth = max_depth
        self.playouts = playouts
        self.save_player_deck = []
        self.save_player_hand = []
        self.save_player_isplayed = []
        self.save_player_dead = []
        self.save_enemy_deck = []
        self.save_enemy_hand = []
        self.save_enemy_isplayed = []
        self.save_player_dead = []
    
    def print_stats(self, loop, score, avg_time):
        sys.stdout.write('\r%3d   score:%10.3f   avg_time:%4.1f s' % (loop, score, avg_time))
        sys.stdout.flush()


    
    def run(self):
        best_rewards = []
        env = CardGameEnv()
        start_time = time()

        for loop in range(self.loops):
            env.reset()
            root = Node(None, None)
            print("intial state ")
            print(env.observation)

            best_actions = []
            best_reward = float("-inf")

            for _ in range(self.playouts):

                self.save_player_deck = env.player.deck
                self.save_player_hand = env.player.hand
                self.save_player_isplayed = env.player.is_played
                self.save_player_dead = env.player.discard
                self.save_enemy_deck = env.player.enemy.deck
                self.save_enemy_hand = env.player.enemy.hand
                self.save_enemy_isplayed = env.player.enemy.is_played
                self.save_player_dead = env.player.enemy.discard

                sum_reward = 0
                node = root
                done = False
                actions = []
                #print("observation")
                #print(env.observation)

                # selection
                while node.children:
                    print("node.children")
                    print(node.children)
                    if node.explored_children < len(node.children):
                        child = node.children[node.explored_children]
                        node.explored_children += 1
                        node = child
                    else:
                        node = max(node.children, key=ucb)
                    #print("node.action")
                    #print(node.action)
                    _, reward, done, _ = env.step(node.action)
                    sum_reward += reward
                    actions.append(node.action)
                    #print(env.observation)

                # expansion
                if not done:
                    node.children = [Node(node, a) for a in combinations(env.action_space)]
                    random.shuffle(node.children)

                # playout
                while not done:
                    action = env.action_space.sample()
                    _, reward, done, _ = env.step(action)
                    sum_reward += reward
                    actions.append(action)

                    if len(actions) > self.max_depth:
                        sum_reward -= 100
                        break

                # remember best
                if best_reward < sum_reward:
                    best_reward = sum_reward
                    best_actions = actions

                # backpropagate
                while node:
                    node.visits += 1
                    node.value += sum_reward
                    node = node.parent

                env.player.deck = self.save_player_dead
                env.player.hand = self.save_player_hand
                env.player.is_played = self.save_enemy_isplayed
                env.player.discard = self.save_player_dead
                env.player.enemy.deck = self.save_enemy_deck
                env.player.enemy.hand = self.save_enemy_hand
                env.player.enemy.is_played = self.save_enemy_isplayed
                env.player.enemy.discard = self.save_player_dead


            sum_reward = 0
            for action in best_actions:
                _, reward, done, _ = env.step(action)
                sum_reward += reward
                if done:
                    break

            best_rewards.append(sum_reward)
            score = max(moving_average(best_rewards, 100))
            avg_time = (time()-start_time)/(loop+1)
            self.print_stats(loop+1, score, avg_time)
    
def main():
    agent = MonteCarloAgent()
    agent.run()

if __name__ == "__main__":
    main()
