import numpy as np
import matplotlib.pyplot as plt
import randomrun
import run
from tqdm import tqdm
import math

class Individual:
    # 各個体のクラス
    def __init__(self, genom):
        self.genom = genom
        self.fitness = 0.0
        self.set_fitness()

    # 個体に対する評価関数の値をfitnessに格納
    def set_fitness(self):
        win_sum = 0
        for _ in range(TEST_COUNT):
            #res = randomrun.play(isFirst=False, card_arr=self.genom)
            #if res[0] == 1:
            if run.play(isFirst=False, card_values=self.genom, p1policy= 1.0, p2policy= 1.0) == 1:
                win_sum += 1
        win_rate = win_sum / TEST_COUNT

        self.fitness =  math.sqrt((DESIRE_WIN_RATE - win_rate) * (DESIRE_WIN_RATE - win_rate))

    # self.fitness を出力
    def get_fitness(self):
        return self.fitness

    # 遺伝子の突然変異
    def mutate(self):
        tmp = self.genom.copy()
        i = np.random.randint(0, len(self.genom) - 1)
        tmp[i] = np.random.randint(1,  6)
        self.genom = tmp
        self.set_fitness()

# ルーレット方式


def select_roulette(generation):
    selected = []
    weights = [ind.get_fitness() for ind in generation]
    norm_weights = [ind.get_fitness() / sum(weights) for ind in generation]
    selected = np.random.choice(
        generation, size=len(generation), p=norm_weights)
    return selected

# トーナメント方式


def select_tournament(generation):
    selected = []
    for i in range(len(generation)):
        tournament = np.random.choice(generation, 3, replace=False)
        min_genom = min(tournament, key=Individual.get_fitness).genom.copy()
        selected.append(Individual(min_genom))
    return selected

# 交叉


def crossover(selected):
    children = []
    if POPURATIONS % 2:
        selected.append(selected[0])
    for child1, child2 in zip(selected[::2], selected[1::2]):
        if np.random.rand() < CROSSOVER_PB:
            child1, child2 = cross_two_point_copy(child1, child2)
        children.append(child1)
        children.append(child2)
    children = children[:POPURATIONS]
    return children

# 二点交叉


def cross_two_point_copy(child1, child2):
    size = len(child1.genom)
    tmp1 = child1.genom.copy()
    tmp2 = child2.genom.copy()
    cxpoint1 = np.random.randint(1, size)
    cxpoint2 = np.random.randint(1, size - 1)
    if cxpoint2 >= cxpoint1:
        cxpoint2 += 1
    else:
        cxpoint1, cxpoint2 = cxpoint2, cxpoint1
    tmp1[cxpoint1:cxpoint2], tmp2[cxpoint1:cxpoint2] = tmp2[cxpoint1:cxpoint2].copy(
    ), tmp1[cxpoint1:cxpoint2].copy()
    new_child1 = Individual(tmp1)
    new_child2 = Individual(tmp2)
    return new_child1, new_child2

# 突然変異
def mutate(children):
    for child in children:
        if np.random.rand() < MUTATION_PB:
            child.mutate()
    return children

# 初期世代の作成
def create_generation(POPURATIONS, GENOMS):
    print("create generation")
    generation = []
    for i in range(POPURATIONS):
        generation.append(Individual(INITAIL_DECK))
    return generation

#GA のソルバー
def ga_solve(generation):
    best = []
    worst = []
    # Generation loop
    print("Generation Loop Start")
    for i in tqdm(range(GENERATIONS)):
        # --- Step1. Print fitness in the generation
        best_ind = min(generation, key=Individual.get_fitness)
        best.append(best_ind.fitness)
        worst_ind = max(generation, key=Individual.get_fitness)
        worst.append(worst_ind.fitness)
        print("Generation: " + str(i)
              + ": Best fitness: " + str(best_ind.fitness)
                + ". Worst fitness: " + str(worst_ind.fitness))
        # --- Step2. Selection (Roulette)
        # selected = select_roulette(generation)
        selected = select_tournament(generation)

        # --- Step3. Crossover (two_point_copy)
        children = crossover(selected)

        # --- Step4. Mutation
        generation = mutate(children)

    print("Generation loop ended. The best individual: ")
    print(best_ind.genom)
    print("Best Individual fitness")
    print(best_ind.fitness)
    return best, worst


# ハイパーパラメータ
POPURATIONS =50  # 1 世代あたりの個体数
GENOM_SIZE = 45  # 遺伝子のサイズ今回は 3 × 15 で
GENERATIONS = 50 # 世代数
CROSSOVER_PB = 0.40
MUTATION_PB = 0.20
INITAIL_DECK = [
    1, 2, 1,  # 0
    2, 2, 2,  # 1
    3, 3, 3,  # 2
    4, 3, 4,  # 3
    5, 4, 5,  # 4
    2, 2, 2,  # 5
    2, 3, 3,  # 6
    1, 1, 1,  # 7
    1, 3, 2,  # 8
    2, 1, 2,  # 9
    3, 1, 3,  # 10
    1, 2, 2,  # 11
    2, 3, 3,  # 12
    1, 1, 1,  # 13
    2, 1, 3  # 14
]
TEST_COUNT = 10000
DESIRE_WIN_RATE = 0.50


# create first genetarion
generation = create_generation(POPURATIONS, GENOM_SIZE)

# solve
best, worst = ga_solve(generation)

# plot
fig, ax = plt.subplots()
ax.plot(best, label='min')
ax.plot(worst, label='max')
ax.axhline(y=GENOM_SIZE, color='black', linestyle=':', label='true')
ax.set_xlim([0, GENERATIONS - 1])
ax.set_ylim([0, 0.1])
ax.legend(loc='best')
ax.set_xlabel('Generations')
ax.set_ylabel('Fitness')
ax.set_title('Tournament Select')
plt.savefig("GA.png", format="png", dpi=300)