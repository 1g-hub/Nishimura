
from nsga2_population import Population
import random
import numpy as np
from nsga2_individual import Individual

class NSGA2Utils:

    def __init__(self, problem, num_of_individuals=50,
                 num_of_tour_particips=2, tournament_prob=0.9, crossover_param=2, mutation_param=5):

        self.problem = problem
        self.num_of_individuals = num_of_individuals
        self.num_of_tour_particips = num_of_tour_particips
        self.tournament_prob = tournament_prob
        self.crossover_param = crossover_param
        self.mutation_param = mutation_param

    def create_initial_population(self):
        population = Population()
        #1 つだけ元デッキ追加
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
        individual = Individual()
        individual.features = INITIAL_DECK
        #print(individual.features)
        self.problem.calculate_objectives(individual)
        population.append(individual)
        # その他ランダム
        for _ in range(self.num_of_individuals - 1):
            individual = self.problem.generate_individual()
            self.problem.calculate_objectives(individual)
            #print(individual.features)
            population.append(individual)
            #print(individual.features)
        return population

    #Non-dominated Sorting: the population is sorted and partitioned into fronts (F1, F2, etc.), where F1 (first front) indicates the approximated Pareto front.
    def fast_nondominated_sort(self, population):
        population.fronts = [[]]
        for individual in population:
            individual.domination_count = 0
            individual.dominated_solutions = []
            #同世代の他の個体と比較
            for other_individual in population:
                #他の個体を支配していたら
                if individual.dominates(other_individual):
                    individual.dominated_solutions.append(other_individual)
                #他の個体に支配されてたら
                elif other_individual.dominates(individual):
                    individual.domination_count += 1
            #他の個体に支配されて無ければfronts[0]にappend
            if individual.domination_count == 0:
                individual.rank = 0
                population.fronts[0].append(individual)
        i = 0
        while len(population.fronts[i]) > 0:
            temp = []
            for individual in population.fronts[i]:
                #支配している個体について
                for other_individual in individual.dominated_solutions:
                    other_individual.domination_count -= 1
                    if other_individual.domination_count == 0:
                        other_individual.rank = i + 1
                        temp.append(other_individual)
            i = i + 1
            population.fronts.append(temp)

    def calculate_crowding_distance(self, front):
        if len(front) > 0:
            solutions_num = len(front)
            for individual in front:
                individual.crowding_distance = 0

            for m in range(len(front[0].objectives)):
                front.sort(key=lambda individual: individual.objectives[m])
                front[0].crowding_distance = 10 ** 9
                front[solutions_num - 1].crowding_distance = 10 ** 9
                m_values = [individual.objectives[m] for individual in front]
                scale = max(m_values) - min(m_values)
                if scale == 0: scale = 1
                for i in range(1, solutions_num - 1):
                    front[i].crowding_distance += (front[i + 1].objectives[m] - front[i - 1].objectives[m]) / scale

    #混雑度トーナメントで用いる
    def crowding_operator(self, individual, other_individual):
        if (individual.rank < other_individual.rank) or \
                ((individual.rank == other_individual.rank) and (
                        individual.crowding_distance > other_individual.crowding_distance)):
            return 1
        else:
            return -1
    #遺伝子オペレートした集団
    def create_children(self, population):
        children = []
        while len(children) < len(population):
            parent1 = self.__tournament(population)
            parent2 = parent1
            while parent1 == parent2:
                parent2 = self.__tournament(population)
            child1, child2 = self.__crossover(parent1, parent2)
            self.__mutate(child1)
            self.__mutate(child2)
            self.problem.calculate_objectives(child1)
            self.problem.calculate_objectives(child2)
            children.append(child1)
            children.append(child2)

        return children

    '''
    def __crossover(self, individual1, individual2):
        child1 = self.problem.generate_individual()
        child2 = self.problem.generate_individual()
        num_of_features = len(child1.features)
        genes_indexes = range(num_of_features)
        for i in genes_indexes:
            beta = self.__get_beta()
            x1 = (individual1.features[i] + individual2.features[i]) / 2
            x2 = abs((individual1.features[i] - individual2.features[i]) / 2)
            child1.features[i] = x1 + beta * x2
            child2.features[i] = x1 - beta * x2
        return child1, child2

    def __get_beta(self):
        u = random.random()
        if u <= 0.5:
            return (2 * u) ** (1 / (self.crossover_param + 1))
        return (2 * (1 - u)) ** (-1 / (self.crossover_param + 1))
    '''

    def __crossover(self, individual1, individual2):
        #初期化と変数用意
        child1 = self.problem.generate_individual()
        child2 = self.problem.generate_individual()
        num_of_features = len(child1.features)
        tmp1 = individual1.features.copy()
        tmp2 = individual2.features.copy()
        cxpoint1 = np.random.randint(1, num_of_features)
        cxpoint2 = np.random.randint(1, num_of_features - 1)
        if cxpoint2 >= cxpoint1:
            cxpoint2 += 1
        else:
            cxpoint1, cxpoint2 = cxpoint2, cxpoint1
        tmp1[cxpoint1:cxpoint2], tmp2[cxpoint1:cxpoint2] = tmp2[cxpoint1:cxpoint2].copy(), tmp1[cxpoint1:cxpoint2].copy()
        child1.features = tmp1
        child2.features = tmp2
        return child1, child2
    
    '''
    def __mutate(self, child):
        num_of_features = len(child.features)
        for gene in range(num_of_features):
            u, delta = self.__get_delta()
            if u < 0.5:
                child.features[gene] += delta * (child.features[gene] - self.problem.variables_range[gene][0])
            else:
                child.features[gene] += delta * (self.problem.variables_range[gene][1] - child.features[gene])
            if child.features[gene] < self.problem.variables_range[gene][0]:
                child.features[gene] = self.problem.variables_range[gene][0]
            elif child.features[gene] > self.problem.variables_range[gene][1]:
                child.features[gene] = self.problem.variables_range[gene][1]

    def __get_delta(self):
        u = random.random()
        if u < 0.5:
            return u, (2 * u) ** (1 / (self.mutation_param + 1)) - 1
        return u, 1 - (2 * (1 - u)) ** (1 / (self.mutation_param + 1))
    '''
    def __mutate(self, child):
        num_of_features = len(child.features)
        index = np.random.randint(0, num_of_features)
        child.features[index] = np.random.randint(self.problem.variables_range[0][0], self.problem.variables_range[0][1] + 1)


    def __tournament(self, population):
        participants = random.sample(population.population, self.num_of_tour_particips)
        best = None
        for participant in participants:
            if best is None or (
                    self.crowding_operator(participant, best) == 1 and self.__choose_with_prob(self.tournament_prob)):
                best = participant

        return best

    def __choose_with_prob(self, prob):
        if random.random() <= prob:
            return True
        return False