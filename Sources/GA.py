import math
import random

# 等差数列の和
def arithmetic_sequence_sum(size, start=1, diff=1):
    return size*( 2*start + (size-1)*diff )/2

# 等差数列の和の逆関数
def arithmetic_sequence_sum_inverse(val, start=1, diff=1):
    if diff == 0:
        return val
    t = diff-2*start + math.sqrt((2*start-diff)**2 + 8*diff*val)
    return t/(2*diff)

class GA():
    def __init__(self, 
            individual_max,   # 個体数
            save_elite=True,  # エリートを生存させるか
            select_method="ranking",  # 選択の方式(roulette or ranking)
            mutation=0.1,     # 突然変異の確率
        ):
        self.individual_max = individual_max

        self.save_elite = save_elite
        self.select_method = select_method
        self.mutation = mutation

    def init(self, problem):
        self.problem = problem

        # 各個体を生成します。
        self.best_individual = None
        self.individuals = []
        for _ in range(self.individual_max):
            o = problem.create()
            self.individuals.append(o)

            # 最高評価の個体を保存
            if self.best_individual is None or self.best_individual.getScore() < o.getScore():
                self.best_individual = o

        # 適応度でソート
        self.individuals.sort(key=lambda x: x.getScore())


    def step(self):

        # 次世代
        next_individuals = []

        if self.save_elite:
            # エリートを生存させる
            next_individuals.append(self.individuals[-1].copy())

        for _ in range(self.individual_max):  # whileでもいいけど安全のため
            # 個数が集まるまで繰り返す
            if len(next_individuals) > self.individual_max:
                break

            # 選択する
            if self.select_method == "roulette":
                o1 = self._selectRoulette()
                o2 = self._selectRoulette()
            elif self.select_method == "ranking":
                o1 = self._selectRanking()
                o2 = self._selectRanking()
            else:
                raise ValueError()

            # 交叉する
            new_o1, new_o2 = self._cross(o1, o2)

            # 次世代に追加
            next_individuals.append(new_o1)
            next_individuals.append(new_o2)

        # 世代交代
        self.individuals = next_individuals

        # 適応度でソート
        self.individuals.sort(key=lambda x: x.getScore())

        # 最高評価を保存
        if self.best_individual.getScore() < self.individuals[-1].getScore():
            self.best_individual = self.individuals[-1]


    def _selectRoulette(self):
        # 全個体の評価値を配列に入れる
        weights = [x.getScore() for x in self.individuals]

        w_min = min(weights)
        if w_min < 0:
            # 最小が負の場合は基準を0→w_min→に変更
            weights = [ w + (-w_min*2) for w in weights]

        # 重さの合計で乱数を出す
        r = random.random() * sum(weights)

        # 重さを順番に見ていき、乱数以下ならそのindexが該当
        num = 0
        for i, weights in enumerate(weights):
            num += weight
            if r <= num:
                return self.individuals[i]

        raise ValueError()


    def _selectRanking(self):
        # 個体の数
        size = len(self.individuals)

        # 全順位の合計値を出す
        num = arithmetic_sequence_sum(size)

        # 合計値から乱数を出す
        r = random.random() * num

        # 逆関数で順位を求める
        index = int(arithmetic_sequence_sum_inverse(r))
        return self.individuals[index]


    def _cross(self, parent1, parent2):
        genes1 = parent1.getArray()  # 親1の遺伝子情報
        genes2 = parent2.getArray()  # 親2の遺伝子情報

        # 子の遺伝子情報
        c_genes1 = []
        c_genes2 = []
        for i in range(len(genes1)):  # 各遺伝子を走査
            # 50%の確率で遺伝子を入れ替える
            if random.random() < 0.5:
                c_gene1 = genes1[i]
                c_gene2 = genes2[i]
            else:
                c_gene1 = genes2[i]
                c_gene2 = genes1[i]

            # 突然変異
            if random.random() < self.mutation:
                c_gene1 = self.problem.randomVal()
            if random.random() < self.mutation:
                c_gene2 = self.problem.randomVal()

            c_genes1.append(c_gene1)
            c_genes2.append(c_gene2)

        # 遺伝子をもとに子を生成
        childe1 = self.problem.create(c_genes1)
        childe2 = self.problem.create(c_genes2)
        return childe1, childe2