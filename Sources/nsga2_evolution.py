from nsga2_utils import NSGA2Utils
from nsga2_population import Population
from tqdm import tqdm


class Evolution:

    def __init__(self, problem, num_of_generations=50, num_of_individuals=50, num_of_tour_particips=2, #An integer, default = 2, representing the number of participants in tournament selection operator.
                 tournament_prob=0.9, crossover_param=2,#representing the parameter used in simulated binary crossover.
                 mutation_param=5#representing the paramenter used in polynomial mutation.
                ):
        self.utils = NSGA2Utils(problem, num_of_individuals, num_of_tour_particips, tournament_prob, crossover_param,
                                mutation_param)
        self.population = None
        self.num_of_generations = num_of_generations
        self.on_generation_finished = []
        self.num_of_individuals = num_of_individuals

    def evolve(self):
        #初期個体群生成
        self.population = self.utils.create_initial_population()
        print(self.population)
        print(len(self.population))
        #高速優越ソート
        self.utils.fast_nondominated_sort(self.population)
        #print(self.population.fronts)
        #crowding distance
        for front in self.population.fronts:
            self.utils.calculate_crowding_distance(front)
        children = self.utils.create_children(self.population)
        returned_population = None
        #print(children)
        for i in tqdm(range(self.num_of_generations)):
            self.population.extend(children)
            self.utils.fast_nondominated_sort(self.population)
            new_population = Population()
            front_num = 0
            while len(new_population) + len(self.population.fronts[front_num]) <= self.num_of_individuals:
                self.utils.calculate_crowding_distance(self.population.fronts[front_num])
                new_population.extend(self.population.fronts[front_num])
                front_num += 1
            self.utils.calculate_crowding_distance(self.population.fronts[front_num])
            self.population.fronts[front_num].sort(key=lambda individual: individual.crowding_distance, reverse=True)
            new_population.extend(self.population.fronts[front_num][0:self.num_of_individuals - len(new_population)])
            returned_population = self.population
            self.population = new_population
            self.utils.fast_nondominated_sort(self.population)
            for front in self.population.fronts:
                self.utils.calculate_crowding_distance(front)
            children = self.utils.create_children(self.population)
        return returned_population.fronts[0]
