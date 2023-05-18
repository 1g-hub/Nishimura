from nsga2_problem import Problem
from nsga2_evolution import Evolution
import matplotlib.pyplot as plt
import randomrun
import run
import math
import random

'''
INITIAL_DECK = [
    4,4,1,#0
    1,1,5 #14
    ]
'''

INITIAL_DECK = [
            4,4,1,#0
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
            1,1,5 #14
            ]
        
TEST_COUNT = 10000
DESIRE_WIN_RATE = 0.50

#勝率
def f1(x):
    total_fitness = random.random()
    win_sum = 0
    '''
    for _ in range(TEST_COUNT):
        #res = randomrun.play(isFirst=False, card_arr=self.genom)
        #if res[0] == 1:
        if run.play(isFirst=False, card_values=x, p1policy= 1.0, p2policy= 1.0 ,is_elim = False, elim_num_player= 0, elim_num_enemy=0, issamedeck=True) == 1:
            win_sum += 1
    win_rate = win_sum / TEST_COUNT
    total_fitness += math.sqrt((DESIRE_WIN_RATE - win_rate) * (DESIRE_WIN_RATE - win_rate))

    win_sum = 0
    for _ in range(TEST_COUNT):
        #res = randomrun.play(isFirst=False, card_arr=self.genom)
        #if res[0] == 1:
        if run.play(isFirst=False, card_values=x, p1policy= 1.0, p2policy= 1.0, is_elim = False, elim_num_player= 0, elim_num_enemy=0, issamedeck= False) == 1:
            win_sum += 1
    win_rate = win_sum / TEST_COUNT
    total_fitness += math.sqrt((DESIRE_WIN_RATE - win_rate) * (DESIRE_WIN_RATE - win_rate))

    win_sum = 0
    for _ in range(TEST_COUNT):
        #res = randomrun.play(isFirst=False, card_arr=self.genom)
        #if res[0] == 1:
        if run.play(isFirst=True, card_values=x, p1policy= 1.0, p2policy= 1.0, is_elim = False, elim_num_player= 0, elim_num_enemy = 0, issamedeck= False) == 1:
            win_sum += 1
    win_rate = win_sum / TEST_COUNT
    total_fitness += math.sqrt((DESIRE_WIN_RATE - win_rate) * (DESIRE_WIN_RATE - win_rate))

    win_sum = 0
    for _ in range(TEST_COUNT):
        #res = randomrun.play(isFirst=False, card_arr=self.genom)
        #if res[0] == 1:
        if run.play(isFirst=False, card_values=x, p1policy= 0.0, p2policy= 1.0, is_elim = False, elim_num_player= 0, elim_num_enemy=0, issamedeck= False) == 1:
            win_sum += 1
    win_rate = win_sum / TEST_COUNT
    total_fitness += math.sqrt((DESIRE_WIN_RATE - win_rate) * (DESIRE_WIN_RATE - win_rate))

    win_sum = 0
    for _ in range(TEST_COUNT):
        #res = randomrun.play(isFirst=False, card_arr=self.genom)
        #if res[0] == 1:
        if run.play(isFirst=True, card_values=x, p1policy= 0.0, p2policy= 1.0, is_elim = False, elim_num_player= 0, elim_num_enemy=0, issamedeck= False) == 1:
            win_sum += 1
    win_rate = win_sum / TEST_COUNT
    total_fitness += math.sqrt((DESIRE_WIN_RATE - win_rate) * (DESIRE_WIN_RATE - win_rate))
    '''
    return total_fitness


#初期デッキからのパラメータの総変更量
def f2(x):

    sum = 0
    for i in range(len(x)):
        sum += abs(x[i] - INITIAL_DECK[i])
    #print(sum)
    return sum

# 初期デッキから調整されたカード枚数
def f3(x):

    sum = 0
    ischanged = False
    for i in range(len(x)):
        if x[i] != INITIAL_DECK[i]:
            ischanged = True
        if i % 3 == 2 and i != 0:
            if ischanged:
                sum += 1
            ischanged = False
    
    return sum

problem = Problem(num_of_variables=45, objectives=[f1, f2, f3], variables_range=[(1, 5)], expand = True)
evo = Evolution(problem, num_of_generations= 100)
evol = evo.evolve()
fig = plt.figure(figsize = (6, 6))
ax = fig.add_subplot(111, projection='3d')
for i in range(len(evol)):
    func = [i.objectives for i in evol[i]]
    ans_list = [i.features for i in evol[i]]
    print("func")
    print(func)
    print("ans_list")
    print(ans_list)
    function1 = [i[0] for i in func]
    function2 = [i[1] for i in func]
    function3 = [i[2] for i in func]
    #plt.zlabel('Function 3', fontsize=15)
    if i == 0:
        #print(str(function1) + " " + str(function2) + " " +  str(function3))
        ax.scatter(function1, function2, function3, c = "red")
    else:
        ax.scatter(function1, function2, function3, c = "blue")


ax.set_xlabel('function 1')
ax.set_ylabel('function 2')
ax.set_zlabel('function 3')
plt.savefig("nsga2.png", format="png", dpi=300)
'''
func = [i.objectives for i in evol[0]]
ans_list = [i.features for i in evol[0]]
print("func")
print(func)
print("ans_list")
print(ans_list)
function1 = [i[0] for i in func]
function2 = [i[1] for i in func]
plt.xlabel('Function 1', fontsize=15)
plt.ylabel('Function 2', fontsize=15)
plt.scatter(function1, function2, c = "red")
plt.savefig("nsga2.png", format="png", dpi=300)
'''