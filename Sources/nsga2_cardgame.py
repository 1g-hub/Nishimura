from nsga2_problem import Problem
from nsga2_evolution import Evolution
import matplotlib.pyplot as plt
import randomrun
import math

'''
INITIAL_DECK = [
    4,4,1,#0
    1,1,5 #14
    ]
'''

INITIAL_DECK = [
                1,1,1,#0
                2,2,2,#1
                3,3,3,#2
                4,3,4,#3
                5,4,5,#4
                2,2,2,#5
                2,3,3,#6
                1,1,1,#7
                1,3,2,#8
                2,1,2,#9
                3,1,3,#10
                1,2,2,#11
                2,3,3,#12
                1,1,1,#13
                2,1,3 #14
            ]
        
TEST_COUNT = 10000
DESIRE_WIN_RATE = 0.50

#勝率
def f1(x):
    win_sum = 0
    for _ in range(TEST_COUNT):
        res = randomrun.play(isFirst=False, card_arr=x, is_all_change=True)
        if res[0] == 1:
            win_sum += 1
    win_rate = win_sum / TEST_COUNT
    return math.sqrt((DESIRE_WIN_RATE - win_rate) * (DESIRE_WIN_RATE - win_rate))


#初期デッキからのパラメータの総変更量
def f2(x):
    sum = 0
    for i in range(len(x)):
        sum += abs(x[i] - INITIAL_DECK[i])
    return sum


problem = Problem(num_of_variables=45, objectives=[f1, f2], variables_range=[(1, 5)], expand= False)
evo = Evolution(problem)
evol = evo.evolve()
func = [i.objectives for i in evol]
ans_list = [i.features for i in evol]
print("func")
print(func)
print("ans_list")
print(ans_list)
function1 = [i[0] for i in func]
function2 = [i[1] for i in func]
plt.xlabel('WinRate', fontsize=15)
plt.ylabel('TotalParameterChanges', fontsize=15)
plt.scatter(function1, function2)
plt.savefig("nsga2_cardgame.png", format="png", dpi=300)