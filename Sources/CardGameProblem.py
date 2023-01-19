import numpy as np
from Problem import Problem
import randomrun

class CardGame(Problem):
    def __init__(self, size):
        super().__init__(self, size)
        self.size = 45
        self.MIN_VAL = 1
        self.MAX_VAL = 5
        self.SCORE_MIN = 0
        self.SCORE_MAX = float('inf')
    
    def init(self):
        pass

    def eval(self, np_arr):
        win_sum = 0
        for _ in range(10000):
            res = randomrun.play(isFirst=False, card_arr=np_arr)
            if res[0] == 1:
                win_sum += 1
        win_rate = win_sum / 10000
        
        return 1 / abs(0.50 - win_rate)
    
    def view(self, np_arr):
        print("score: {}".format(self.eval(np_arr)))
        for i in np_arr:
            if i % 3 == 0:
                print("\n")
            else:
                print(str(np_arr[i]) + " ")
        